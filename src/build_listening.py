import re, json, html
R='/home/claude/leim/'
src=open(R+'src/jc-spanish-exam-pack.html',encoding='utf-8').read()
start=src.index('<!-- PAGE 28: PRACTICE SCRIPTS 1-2 -->')
end=src.index('<!-- PAGE 32',start) if '<!-- PAGE 32' in src[start:] else len(src)
chunk=src[start:end]
def clean(s):
    s=re.sub(r'<[^>]+>','',s); return html.unescape(s).strip()
# walk h3 + p in order
cards=[];cur=None
for m in re.finditer(r'<h3>(.*?)</h3>|<p>(.*?)</p>',chunk,re.S):
    if m.group(1):
        cur={'title':clean(m.group(1)),'parts':[]};cards.append(cur);continue
    p=m.group(2)
    sp=re.match(r'\s*<span class="sp">(.*?)</span>\s*(.*)',p,re.S)
    if sp:
        tag=clean(sp.group(1));txt=clean(sp.group(2))
        if re.fullmatch(r'\(\d\)',tag):
            if txt.startswith('—'):
                lines=[[i%2,t.strip()] for i,t in enumerate(txt.split('—')[1:])]
            else: lines=[[0,txt]]
            cur['parts'].append({'label':'Item '+tag.strip('()'),'lines':lines})
        else:
            if not cur['parts']: cur['parts'].append({'label':'','lines':[],'who':[]})
            part=cur['parts'][0]; who=tag.rstrip(':')
            if who not in part['who']: part['who'].append(who)
            part['lines'].append([part['who'].index(who),txt,who])
    else:
        cur['parts'].append({'label':'','lines':[[0,clean(p)]]})
assert len(cards)==10,[c['title'] for c in cards]
for i,c in enumerate(cards):
    c['group']='practice' if i<4 else 'mock'
    c['id']=('p%d'%(i+1)) if i<4 else ('a%d'%(i-3))
    for p in c['parts']: p.pop('who',None)
data=json.dumps(cards,ensure_ascii=False)
open('/home/claude/scripts/listening.json','w').write(json.dumps(cards,ensure_ascii=False,indent=1))

tpl=open(R+'junior-cycle-spanish-no-spanish-at-school.html',encoding='utf-8').read()
head=tpl[:tpl.index('<main id="main">')]
head=re.sub(r'<title>.*?</title>','<title>Exam Pack listening: play the Junior Cycle Spanish practice audio | Léim</title>',head)
head=re.sub(r'<meta name="description" content=".*?">','<meta name="description" content="The listening for the Léim Junior Cycle Spanish Exam Pack: play every practice set and mock-paper question in Spanish, twice, with exam-style pauses.">\n<meta name="robots" content="noindex">',head)
extra_css='''
.li-card{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:14px 0}
.li-card h3{margin:0 0 4px!important;font-size:20px}
.li-card .meta{font-size:15px;color:var(--ink-2);margin-bottom:12px}
.li-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}
.li-row .lab{font-weight:700;min-width:70px;font-size:15px}
.li-btn{font:inherit;font-weight:700;font-size:15px;border-radius:999px;padding:9px 16px;border:2px solid var(--green);background:var(--green);color:#fff;cursor:pointer}
.li-btn.ghost{background:#fff;color:var(--green)}
.li-btn:disabled{opacity:.45;cursor:not-allowed}
.li-status{font-size:15px;font-weight:600;color:var(--green);min-height:22px;margin-top:6px}
.li-status.wait{color:#8a5a00}
.li-script{display:none;background:var(--cream);border:1px solid var(--cream-line);border-radius:10px;padding:12px 14px;margin-top:10px;font-size:15px;line-height:1.55}
.li-script.open{display:block}
.li-script p{margin:0 0 6px!important;font-size:15px!important}
.li-set{display:flex;flex-wrap:wrap;gap:14px;align-items:center;background:var(--cream);border:1px solid var(--cream-line);border-radius:12px;padding:12px 16px;margin:16px 0;font-size:16px}
.li-set select{font:inherit;padding:6px 8px;border-radius:8px;border:1px solid var(--line)}
.li-warn{display:none;background:#fdecea;border:1px solid #f3b8b0;border-radius:12px;padding:14px 16px;margin:14px 0;font-size:16px}
.li-warn.show{display:block}
.li-card.playing{border-color:var(--green);box-shadow:0 0 0 3px rgba(46,125,87,.15)}
'''
head=head.replace('</style>',extra_css+'</style>')
main='''<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <span class="pill">Junior Cycle Spanish · Exam Pack</span>
      <h1>Exam Pack <span class="hl">listening</span></h1>
      <p class="lede">Press play and your device reads each listening item aloud in Spanish, <b>twice</b>, with a pause in between, like the real exam. Use it with Part 3 (pages 15–16) and the mock paper Section A (pages 17–18) of the Léim Exam Pack.</p>
      <div class="toc"><a href="#practice">Practice sets 1–4</a><a href="#mock">Mock paper A1–A6</a><a href="#help">No sound?</a></div>
    </div>
  </div>
</section>

<div class="block"><div class="wrap ec">
    <div id="liWarn" class="li-warn"><b>No Spanish voice found on this device.</b> Try Chrome, Safari or Edge, or a phone or tablet. On a computer you may need to add a Spanish voice (see <a href="#help">No sound?</a>). The scripts are also at the back of the Exam Pack for an adult to read aloud.</div>
    <div class="li-set">
      <label>Pause between the two readings:
        <select id="liPause"><option value="30">30 seconds (exam style)</option><option value="20">20 seconds</option><option value="10">10 seconds</option><option value="0">No pause</option></select>
      </label>
      <label>Speed:
        <select id="liRate"><option value="0.95">Normal</option><option value="0.8">A bit slower</option><option value="0.68">Slow (for learning)</option></select>
      </label>
      <button class="li-btn ghost" id="liStop" type="button">■ Stop</button>
    </div>
    <p>How to use it: read the questions in the pack first (30 seconds), press <b>▶ Play twice</b>, and write your answers. Keep the script closed until you have checked your answers with the answer key. The voice is your device's built-in Spanish voice, so it can sound a little robotic, and it may differ from phone to phone.</p>

    <section id="practice">
      <h2>Part 3: Practice sets 1–4</h2>
      <div id="liPractice"></div>
    </section>

    <section id="mock">
      <h2>Mock paper: Section A (Listening, 140 marks)</h2>
      <p>Do these in one go, with the timer, after the student has had 30 seconds to read each question. No scripts until the end.</p>
      <div id="liMock"></div>
    </section>

    <section id="help">
      <h2>No sound?</h2>
      <ul>
        <li>Turn the volume up and check the phone isn't on silent (on an iPhone, flick the switch on the side).</li>
        <li>Use <b>Chrome, Safari or Edge</b>. Some other browsers have no Spanish voice.</li>
        <li><b>iPhone / iPad:</b> Settings → Accessibility → Spoken Content → Voices → Spanish, and download a Spain voice (e.g. Mónica).</li>
        <li><b>Mac:</b> System Settings → Accessibility → Spoken Content → System voice → Manage Voices → Spanish (Spain).</li>
        <li><b>Windows:</b> Settings → Time &amp; language → Speech → Add voices → Spanish (Spain).</li>
        <li><b>Android:</b> Settings → Accessibility → Text-to-speech → Google speech engine → Install voice data → Spanish (Spain).</li>
        <li>Still nothing? The scripts are at the back of the Exam Pack (pages 28–31): a parent or friend can read them aloud.</li>
      </ul>
      <div class="note"><b>About this audio:</b> all texts were written by Léim in the style of the Junior Cycle exam. It is not official exam material. Léim is independent and not connected to the State Examinations Commission or the NCCA. The real past papers and their audio are free on <b>examinations.ie</b>. Don't have the Exam Pack yet? <a href="https://payhip.com/b/IAjDY">Get it here (€10)</a>.</div>
    </section>
</div></div>

</main>
'''
foot=tpl[tpl.index('</main>')+len('</main>'):]
script='''<script>
(function(){
var DATA=__DATA__;
var $=function(id){return document.getElementById(id);};
var synth=window.speechSynthesis,voices=[],run=0,cardEl=null;
function esc(s){return s.replace(/[&<>]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;"}[c];});}
function findVoices(){
  if(!synth){$("liWarn").classList.add("show");return;}
  var v=synth.getVoices()||[];
  var bad=/eddy|flo\b|grandma|grandpa|reed|rocko|sandy|shelley|bells|bubbles|jester|organ|superstar|trinoids|whisper|wobble|zarvox|albert|bad news|good news|boing|cellos|fred|junior|kathy|ralph/i;
  var good=/m[oó]nica|jorge|marisol|google|microsoft|elvira|[aá]lvaro|helena|pablo|laura|lucia|luc[ií]a|enrique|conchita|dar[ií]o|paulina|juan|diego|isabela/i;
  function score(x){return (/^es[-_]ES/i.test(x.lang)?4:0)+(good.test(x.name)?2:0)+(x.localService===false?0:0)-(bad.test(x.name)?10:0);}
  var es=v.filter(function(x){return /^es/i.test(x.lang);}).sort(function(a,b){return score(b)-score(a);});
  var ok=es.filter(function(x){return !bad.test(x.name);});if(ok.length)es=ok;
  voices=es.slice(0,2);
  $("liWarn").classList.toggle("show",!voices.length&&v.length>0);
}
if(synth){findVoices();synth.onvoiceschanged=findVoices;setTimeout(function(){findVoices();if(!voices.length)$("liWarn").classList.add("show");},1500);}else findVoices();
function sentences(t){return t.match(/[^.!?…]+[.!?…]+[»"]?|[^.!?…]+$/g).map(function(s){return s.trim();}).filter(Boolean);}
function say(text,who,my){return new Promise(function(res){
  if(my!==run||!synth||!voices.length)return res();
  var u=new SpeechSynthesisUtterance(text);var v=voices[who%voices.length];
  u.voice=v;u.lang=v?v.lang:"es-ES";u.rate=parseFloat($("liRate").value);
  u.pitch=(voices.length<2&&who===1)?1.35:1;
  var done=false;function fin(){if(!done){done=true;res();}}
  u.onend=fin;u.onerror=fin;synth.speak(u);
  setTimeout(fin,Math.max(8000,text.length*220));
});}
function wait(sec,my,st,msg){return new Promise(function(res){
  var left=sec;if(left<=0)return res();
  st.className="li-status wait";
  (function tick(){if(my!==run)return res();st.textContent=msg+" "+left+"s";if(left--<=0)return res();setTimeout(tick,1000);})();
});}
async function speakPart(part,my){
  for(var i=0;i<part.lines.length;i++){
    var L=part.lines[i],ss=sentences(L[1]);
    for(var j=0;j<ss.length;j++){if(my!==run)return;await say(ss[j],L[0],my);}
    await new Promise(function(r){setTimeout(r,350);});
  }
}
function stop(){run++;if(synth)synth.cancel();if(cardEl){cardEl.classList.remove("playing");cardEl=null;}
  document.querySelectorAll(".li-status").forEach(function(s){if(s.dataset.busy){s.textContent="Stopped.";s.className="li-status";delete s.dataset.busy;}});}
async function play(card,parts,twice,el,st){
  stop();if(!voices.length){$("liWarn").classList.add("show");return;}
  var my=++run;cardEl=el;el.classList.add("playing");st.dataset.busy=1;
  var pause=parseInt($("liPause").value,10);
  for(var k=0;k<parts.length;k++){
    var lab=parts[k].label?parts[k].label+": ":"";
    st.className="li-status";st.textContent="▶ "+lab+"first reading…";
    await speakPart(parts[k],my);if(my!==run)return;
    if(twice){
      await wait(pause,my,st,lab+"second reading in");if(my!==run)return;
      st.className="li-status";st.textContent="▶ "+lab+"second reading…";
      await speakPart(parts[k],my);if(my!==run)return;
    }
    if(k<parts.length-1){await wait(Math.min(pause,15)||3,my,st,"Next item in");if(my!==run)return;}
  }
  st.className="li-status";st.textContent="✓ Finished. Write your answers, then check them with the answer key.";delete st.dataset.busy;
  el.classList.remove("playing");cardEl=null;
}
function render(c){
  var el=document.createElement("div");el.className="li-card";el.id=c.id;
  var n=c.parts.length;
  var h='<h3>'+esc(c.title)+'</h3><div class="meta">'+(n>1?n+" short items, each played twice":"Played twice")+'</div>';
  h+='<div class="li-row"><button class="li-btn" data-a="all2" type="button">▶ Play twice</button><button class="li-btn ghost" data-a="all1" type="button">▶ Once</button></div>';
  if(n>1){c.parts.forEach(function(p,i){h+='<div class="li-row"><span class="lab">'+esc(p.label)+'</span><button class="li-btn ghost" data-a="p2" data-i="'+i+'" type="button">▶ Twice</button><button class="li-btn ghost" data-a="p1" data-i="'+i+'" type="button">▶ Once</button></div>';});}
  h+='<div class="li-status" aria-live="polite"></div>';
  h+='<div class="li-row"><button class="li-btn ghost" data-a="script" type="button">Show the script</button></div><div class="li-script">';
  c.parts.forEach(function(p){
    if(p.label)h+='<p><b>'+esc(p.label)+'</b></p>';
    p.lines.forEach(function(L){h+='<p>'+(L[2]?'<b>'+esc(L[2])+':</b> ':(p.lines.length>1?'— ':''))+esc(L[1])+'</p>';});
  });
  h+='</div>';el.innerHTML=h;
  var st=el.querySelector(".li-status");
  el.addEventListener("click",function(e){
    var b=e.target.closest("button");if(!b)return;var a=b.dataset.a;
    if(a==="script"){var s=el.querySelector(".li-script");
      if(!s.classList.contains("open")&&c.group==="mock"&&!b.dataset.sure){b.dataset.sure=1;b.textContent="Finished the questions? Tap again to show the answers";return;}delete b.dataset.sure;
      s.classList.toggle("open");b.textContent=s.classList.contains("open")?"Hide the script":"Show the script";return;}
    if(a==="all2"||a==="all1")play(c,c.parts,a==="all2",el,st);
    else play(c,[c.parts[+b.dataset.i]],a==="p2",el,st);
  });
  return el;
}
DATA.forEach(function(c){$(c.group==="practice"?"liPractice":"liMock").appendChild(render(c));});
$("liStop").addEventListener("click",stop);
window.addEventListener("pagehide",stop);
})();
</script>
'''.replace('__DATA__',data)
foot=foot.replace('<script src="site.js"></script>',script+'<script src="site.js"></script>')
open(R+'junior-cycle-spanish-exam-pack-listening.html','w',encoding='utf-8').write(head+main+foot)
print('ok',[ (c['id'],c['title'],len(c['parts'])) for c in cards])
