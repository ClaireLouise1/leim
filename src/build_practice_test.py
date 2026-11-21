"""Builds practice-test.html: one page that runs a 10-question practice test for any
Maths topic, e.g. practice-test.html?t=angle-chase  (21 Nov 2026).
Questions come from that topic's game makers in the exam-mix-<strand>.js bundles
(original questions, generated fresh each time, with the worked "why").
Untimed, one question at a time, working shown after each answer, score /10 at the end.
Best score is kept in the student's own browser (localStorage, key leim-pt-<slug>)
and shown on the subject page cards. Called by build_subject_hub.py."""
import re, os, json
ROOT = os.path.join(os.path.dirname(__file__), '..'); os.chdir(ROOT)

def build(topics):
    """topics: {slug: {"topic":..., "game":..., "bundle":"number|algebra|geometry|stats"}}"""
    mix = open('exam-mix.html', encoding='utf-8').read()
    idx = open('index.html', encoding='utf-8').read()
    styles = ''.join(re.findall(r'<style>.*?</style>', mix, re.S))
    head = idx.split('<style>')[0]
    head = re.sub(r'<title>.*?</title>', '<title>Junior Cycle Maths practice test | Léim</title>', head)
    head = head.replace('href="https://leim.ie/"', 'href="https://leim.ie/practice-test.html"').replace('content="https://leim.ie/"', 'content="https://leim.ie/practice-test.html"')
    hdr = idx.split('<body>')[1].split('<main id="main">')[0]
    foot = '</main>' + idx.split('</main>')[1]
    css = '''<style>
.pt{max-width:640px;margin:0 auto;padding:18px 16px 40px}
.pt .crumbs{font-size:.9rem;color:var(--muted);margin:0 0 6px}.pt .crumbs a{color:var(--muted)}
.pt h1{font-size:1.7rem;line-height:1.15;margin:0 0 4px}
.pt h1 .acc{background:linear-gradient(transparent 55%,var(--sun) 55%)}
.pt .sub{color:var(--muted);font-weight:600;margin:0 0 14px}
.pbar{display:flex;gap:5px;margin:0 0 16px}.pbar i{flex:1;height:8px;border-radius:99px;background:var(--mist)}
.pbar i.ok{background:var(--green)}.pbar i.no{background:#D9534F}.pbar i.now{background:var(--sun)}
.qcard{border:3px solid var(--ink);border-radius:22px;padding:18px;background:#fff}
.qn{font-weight:800;color:var(--muted);font-size:.9rem;margin-bottom:6px}
.why{margin-top:14px;background:var(--green-soft);border-radius:14px;padding:12px 14px;font-weight:600;line-height:1.45}
.why.bad{background:#FBE9E8}
.why b{display:block;margin-bottom:4px}
.nextb{margin-top:14px;width:100%}
.res{text-align:center}
.res .big{font-size:64px;font-weight:800;letter-spacing:-.03em;line-height:1}
.res .msg{font-weight:700;font-size:1.1rem;margin:8px 0 2px}
.mlist{text-align:left;margin-top:18px}
.mlist li{margin:10px 0;line-height:1.45}
.mlist .w{color:var(--green-dark);font-weight:600}
.acts{display:grid;gap:10px;margin-top:20px}
.acts .btn{width:100%;text-align:center}
.btn.ghost2{background:#fff;border:2px solid var(--ink);color:var(--ink)}
</style>'''
    main = '''<main id="main">
<div class="pt">
<p class="crumbs"><a href="index.html">Home</a> › <a href="junior-cycle-maths.html">Maths</a> › Practice test</p>
<h1>📝 <span class="acc" id="tname">Practice test</span></h1>
<p class="sub" id="tsub">10 questions · no timer · see the working after each one</p>
<div class="pbar" id="pbar"></div>
<div id="quiz" class="qcard">
  <div class="qn" id="qn">Loading…</div>
  <div class="prompt"><div class="en" id="en"></div><div class="frame" id="frame"></div></div>
  <div class="choices" id="choices"></div>
  <div id="why"></div>
</div>
<div id="done" class="qcard res" hidden>
  <div class="big" id="score">0/10</div>
  <p class="msg" id="msg"></p>
  <p class="sub" id="bestline" style="margin:0"></p>
  <div class="mlist" id="mlist"></div>
  <div class="acts">
    <button class="btn" id="again" type="button">🔁 New practice test</button>
    <a class="btn ghost2" id="gamelink" href="#">🎮 Play the game</a>
    <a class="btn ghost2" href="junior-cycle-maths.html">← All Maths topics</a>
  </div>
</div>
</div>
'''
    js = '''<script>
(function(){
var T=%s;
var N=10,$=function(i){return document.getElementById(i);};
var slug=(new URLSearchParams(location.search).get("t")||"").toLowerCase();
var info=T[slug];
if(!info){$("qn").textContent="Pick a topic from the Maths page.";$("en").innerHTML='<a class="btn" href="junior-cycle-maths.html">Go to Maths topics</a>';return;}
document.title=info.topic+" practice test | Léim";
$("tname").textContent=info.topic;
$("gamelink").href=slug+".html";$("gamelink").textContent="🎮 Play "+info.game;
function rnd(a){return a[Math.floor(Math.random()*a.length)];}
function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t;}return a;}
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;");}
var qs,i,score,miss,locked;
function bar(){var h="";for(var k=0;k<N;k++){var c=k<qs.length&&qs[k].res?qs[k].res:(k===i?"now":"");h+='<i class="'+c+'"></i>';}$("pbar").innerHTML=h;}
function make(){var M=window.LEIM_MAKERS[slug],list=(M.mixed&&M.mixed.length)?M.mixed:[],seen={},out=[],tries=0;
  while(out.length<N&&tries<200){tries++;var q;try{q=rnd(list)();}catch(e){continue;}
    if(!q||!q.answer||!q.wrong||q.wrong.length<3)continue;var key=q.review||q.en+q.frame;if(seen[key])continue;seen[key]=1;out.push(q);}
  return out;}
function start(){qs=make();i=0;score=0;miss=[];$("done").hidden=true;$("quiz").hidden=false;show();}
function show(){locked=false;var q=qs[i];bar();
  $("qn").textContent="Question "+(i+1)+" of "+N;
  $("en").innerHTML=esc(q.en);
  $("frame").innerHTML=(q.html||"")+esc(q.frame||"");
  $("frame").className="frame gx-"+slug+(q.frame&&q.frame.length>24?" long":"");
  $("why").innerHTML="";
  var box=$("choices");box.innerHTML="";
  box.className="choices"+([q.answer].concat(q.wrong).some(function(x){return String(x).length>16;})?" one":"");
  shuffle([q.answer].concat(q.wrong.slice(0,3))).forEach(function(t){
    var b=document.createElement("button");b.className="choice";b.type="button";b.textContent=t;
    b.onclick=function(){pick(b,t);};box.appendChild(b);});
  $("quiz").scrollIntoView({behavior:"smooth",block:"start"});}
function pick(btn,t){if(locked)return;locked=true;var q=qs[i],ok=String(t)===String(q.answer);
  [].forEach.call($("choices").children,function(c){c.disabled=true;if(c.textContent===String(q.answer))c.classList.add("right");});
  if(ok){score++;q.res="ok";}else{btn.classList.add("wrong");q.res="no";miss.push(q);}
  bar();
  var w=q.why?esc(q.why):"The answer is "+esc(q.answer)+".";
  $("why").innerHTML='<div class="why'+(ok?"":" bad")+'"><b>'+(ok?"✅ Right!":"❌ Not this time. Answer: "+esc(q.answer))+'</b>'+w+'</div>'+
    '<button class="btn nextb" type="button" id="nx">'+(i<N-1?"Next question →":"See my score")+'</button>';
  $("nx").onclick=function(){i++;if(i<N)show();else end();};$("nx").focus({preventScroll:true});}
function end(){$("quiz").hidden=true;$("done").hidden=false;bar();
  $("score").textContent=score+"/"+N;
  $("msg").textContent=score>=9?"🏆 Exam ready!":score>=7?"💪 Strong. Fix the ones below.":score>=5?"👍 Getting there. Read the working below, then try again.":"🌱 Play the game first, then try again.";
  var best=0;try{best=+localStorage.getItem("leim-pt-"+slug)||0;if(score>best){localStorage.setItem("leim-pt-"+slug,score);best=score;}}catch(e){}
  $("bestline").textContent=best?"Your best: "+best+"/"+N:"";
  $("mlist").innerHTML=miss.length?"<b>Go back over these:</b><ul>"+miss.map(function(q){return "<li>"+esc(q.why||(q.en+" Answer: "+q.answer))+"</li>";}).join("")+"</ul>":"";
  $("done").scrollIntoView({behavior:"smooth",block:"start"});}
$("again").onclick=start;
var sc=document.createElement("script");sc.src="exam-mix-"+info.bundle+".js?v=1";
sc.onload=function(){if(!window.LEIM_MAKERS||!window.LEIM_MAKERS[slug]){$("qn").textContent="Sorry, this test isn't ready yet.";return;}start();};
sc.onerror=function(){$("qn").textContent="Couldn't load the questions. Check your connection and try again.";};
document.body.appendChild(sc);
})();
</script>
''' % json.dumps(topics, ensure_ascii=False)
    page = head + styles + css + '\n</head>\n<body>' + hdr + main + foot.replace('</body>', js + '</body>')
    open('practice-test.html', 'w', encoding='utf-8').write(page)
    print('built practice-test.html for', len(topics), 'topics')
