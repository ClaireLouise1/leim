/* Léim Arcade mode: answers fall from the sky as bubbles — tap the right one before it lands.
   Works on any Léim game that exposes window.__leimTest = {MAKERS: {mode: [makerFn, …]}}
   (every JC Maths game). Uses window.LeimFun (fun.js) for sounds, confetti and saving, if present.
   Load after the game script and fun.js: <script src="arcade.js"></script> */
(function(){
  var T=window.__leimTest,startP=document.getElementById("start"),playP=document.getElementById("play");
  if(!T||!T.MAKERS||!startP||!playP)return;
  var MAKERS=T.MAKERS,F=function(){return window.LeimFun||null;};
  function snd(n,a){var f=F();if(f&&f.snd&&f.snd[n])f.snd[n](a);}
  function rnd(a){return a[Math.floor(Math.random()*a.length)];}
  function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t;}return a;}
  function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;");}
  var STYLE_KEY="leimStyle",style="arcade";
  try{style=localStorage.getItem(STYLE_KEY)||"arcade";}catch(e){}

  /* ---------- styles ---------- */
  var css=[
  ".arc-style{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0 4px}",
  ".arc-style button{font:inherit;font-weight:800;font-size:16px;padding:12px 8px;border-radius:14px;border:2px solid var(--line,#E5E7EB);background:#fff;color:var(--ink,#1B2430);cursor:pointer;box-shadow:0 4px 0 var(--line,#E5E7EB)}",
  ".arc-style button small{display:block;font-weight:600;font-size:12.5px;color:var(--muted,#5B6470)}",
  ".arc-style button.on{border-color:#1CB0F6;background:#DDF4FF;box-shadow:0 4px 0 #1899D6}",
  ".arc-style button:active{transform:translateY(3px);box-shadow:0 1px 0 var(--line,#E5E7EB)}",
  "#arcade{padding:0;overflow:hidden;border:0;background:#141C2B;color:#fff;border-radius:20px;position:relative;user-select:none;-webkit-user-select:none;touch-action:manipulation}",
  ".arc-hud{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:12px 14px;font-weight:900;font-size:16px;background:#0E1522}",
  ".arc-hud .lv{background:#FF9600;border-radius:999px;padding:3px 12px;box-shadow:0 3px 0 #C46F00}",
  ".arc-hud .sc{color:#FFD43B;font-size:20px;min-width:60px;text-align:right}",
  ".arc-hud .x{background:none;border:0;color:#8FA0B8;font-size:22px;cursor:pointer;padding:0 2px;line-height:1}",
  ".arc-hearts{font-size:19px;letter-spacing:1px;white-space:nowrap}.arc-hearts .gone{filter:grayscale(1);opacity:.25}",
  ".arc-q{background:#fff;color:var(--ink,#1B2430);margin:10px 12px 0;border-radius:16px;padding:12px 14px;text-align:center;box-shadow:0 5px 0 #C9D3E1;position:relative;z-index:3;transition:background .2s}",
  ".arc-q .en{font-size:15px;color:var(--muted,#5B6470);font-weight:700}",
  ".arc-q .frame{font-size:clamp(20px,5.4vw,28px);font-weight:900;line-height:1.25;margin-top:4px}",
  ".arc-q .frame.long{font-size:clamp(16px,4.4vw,21px)}",
  ".arc-q svg{display:block;margin:6px auto 0;max-width:100%;height:auto;max-height:150px}",
  ".arc-q table{min-width:0!important;width:auto!important;margin:6px auto;font-size:14px}",
  ".arc-q.ok{background:#D7FFB8}.arc-q.bad{background:#FFDFE0}",
  ".arc-why{font-size:14px;font-weight:700;color:#C0392B;margin-top:6px;min-height:0}",
  ".arc-sky{position:relative;height:clamp(300px,48vh,430px);margin-top:-14px;overflow:hidden;",
  "background:radial-gradient(2px 2px at 12% 22%,#fff8,transparent),radial-gradient(1.5px 1.5px at 72% 12%,#fff9,transparent),radial-gradient(2px 2px at 40% 64%,#fff6,transparent),radial-gradient(1.5px 1.5px at 88% 52%,#fff8,transparent),radial-gradient(1.5px 1.5px at 24% 82%,#fff6,transparent),radial-gradient(2px 2px at 58% 36%,#fff7,transparent),linear-gradient(#1D2B47,#2A3F66 70%,#3B5A8C)}",
  ".arc-ground{position:absolute;left:0;right:0;bottom:0;height:34px;background:linear-gradient(#58CC02,#46A302);box-shadow:inset 0 4px 0 #89E219;z-index:2}",
  ".arc-ground.hit{animation:arcHit .5s}",
  ".arc-b{position:absolute;top:0;left:0;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;color:#1B2430;border-radius:999px;border:3px solid #fff;cursor:pointer;padding:6px 10px;line-height:1.15;will-change:transform;z-index:1;box-shadow:0 5px 0 rgba(0,0,0,.25),inset 0 -6px 0 rgba(0,0,0,.08),inset 0 5px 0 rgba(255,255,255,.45)}",
  ".arc-b.c0{background:#FFD43B}.arc-b.c1{background:#7DE3FF}.arc-b.c2{background:#FF9EC7}.arc-b.c3{background:#B6F36B}",
  ".arc-b.no{background:#FF6B6B!important;color:#fff;animation:arcShake .35s}",
  ".arc-b.yes{background:#58CC02!important;color:#fff}",
  ".arc-b.pop{animation:arcPop .35s forwards;pointer-events:none}",
  ".arc-b.fade{transition:opacity .3s;opacity:0;pointer-events:none}",
  ".arc-p{position:absolute;width:9px;height:9px;border-radius:50%;pointer-events:none;z-index:4}",
  ".arc-pts{position:absolute;font-weight:900;font-size:24px;color:#FFD43B;text-shadow:0 2px 0 #0008;pointer-events:none;z-index:5;animation:arcUp .9s forwards}",
  ".arc-ban{position:absolute;left:50%;top:40%;transform:translate(-50%,-50%);background:#FF9600;color:#fff;font-weight:900;font-size:clamp(22px,7vw,34px);padding:10px 22px;border-radius:18px;box-shadow:0 6px 0 #C46F00;z-index:6;white-space:nowrap;pointer-events:none;animation:arcBan 1.4s forwards}",
  ".arc-ready{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:64px;font-weight:900;color:#fff;text-shadow:0 5px 0 #0006;z-index:6;pointer-events:none}",
  ".arc-over{position:absolute;inset:0;background:#0E1522;z-index:8;overflow:auto;padding:22px 18px;text-align:center}",
  ".arc-over h2{color:#fff;font-size:clamp(26px,7vw,36px);margin:4px 0}",
  ".arc-over .st{font-size:52px;letter-spacing:6px;margin:6px 0}.arc-over .st span{color:#3A4555;display:inline-block}.arc-over .st span.on{color:#FFD43B;text-shadow:0 3px 0 #C99400;animation:arcStar .5s both}",
  ".arc-over .ch{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:8px 0}",
  ".arc-over .ch div{background:#1F2B40;border-radius:14px;padding:8px 12px;min-width:84px}.arc-over .ch b{display:block;font-size:22px}.arc-over .ch span{font-size:12.5px;color:#9FB0C8;font-weight:700}",
  ".arc-over .nb{display:inline-block;background:#FFD43B;color:#1B2430;font-weight:900;border-radius:999px;padding:4px 12px;margin:4px}",
  ".arc-over .rv{text-align:left;background:#fff;color:var(--ink,#1B2430);border-radius:14px;padding:12px 14px;margin:12px 0;font-size:15px}",
  ".arc-over .rv li{margin:6px 0}.arc-over .rv .w{color:var(--muted,#5B6470);font-size:13.5px}",
  ".arc-over .bt{display:grid;gap:10px;margin-top:10px}",
  ".arc-over .bt button{font:inherit;font-weight:900;font-size:17px;padding:14px;border-radius:14px;border:0;cursor:pointer}",
  ".arc-over .go1{background:#58CC02;color:#fff;box-shadow:0 5px 0 #46A302}.arc-over .go2{background:#2A3A55;color:#fff;box-shadow:0 5px 0 #18233A}",
  "@keyframes arcPop{0%{transform:var(--t) scale(1)}50%{transform:var(--t) scale(1.35)}100%{transform:var(--t) scale(1.6);opacity:0}}",
  "@keyframes arcShake{0%,100%{margin-left:0}25%{margin-left:-8px}75%{margin-left:8px}}",
  "@keyframes arcUp{from{opacity:1;transform:translateY(0)}to{opacity:0;transform:translateY(-60px)}}",
  "@keyframes arcBan{0%{opacity:0;transform:translate(-50%,-50%) scale(.4)}15%{opacity:1;transform:translate(-50%,-50%) scale(1.12)}25%{transform:translate(-50%,-50%) scale(1)}80%{opacity:1}100%{opacity:0}}",
  "@keyframes arcHit{0%,100%{filter:none}30%{filter:brightness(1.6) hue-rotate(-90deg)}}",
  "@keyframes arcStar{0%{transform:scale(0) rotate(-40deg)}70%{transform:scale(1.3)}100%{transform:scale(1)}}"
  ].join("\n");
  var st=document.createElement("style");st.textContent=css;document.head.appendChild(st);

  /* ---------- play-style switch on the start screen ---------- */
  var modesBox=startP.querySelector(".modes");
  var sw=document.createElement("div");sw.className="arc-style";
  sw.innerHTML="<button type='button' data-s='arcade'>🚀 Arcade<small>Catch the falling answers</small></button>"+
               "<button type='button' data-s='classic'>⏱️ Classic<small>60-second quiz</small></button>";
  if(modesBox)modesBox.parentNode.insertBefore(sw,modesBox);else startP.appendChild(sw);
  function drawSw(){[].forEach.call(sw.children,function(b){b.classList.toggle("on",b.dataset.s===style);});}
  [].forEach.call(sw.children,function(b){b.onclick=function(){style=b.dataset.s;try{localStorage.setItem(STYLE_KEY,style);}catch(e){}drawSw();};});
  drawSw();
  [].forEach.call(document.querySelectorAll(".mode"),function(b){
    b.addEventListener("click",function(e){
      if(style!=="arcade"||!MAKERS[b.dataset.mode])return;
      e.stopImmediatePropagation();e.preventDefault();begin(b.dataset.mode);
    },true);
  });

  /* ---------- the arcade panel ---------- */
  var P=document.createElement("div");P.className="panel";P.id="arcade";P.hidden=true;
  P.innerHTML="<div class='arc-hud'><span class='arc-hearts'></span><span class='lv'>Level 1</span><span class='sc'>0</span><button class='x' type='button' aria-label='Stop'>✕</button></div>"+
    "<div class='arc-q' aria-live='polite'><div class='en'></div><div class='frame'></div><div class='arc-why'></div></div>"+
    "<div class='arc-sky'><div class='arc-ground'></div></div>";
  playP.parentNode.insertBefore(P,playP.nextSibling);
  var $=function(s){return P.querySelector(s);};
  var sky=$(".arc-sky"),ground=$(".arc-ground"),qBox=$(".arc-q");
  $(".x").onclick=function(){stop();showStart();};

  var MAXH=3,mode,hearts,score,level,right,asked,combo,bestCombo,mistakes,bubbles,cur,last,running,raf,lastT,busy,fallTime;
  function showStart(){P.hidden=true;startP.hidden=false;startP.scrollIntoView({behavior:"smooth",block:"start"});}
  function drawHud(){
    var h="";for(var i=0;i<MAXH;i++)h+="<span class='"+(i<hearts?"":"gone")+"'>❤️</span>";
    $(".arc-hearts").innerHTML=h;$(".lv").textContent="Level "+level;$(".sc").textContent=score;
  }
  function begin(m){
    mode=m;hearts=MAXH;score=0;level=1;right=0;asked=0;combo=0;bestCombo=0;mistakes=[];bubbles=[];last="";busy=false;
    fallTime=9.5;
    var ov=P.querySelector(".arc-over");if(ov)ov.remove();
    startP.hidden=true;playP.hidden=true;var e=document.getElementById("end");if(e)e.hidden=true;
    P.hidden=false;drawHud();
    P.scrollIntoView({behavior:"smooth",block:"start"});
    var r=document.createElement("div");r.className="arc-ready";sky.appendChild(r);
    var n=3;(function tick(){if(n>0){r.textContent=n;snd("star",3-n);n--;setTimeout(tick,600);}else{r.textContent="Go!";snd("combo");setTimeout(function(){r.remove();},450);next();run();}})();
  }
  function stop(){running=false;cancelAnimationFrame(raf);clearBubbles();}
  function clearBubbles(){bubbles.forEach(function(b){b.el.remove();});bubbles=[];}

  function next(){
    clearBubbles();busy=false;
    var list=MAKERS[mode],q,tries=0;
    do{q=rnd(list)();tries++;}while((q.review===last||!q.wrong||q.wrong.length<2)&&tries<25);
    last=q.review;cur=q;asked++;
    qBox.classList.remove("ok","bad");$(".arc-why").textContent="";
    $(".en").textContent=q.en||"";
    var fr=$(".frame"),txt=esc(q.frame||""),html=q.html||"";
    fr.innerHTML=(q.data&&q.data.after)?txt+html:html+txt;
    fr.className="frame"+(q.frame&&q.frame.length>24?" long":"");
    var opts=shuffle([q.answer].concat(q.wrong.slice(0,3)));
    var W=sky.clientWidth,maxLen=Math.max.apply(null,opts.map(function(o){return String(o).length;}));
    var lanes=maxLen<=8?opts.length:maxLen<=18?2:1;
    var bw=lanes===1?W*0.86:lanes===2?W*0.44:Math.min(W/opts.length-10,110);
    var fs=maxLen<=5?22:maxLen<=8?18:maxLen<=18?16:14.5;
    var gap=lanes===opts.length?55:lanes===2?95:78;
    var order=shuffle(opts.map(function(_,i){return i;}));
    opts.forEach(function(o,i){
      var el=document.createElement("button");el.type="button";el.className="arc-b c"+(i%4);
      el.textContent=o;el.style.width=bw+"px";el.style.fontSize=fs+"px";el.style.minHeight=(lanes===opts.length?Math.min(bw,70):52)+"px";
      sky.appendChild(el);
      var lane=lanes===opts.length?i:(i%lanes),laneW=W/lanes;
      var x=lane*laneW+(laneW-bw)/2+(lanes===1?0:(Math.random()-.5)*Math.max(0,laneW-bw-8));
      var b={el:el,text:o,x:x,y:-el.offsetHeight-20-order[i]*gap,h:el.offsetHeight,dead:false};
      el.addEventListener("pointerdown",function(ev){ev.preventDefault();tap(b);});
      place(b);bubbles.push(b);
    });
  }
  function place(b){var t="translate("+b.x+"px,"+b.y+"px)";b.el.style.setProperty("--t",t);b.el.style.transform=t;}

  function run(){running=true;lastT=performance.now();raf=requestAnimationFrame(loop);}
  function loop(t){
    if(!running)return;
    var dt=Math.min(.05,(t-lastT)/1000);lastT=t;
    if(!busy){
      var H=sky.clientHeight-34,v=H/fallTime;
      bubbles.forEach(function(b){
        if(b.dead)return;b.y+=v*dt;place(b);
        if(b.y+b.h>=H){b.dead=true;
          if(b.text===cur.answer)missed(b);else{b.el.classList.add("fade");}
        }
      });
    }
    raf=requestAnimationFrame(loop);
  }
  function burst(b,colour){
    var cx=b.x+b.el.offsetWidth/2,cy=b.y+b.h/2;
    for(var i=0;i<16;i++){var p=document.createElement("div");p.className="arc-p";p.style.background=rnd(["#FFD43B","#58CC02","#7DE3FF","#FF9EC7","#fff"]);
      sky.appendChild(p);var a=Math.random()*Math.PI*2,d=40+Math.random()*60;
      p.animate([{transform:"translate("+cx+"px,"+cy+"px) scale(1)",opacity:1},{transform:"translate("+(cx+Math.cos(a)*d)+"px,"+(cy+Math.sin(a)*d)+"px) scale(.3)",opacity:0}],{duration:600,easing:"cubic-bezier(.2,.7,.3,1)"});
      setTimeout(function(p){return function(){p.remove();};}(p),620);}
    var pts=document.createElement("div");pts.className="arc-pts";pts.textContent=colour;pts.style.left=(cx-24)+"px";pts.style.top=(cy-30)+"px";sky.appendChild(pts);setTimeout(function(){pts.remove();},950);
  }
  function banner(t){var b=document.createElement("div");b.className="arc-ban";b.textContent=t;sky.appendChild(b);setTimeout(function(){b.remove();},1450);}
  function tap(b){
    if(busy||b.dead||!running)return;
    if(b.text===cur.answer){
      busy=true;b.dead=true;right++;combo++;if(combo>bestCombo)bestCombo=combo;
      var pts=10*level+(combo>=3?5*Math.min(combo,10):0);score+=pts;
      b.el.classList.add("yes","pop");burst(b,"+"+pts);snd("right");qBox.classList.add("ok");
      bubbles.forEach(function(o){if(o!==b){o.dead=true;o.el.classList.add("fade");}});
      if(combo===3||combo===5||combo===10||combo===15){setTimeout(function(){snd("combo");},100);banner("🔥 "+combo+" in a row!");}
      if(right%5===0){level++;fallTime=Math.max(4.2,fallTime*0.86);setTimeout(function(){snd("win");banner("⬆️ Level "+level+"!");},combo%5===0&&COMBOAT(combo)?700:150);}
      drawHud();setTimeout(next,650);
    }else{
      b.dead=true;b.el.classList.add("no");snd("wrong");var f=F();if(f)f.buzz(100);
      combo=0;mistakes.push({review:cur.review,said:b.text,why:cur.why||""});
      setTimeout(function(){b.el.classList.add("fade");},350);
      lose();
    }
  }
  function COMBOAT(c){return c===5||c===10||c===15;}
  function missed(b){
    busy=true;combo=0;mistakes.push({review:cur.review,said:"(missed it)",why:cur.why||""});
    b.el.classList.add("yes");ground.classList.remove("hit");void ground.offsetWidth;ground.classList.add("hit");
    qBox.classList.add("bad");$(".arc-why").textContent="It was "+cur.answer+(cur.why?". "+cur.why:"");
    snd("heart");lose(true);
  }
  function lose(fromMiss){
    hearts--;drawHud();
    if(!fromMiss&&cur.why){$(".arc-why").textContent=cur.why;}
    if(hearts<=0){busy=true;setTimeout(over,fromMiss?1400:900);return;}
    if(fromMiss)setTimeout(next,2200);
  }
  function over(){
    stop();
    var stars=right>=15?3:right>=8?2:right>=1?1:0;
    var f=F(),res=f?f.award({key:"arcade-"+mode,right:right,stars:stars,xp:score}):{isBest:false,newDay:false};
    var acc=asked?Math.round(right/Math.max(1,right+mistakes.length)*100):0;
    var seen={},rv="";
    mistakes.forEach(function(m){if(seen[m.review])return;seen[m.review]=1;rv+="<li><b>"+esc(m.review)+"</b>"+(m.why?"<br><span class='w'>"+esc(m.why)+"</span>":"")+"</li>";});
    var o=document.createElement("div");o.className="arc-over";
    o.innerHTML="<h2>"+(stars===3?"Legendary! 🏆":stars===2?"Brilliant! 🎉":stars===1?"Good run! 💪":"Have another go! 💪")+"</h2>"+
      "<div class='st'>"+[1,2,3].map(function(n,i){return "<span class='"+(n<=stars?"on":"")+"' style='animation-delay:"+(.2+i*.3)+"s'>★</span>";}).join("")+"</div>"+
      "<div class='ch'><div><b>"+score+"</b><span>points</span></div><div><b>"+right+"</b><span>caught</span></div><div><b>"+level+"</b><span>level</span></div><div><b>🔥 "+bestCombo+"</b><span>best combo</span></div></div>"+
      (res.isBest?"<span class='nb'>🏅 New personal best!</span>":"")+(res.newDay?"<span class='nb'>🔥 "+res.streak+"-day streak!</span>":"")+
      "<p style='color:#9FB0C8;font-size:14px;margin:6px 0'>"+(stars<3?"Catch 15 for 3 stars.":"All 3 stars!")+"</p>"+
      (rv?"<div class='rv'><b>Go back over these</b><ul style='margin:6px 0 0;padding-left:18px'>"+rv+"</ul></div>":"")+
      "<div class='bt'><button class='go1' type='button'>Play again</button><button class='go2' type='button'>Choose another level</button></div>";
    P.appendChild(o);
    o.querySelector(".go1").onclick=function(){begin(mode);};
    o.querySelector(".go2").onclick=function(){o.remove();showStart();};
    snd(stars>=2?"win":"heart");if(stars>=2&&f)setTimeout(f.confetti,500);
  }
  window.__leimArcade={begin:begin,state:function(){return {hearts:hearts,score:score,level:level,right:right,cur:cur,bubbles:bubbles};}};
})();
