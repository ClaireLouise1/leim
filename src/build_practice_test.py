"""Builds the topic practice-test pages: one page per subject that runs a 10-question
practice test for any topic in it (21 Nov 2026):
  Maths:   practice-test.html?t=angle-chase          (makers from exam-mix-<strand>.js)
  English: english-practice-test.html?t=comma-catch  (makers from english-exam-mix-<section>.js)
Questions come from that topic's own game makers in the Exam Mix bundles
(original questions, generated fresh each time, with the worked "why").
English uses the English Exam Mix page's styles, each game's button order (orders)
and punctuation renderer (pu), and the game's .gx-<slug> styles on the question card.
Untimed, one question at a time, working shown after each answer, score /10 at the end.
Best score is kept in the student's own browser (localStorage, key leim-pt-<slug>)
and shown on the subject page cards. Called by build_subject_hub.py."""
import re, os, json
ROOT = os.path.join(os.path.dirname(__file__), '..'); os.chdir(ROOT)

SUBJ = {
 'maths': dict(page='practice-test.html', mix='exam-mix.html', hub='junior-cycle-maths.html', title='Maths', prefix='exam-mix-', en=False),
 'english': dict(page='english-practice-test.html', mix='english-exam-mix.html', hub='junior-cycle-english.html', title='English', prefix='english-exam-mix-', en=True),
}

def build(topics, subject='maths'):
    """topics: {slug: {"topic":..., "game":..., "bundle": <bundle section>}} for one subject"""
    S = SUBJ[subject]
    mix = open(S['mix'], encoding='utf-8').read()
    idx = open('index.html', encoding='utf-8').read()
    styles = ''.join(re.findall(r'<style>.*?</style>', mix, re.S))
    head = idx.split('<style>')[0]
    head = re.sub(r'<title>.*?</title>', '<title>Junior Cycle %s practice test | Léim</title>' % S['title'], head)
    head = head.replace('href="https://leim.ie/"', 'href="https://leim.ie/%s"' % S['page']).replace('content="https://leim.ie/"', 'content="https://leim.ie/%s"' % S['page'])
    hdr = idx.split('<body>')[1].split('<main id="main">')[0]
    foot = '</main>' + idx.split('</main>')[1]
    hdr, foot = (x.replace('href="#join"', 'href="index.html#join"') for x in (hdr, foot))   # the sign-up form is on the home page
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
    main = ('''<main id="main">
<div class="pt">
<p class="crumbs"><a href="index.html">Home</a> › <a href="HUB">TITLE</a> › Practice test</p>
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
    <a class="btn ghost2" href="HUB">← All TITLE topics</a>
  </div>
</div>
</div>
''').replace('HUB', S['hub']).replace('TITLE', S['title'])
    js = '''<script>
(function(){
var T=%s,EN=%s,HUB=%s,PRE=%s;
var N=10,$=function(i){return document.getElementById(i);};
var slug=(new URLSearchParams(location.search).get("t")||"").toLowerCase();
var info=T[slug];
if(!info){$("qn").textContent="Pick a topic from the topics page.";$("en").innerHTML='<a class="btn" href="'+HUB+'">Go to the topics</a>';return;}
document.title=info.topic+" practice test | Léim";
$("tname").textContent=info.topic;
$("gamelink").href=slug+".html";$("gamelink").textContent="🎮 Play "+info.game;
function rnd(a){return a[Math.floor(Math.random()*a.length)];}
function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t;}return a;}
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;");}
var qs,i,score,miss,locked;
function bar(){var h="";for(var k=0;k<N;k++){var c=k<qs.length&&qs[k].res?qs[k].res:(k===i?"now":"");h+='<i class="'+c+'"></i>';}$("pbar").innerHTML=h;}
function G(){return EN?window.LEIM_EN[slug]:{M:window.LEIM_MAKERS[slug],orders:[],pu:null};}
function make(){var M=G().M,list=(M.mixed&&M.mixed.length)?M.mixed:[],seen={},out=[],tries=0;
  while(out.length<N&&tries<200){tries++;var q;try{q=rnd(list)();}catch(e){continue;}
    if(!q||q.answer==null||!q.wrong||q.wrong.length<(q.nw||3))continue;var key=q.review||q.en+q.frame;if(seen[key])continue;seen[key]=1;out.push(q);}
  return out;}
function start(){qs=make();i=0;score=0;miss=[];$("done").hidden=true;$("quiz").hidden=false;show();}
function show(){locked=false;var q=qs[i];bar();
  $("qn").textContent="Question "+(i+1)+" of "+N;
  $("en").innerHTML=esc(q.en);
  $("frame").innerHTML=(q.html||"")+esc(q.frame||"");
  $("frame").className="frame"+(EN?"":" gx-"+slug)+(q.frame&&q.frame.length>24?" long":"");
  if(EN)$("quiz").className="qcard gx-"+slug;   /* English games' styles are scoped to .gx-<slug> on the card */
  $("why").innerHTML="";
  var box=$("choices");box.innerHTML="";
  box.className="choices"+([q.answer].concat(q.wrong).some(function(x){return String(x).length>16;})?" one":"");
  var g=G(),opts=shuffle([String(q.answer)].concat(q.wrong.slice(0,q.nw||3).map(String))),ORDS=q.fixed?[q.fixed]:(g.orders||[]);
  for(var k=0;k<ORDS.length;k++){var O=ORDS[k];if(opts.every(function(o){return O.indexOf(o)>=0;})){opts.sort(function(a,b){return O.indexOf(a)-O.indexOf(b);});break;}}   /* label buttons keep the game's order */
  opts.forEach(function(t,n){
    var b=document.createElement("button");b.className="choice";b.type="button";b.setAttribute("data-v",t);
    if(g.pu)b.innerHTML=g.pu(t);else b.textContent=t;
    b.setAttribute("aria-label","Option "+(n+1)+": "+t);
    b.onclick=function(){pick(b,t);};box.appendChild(b);});
  $("quiz").scrollIntoView({behavior:"smooth",block:"start"});}
function pick(btn,t){if(locked)return;locked=true;var q=qs[i],ok=String(t)===String(q.answer);
  [].forEach.call($("choices").children,function(c){c.disabled=true;if(c.getAttribute("data-v")===String(q.answer))c.classList.add("right");});
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
  $("mlist").innerHTML=miss.length?"<b>Go back over these:</b><ul>"+miss.map(function(q){return EN?"<li><b>"+esc(q.review||(q.en+" → "+q.answer))+"</b>"+(q.why?'<br><span class="w">'+esc(q.why)+"</span>":"")+"</li>":"<li>"+esc(q.why||(q.en+" Answer: "+q.answer))+"</li>";}).join("")+"</ul>":"";
  $("done").scrollIntoView({behavior:"smooth",block:"start"});}
$("again").onclick=start;
var sc=document.createElement("script");sc.src=PRE+info.bundle+".js?v=1";
sc.onload=function(){var R=EN?window.LEIM_EN:window.LEIM_MAKERS;if(!R||!R[slug]){$("qn").textContent="Sorry, this test isn't ready yet.";return;}start();};
sc.onerror=function(){$("qn").textContent="Couldn't load the questions. Check your connection and try again.";};
document.body.appendChild(sc);
})();
</script>
''' % (json.dumps(topics, ensure_ascii=False), 'true' if S['en'] else 'false', json.dumps(S['hub']), json.dumps(S['prefix']))
    page = head + styles + css + '\n</head>\n<body>' + hdr + main + foot.replace('</body>', js + '</body>')
    open(S['page'], 'w', encoding='utf-8').write(page)
    print('built', S['page'], 'for', len(topics), 'topics')
