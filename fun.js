/* Léim "fun layer": sounds, hearts, combos, stars, XP and a daily streak for any
   Léim game that uses the standard #start / #play / #end panels and .choice buttons.
   Add <script src="fun.js"></script> after the game script. Optional: the game can
   expose window.__leimFinish = finish so running out of hearts ends the round. */
(function(){
  var $=function(id){return document.getElementById(id);};
  var play=$("play"),end=$("end"),startP=$("start"),box=$("choices");
  if(!play||!end||!box)return;

  /* ---------- saved progress (this device only, no sign-up) ---------- */
  var KEY="leimFun",S={};
  try{S=JSON.parse(localStorage.getItem(KEY)||"{}")||{};}catch(e){S={};}
  S.xp=S.xp||0;S.best=S.best||{};S.day=S.day||{last:"",count:0};
  function save(){try{localStorage.setItem(KEY,JSON.stringify(S));}catch(e){}}
  var PAGE=location.pathname.replace(/^.*\//,"").replace(/(-test)?\.html$/,"")||"game";
  function today(d){d=d||new Date();return d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate();}
  function bumpDay(){
    var t=today();if(S.day.last===t)return false;
    var y=new Date();y.setDate(y.getDate()-1);
    S.day.count=(S.day.last===today(y))?S.day.count+1:1;S.day.last=t;return true;
  }
  function streakNow(){var y=new Date();y.setDate(y.getDate()-1);return (S.day.last===today()||S.day.last===today(y))?S.day.count:0;}

  /* ---------- styles ---------- */
  var css=[
  ".fun-top{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:0 0 6px}",
  ".fun-pill{display:inline-flex;align-items:center;gap:6px;background:var(--cream,#FFF7DC);border:1px solid var(--cream-line,#F3E3A8);border-radius:999px;padding:6px 14px;font-weight:800;font-size:15px}",
  ".fun-stars{font-size:15px;letter-spacing:2px;color:#D8DCE1;white-space:nowrap;margin-left:auto;margin-right:8px}",
  ".fun-stars .on{color:#F2B705}",
  ".mode{transition:transform .12s}.mode:active{transform:scale(.97)}",
  ".fun-row{display:flex;justify-content:space-between;align-items:center;margin:-8px 0 10px}",
  ".fun-hearts{font-size:20px;letter-spacing:2px;white-space:nowrap}",
  ".fun-hearts .gone{filter:grayscale(1);opacity:.3;display:inline-block;animation:funDrop .5s}",
  ".fun-mute{background:none;border:0;font-size:20px;cursor:pointer;padding:0 4px;line-height:1}",
  ".hud .streak{transition:transform .2s}",
  ".fun-hot .hud .streak{color:#E8590C;transform:scale(1.15)}",
  "#play{position:relative;overflow:hidden;transition:box-shadow .3s}",
  "#play.fun-ok{box-shadow:0 0 0 4px #58CC8A,0 6px 24px rgba(27,36,48,.06)}",
  "#play.fun-bad{box-shadow:0 0 0 4px #E5534B,0 6px 24px rgba(27,36,48,.06)}",
  ".fun-shake{animation:funShake .4s}",
  ".choice{transition:transform .12s,background .15s,border-color .15s;box-shadow:0 4px 0 var(--line,#E5E7EB)}",
  ".choice:active{transform:translateY(3px);box-shadow:0 1px 0 var(--line,#E5E7EB)}",
  ".choice.right{box-shadow:0 4px 0 var(--green,#2E7D57);animation:funPop .35s}",
  ".choice.wrong{box-shadow:0 4px 0 #D9534F}",
  ".fun-in .choice{animation:funIn .28s both}",
  ".fun-in .choice:nth-child(2){animation-delay:.04s}.fun-in .choice:nth-child(3){animation-delay:.08s}.fun-in .choice:nth-child(4){animation-delay:.12s}",
  ".fun-in .frame{animation:funIn .25s both}",
  ".fun-float{position:absolute;pointer-events:none;font-weight:900;color:var(--green,#2E7D57);font-size:22px;animation:funFloat .9s forwards;z-index:5}",
  ".fun-banner{position:absolute;left:50%;top:10px;transform:translate(-50%,0);background:#FF9600;color:#fff;font-weight:900;font-size:clamp(18px,5vw,26px);padding:8px 18px;border-radius:16px;box-shadow:0 6px 0 #D97F00;pointer-events:none;z-index:6;animation:funBanner 1.2s forwards;white-space:nowrap}",
  ".fun-reward{text-align:center;margin-bottom:10px}",
  ".fun-reward h2{font-size:clamp(24px,6vw,32px);margin:0 0 6px}",
  ".fun-bigstars{font-size:54px;letter-spacing:6px;line-height:1.1;margin:4px 0 10px}",
  ".fun-bigstars span{display:inline-block;color:#D8DCE1;transform:scale(0)}",
  ".fun-bigstars span.on{color:#F2B705;text-shadow:0 3px 0 #C99400}",
  ".fun-bigstars span.show{animation:funStar .45s forwards}",
  ".fun-chips{display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin:10px 0 4px}",
  ".fun-chip{border:2px solid var(--line,#E5E7EB);border-radius:14px;padding:8px 14px;min-width:86px}",
  ".fun-chip b{display:block;font-size:22px}.fun-chip span{font-size:13px;color:var(--muted,#5B6470);font-weight:700}",
  ".fun-new{display:inline-block;background:#F2B705;color:#1B2430;font-weight:900;border-radius:999px;padding:4px 12px;margin-top:8px;animation:funPop .5s}",
  "#funConfetti{position:fixed;inset:0;pointer-events:none;z-index:9999}",
  "@keyframes funPop{0%{transform:scale(1)}40%{transform:scale(1.08)}100%{transform:scale(1)}}",
  "@keyframes funShake{0%,100%{transform:translateX(0)}20%{transform:translateX(-8px)}40%{transform:translateX(8px)}60%{transform:translateX(-5px)}80%{transform:translateX(5px)}}",
  "@keyframes funIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}",
  "@keyframes funFloat{from{opacity:1;transform:translateY(0)}to{opacity:0;transform:translateY(-50px)}}",
  "@keyframes funBanner{0%{opacity:0;transform:translate(-50%,0) scale(.5)}15%{opacity:1;transform:translate(-50%,0) scale(1.1)}25%{transform:translate(-50%,0) scale(1)}80%{opacity:1}100%{opacity:0;transform:translate(-50%,-20px) scale(1)}}",
  "@keyframes funStar{0%{transform:scale(0) rotate(-30deg)}70%{transform:scale(1.3) rotate(8deg)}100%{transform:scale(1) rotate(0)}}",
  "@keyframes funDrop{0%{transform:scale(1.4)}100%{transform:scale(1)}}",
  "@media (prefers-reduced-motion:reduce){.fun-in .choice,.fun-in .frame,.fun-shake,.choice.right{animation:none}}"
  ].join("\n");
  var st=document.createElement("style");st.textContent=css;document.head.appendChild(st);

  /* ---------- sound (made in the browser, no files) ---------- */
  var AC=null;
  function ac(){if(S.mute)return null;try{AC=AC||new (window.AudioContext||window.webkitAudioContext)();if(AC.state==="suspended")AC.resume();}catch(e){AC=null;}return AC;}
  function tone(f,t0,dur,type,vol){var a=ac();if(!a)return;var o=a.createOscillator(),g=a.createGain();o.type=type||"sine";o.frequency.value=f;
    var t=a.currentTime+t0;g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol||.18,t+.01);g.gain.exponentialRampToValueAtTime(.001,t+dur);
    o.connect(g);g.connect(a.destination);o.start(t);o.stop(t+dur+.02);}
  var SND={
    right:function(){tone(784,0,.12,"triangle");tone(1175,.08,.2,"triangle");},
    wrong:function(){tone(196,0,.25,"square",.08);tone(147,.1,.3,"square",.08);},
    combo:function(){[659,784,988,1319].forEach(function(f,i){tone(f,i*.07,.18,"triangle",.15);});},
    heart:function(){tone(330,0,.15,"sawtooth",.06);tone(220,.12,.3,"sawtooth",.06);},
    win:function(){[523,659,784,1047,784,1047].forEach(function(f,i){tone(f,i*.11,i===5?.5:.16,"triangle",.17);});},
    star:function(i){tone(880+i*220,0,.18,"triangle",.15);}
  };
  function buzz(ms){try{if(!S.mute&&navigator.vibrate)navigator.vibrate(ms);}catch(e){}}

  /* ---------- start screen: streak, XP, stars on each level ---------- */
  var top=null;
  function drawTop(){
    if(!startP)return;
    if(!top){top=document.createElement("div");top.className="fun-top";startP.insertBefore(top,startP.firstChild);}
    var s=streakNow();
    top.innerHTML="<span class='fun-pill' title='Days in a row you have played'>🔥 "+s+" day"+(s===1?"":"s")+"</span>"+
      "<span class='fun-pill' title='Points you have earned'>⚡ "+S.xp+" XP</span>";
    [].forEach.call(document.querySelectorAll(".mode"),function(b){
      var k=PAGE+"|"+b.dataset.mode,got=(S.best[k]||{}).stars||0,el=b.querySelector(".fun-stars");
      if(!el){el=document.createElement("span");el.className="fun-stars";var go=b.querySelector(".go");b.insertBefore(el,go||null);}
      el.innerHTML=[1,2,3].map(function(n){return "<span class='"+(n<=got?"on":"")+"'>★</span>";}).join("");
      el.setAttribute("aria-label",got+" of 3 stars");
    });
  }
  var mode="";
  [].forEach.call(document.querySelectorAll(".mode"),function(b){b.addEventListener("click",function(){mode=b.dataset.mode;ac();},true);});

  /* ---------- in-game: hearts, combos, feedback ---------- */
  var hud=play.querySelector(".hud"),heartsEl=document.createElement("span"),muteB=document.createElement("button");
  heartsEl.className="fun-hearts";heartsEl.setAttribute("aria-label","Lives");
  muteB.className="fun-mute";muteB.type="button";
  function drawMute(){muteB.textContent=S.mute?"🔇":"🔊";muteB.setAttribute("aria-label",S.mute?"Sound off":"Sound on");}
  muteB.onclick=function(){S.mute=!S.mute;save();drawMute();};drawMute();
  var row=document.createElement("div");row.className="fun-row";row.appendChild(heartsEl);row.appendChild(muteB);
  if(hud)hud.parentNode.insertBefore(row,hud.nextSibling);else play.insertBefore(row,play.firstChild);
  var MAXH=3,hearts,combo,asked,right,xpRound,bestCombo,handled,outOfHearts,ended;
  function drawHearts(){var h="";for(var i=0;i<MAXH;i++)h+="<span class='"+(i<hearts?"":"gone")+"'>❤️</span>";heartsEl.innerHTML=h;}
  function reset(){hearts=MAXH;combo=0;asked=0;right=0;xpRound=0;bestCombo=0;outOfHearts=false;ended=false;drawHearts();play.classList.remove("fun-hot");}
  function flash(cls){play.classList.remove("fun-ok","fun-bad");void play.offsetWidth;play.classList.add(cls);setTimeout(function(){play.classList.remove(cls);},450);}
  function floatText(txt,el){var r=el.getBoundingClientRect(),p=play.getBoundingClientRect(),f=document.createElement("div");
    f.className="fun-float";f.textContent=txt;f.style.left=(r.left-p.left+r.width/2-20)+"px";f.style.top=(r.top-p.top-6)+"px";play.appendChild(f);setTimeout(function(){f.remove();},950);}
  function banner(txt){var b=document.createElement("div");b.className="fun-banner";b.textContent=txt;play.appendChild(b);setTimeout(function(){b.remove();},1250);}
  var COMBO={3:"🔥 3 in a row!",5:"🔥 5 in a row! Double XP",8:"⚡ 8 in a row!",10:"🚀 10 in a row!",15:"🌟 15! Unstoppable!",20:"🏆 20 in a row!!"};

  function onAnswer(){
    if(handled||ended)return;
    var w=box.querySelector(".choice.wrong"),r=box.querySelector(".choice.right");
    if(!w&&!r)return;handled=true;asked++;
    if(!w){
      right++;combo++;if(combo>bestCombo)bestCombo=combo;
      var gain=combo>=5?20:10;xpRound+=gain;
      SND.right();flash("fun-ok");floatText("+"+gain+" XP",r);
      if(combo>=5)play.classList.add("fun-hot");
      if(COMBO[combo]){setTimeout(SND.combo,120);banner(COMBO[combo]);}
    }else{
      combo=0;play.classList.remove("fun-hot");
      hearts--;drawHearts();SND.wrong();setTimeout(SND.heart,250);buzz(120);flash("fun-bad");
      var pr=play.querySelector(".prompt")||play;pr.classList.remove("fun-shake");void pr.offsetWidth;pr.classList.add("fun-shake");
      if(hearts<=0&&typeof window.__leimFinish==="function"){outOfHearts=true;setTimeout(function(){if(!end.hidden)return;window.__leimFinish();},1900);}
    }
  }
  new MutationObserver(function(muts){
    var fresh=muts.some(function(m){return m.type==="childList"&&m.addedNodes.length;});
    if(fresh){handled=false;box.classList.remove("fun-in");void box.offsetWidth;box.classList.add("fun-in");
      var fr=play.querySelector(".prompt");if(fr){fr.classList.remove("fun-in");void fr.offsetWidth;fr.classList.add("fun-in");}}
    onAnswer();
  }).observe(box,{childList:true,subtree:true,attributes:true,attributeFilter:["class"]});

  /* ---------- end screen: stars, XP, best, confetti ---------- */
  var reward=document.createElement("div");reward.className="fun-reward";end.insertBefore(reward,end.firstChild);
  var fin=$("final");if(fin){fin.style.display="none";var lab=fin.previousElementSibling;if(lab&&/score/i.test(lab.textContent))lab.style.display="none";}
  function finishFun(){
    if(ended)return;ended=true;
    var acc=asked?right/asked:0;
    var stars=right===0?0:(right>=14&&acc>=.85)?3:(right>=7&&acc>=.7)?2:1;
    var k=PAGE+"|"+(mode||"all"),prev=S.best[k]||{score:0,stars:0},isBest=right>prev.score&&right>0;
    S.best[k]={score:Math.max(prev.score,right),stars:Math.max(prev.stars,stars)};
    S.xp+=xpRound;var newDay=asked>0&&bumpDay();save();
    var title=outOfHearts?"Out of hearts! 💔":stars===3?"Amazing! 🎉":stars===2?"Great work! 👏":stars===1?"Nice start! 💪":"Have another go! 💪";
    reward.innerHTML="<h2>"+title+"</h2><div class='fun-bigstars' aria-label='"+stars+" of 3 stars'>"+
      [1,2,3].map(function(n){return "<span class='"+(n<=stars?"on":"")+"'>★</span>";}).join("")+"</div>"+
      "<div class='fun-chips'><div class='fun-chip'><b>✅ "+right+"</b><span>right</span></div><div class='fun-chip'><b>⚡ "+xpRound+"</b><span>XP earned</span></div>"+
      "<div class='fun-chip'><b>🎯 "+Math.round(acc*100)+"%</b><span>accuracy</span></div>"+
      "<div class='fun-chip'><b>🔥 "+bestCombo+"</b><span>best combo</span></div></div>"+
      (isBest?"<div class='fun-new'>🏅 New personal best!</div>":"")+
      (newDay?"<div style='margin-top:8px;font-weight:800'>🔥 "+S.day.count+"-day streak! Come back tomorrow to keep it going.</div>":"")+
      "<p style='font-size:14px;color:var(--muted);margin:10px 0 0'>"+(stars<3?"3 stars: 14 right with 85% accuracy.":"You got all 3 stars!")+"</p>";
    var spans=reward.querySelectorAll(".fun-bigstars span");
    [].forEach.call(spans,function(s,i){setTimeout(function(){s.classList.add("show");if(i<stars)SND.star(i);},300+i*350);});
    if(stars>=2)setTimeout(function(){SND.win();confetti();},300+3*350);
    drawTop();
  }
  new MutationObserver(function(){
    if(!play.hidden&&!ended&&asked===0&&hearts===MAXH)return;
    if(!play.hidden&&end.hidden){reset();}
  }).observe(play,{attributes:true,attributeFilter:["hidden"]});
  new MutationObserver(function(){if(!end.hidden)finishFun();}).observe(end,{attributes:true,attributeFilter:["hidden"]});

  function confetti(){
    if(window.matchMedia&&matchMedia("(prefers-reduced-motion: reduce)").matches)return;
    var c=document.createElement("canvas");c.id="funConfetti";document.body.appendChild(c);
    var x=c.getContext("2d"),W=c.width=innerWidth,H=c.height=innerHeight,cols=["#58CC8A","#F2B705","#FF9600","#1CB0F6","#E5534B","#CE82FF"],P=[];
    for(var i=0;i<140;i++)P.push({x:W/2+(Math.random()-.5)*W*.3,y:H*.35,vx:(Math.random()-.5)*14,vy:-Math.random()*14-4,s:6+Math.random()*6,r:Math.random()*6,vr:(Math.random()-.5)*.3,c:cols[i%cols.length]});
    var t0=performance.now();
    (function f(t){x.clearRect(0,0,W,H);P.forEach(function(p){p.vy+=.35;p.vx*=.99;p.x+=p.vx;p.y+=p.vy;p.r+=p.vr;
      x.save();x.translate(p.x,p.y);x.rotate(p.r);x.fillStyle=p.c;x.fillRect(-p.s/2,-p.s/4,p.s,p.s/2);x.restore();});
      if(t-t0<3000)requestAnimationFrame(f);else c.remove();})(t0);
  }

  /* shared with arcade.js */
  window.LeimFun={snd:SND,confetti:confetti,buzz:buzz,isMuted:function(){return !!S.mute;},
    award:function(o){var k=PAGE+"|"+o.key,prev=S.best[k]||{score:0,stars:0},isBest=o.right>prev.score&&o.right>0;
      S.best[k]={score:Math.max(prev.score,o.right),stars:Math.max(prev.stars,o.stars)};S.xp+=o.xp;
      var nd=o.right>0&&bumpDay();save();drawTop();return {isBest:isBest,best:S.best[k].score,newDay:nd,streak:S.day.count};}};
  reset();drawTop();
})();
