const fs=require('fs');
const html=fs.readFileSync(require('path').join(__dirname,'fraction-match.script.html'),'utf8');
const code=html.replace(/^<script>/,'').replace(/<\/script>\s*$/,'');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(code);
const T=window.__leimTest;
const g=(a,b)=>{a=Math.abs(a);b=Math.abs(b);while(b){[a,b]=[b,a%b]}return a};
const R=(n,d)=>{const k=g(n,d);return [n/k,d/k]};
function parse(s){s=s.trim().replace(/^€/,'').replace(/ (students|pieces|glasses|km|minutes|g of flour)$/,'');let m;
 if(m=s.match(/^(\d+) (\d+)\/(\d+)$/))return [ +m[1]*+m[3]+ +m[2], +m[3]];
 if(m=s.match(/^(\d+)\/(\d+)$/))return [+m[1],+m[2]];
 if(m=s.match(/^(\d+)$/))return [+m[1],1]; throw 'parse '+s;}
const eq=(a,b)=>a[0]*b[1]===a[1]*b[0];
function op(a,o,b){if(o==='+')return R(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);if(o==='−')return R(a[0]*b[1]-b[0]*a[1],a[1]*b[1]);if(o==='×')return R(a[0]*b[0],a[1]*b[1]);return R(a[0]*b[1],a[1]*b[0]);}
function lowestForm(s){ // answer must be simplest: proper part reduced
 let m=s.match(/(\d+)\/(\d+)$/);return !m||g(+m[1],+m[2])===1;}
let probs=0,n=0;const bad=(q,msg)=>{probs++;if(probs<25)console.log(msg,JSON.stringify({en:q.en,frame:q.frame,a:q.answer,w:q.wrong}));};
for(const mode in T.MAKERS)for(const mk of T.MAKERS[mode])for(let i=0;i<400;i++){const q=mk();n++;
 const all=[q.answer,...q.wrong];
 if(q.wrong.length!==3||new Set(all).size!==4)bad(q,'options');
 if(all.some(x=>/undefined|NaN|Infinity|null/.test(x))||/undefined|NaN/.test(q.en+q.frame+q.why))bad(q,'undef');
 let A; const name=mk.name;
 // expected value
 let E=null;
 if(/^[\d\s\/]+ [+−×÷] [\d\s\/]+$/.test(q.frame)){const m=q.frame.match(/^(.+) ([+−×÷]) (.+)$/);E=op(parse(m[1]),m[2],parse(m[3]));}
 else if(name==='qSimplify'){const f=parse(q.frame);E=f; if(!lowestForm(q.answer))bad(q,'not simplest');}
 else if(name==='qToMixed'||name==='qToImproper'){E=parse(q.frame); if(name==='qToMixed'&&!/ /.test(q.answer))bad(q,'not mixed'); if(name==='qToImproper'&&/ /.test(q.answer))bad(q,'not improper');}
 else if(name==='qShaded'||name==='qShadedSimplest'||name==='qPicEquiv'){const on=(q.html.match(/data-on="1"/g)||[]).length,tot=(q.html.match(/class="pc"/g)||[]).length;E=[on,tot];
   if(name==='qShaded'&&q.answer!==on+'/'+tot)bad(q,'shaded raw'); if(name==='qShadedSimplest'&&!lowestForm(q.answer))bad(q,'simp');}
 else if(name==='qLine'){const d=+q.html.match(/data-d="(\d+)"/)[1],k=+q.html.match(/data-k="(\d+)"/)[1];
   // recompute from geometry: arrow x / unit length
   const ax=+q.html.match(/<path d="M([\d.]+) 4/)[1];const units=(q.html.match(/font-size="16"/g)||[]).length-1;E=R(Math.round(ax/(300/units)*d),d); if(Math.round(ax/(300/units)*d)!==k)bad(q,'line');}
 else if(name==='qMissing'){const m=q.frame.match(/^(\d+)\/(\d+) = (\?|\d+)\/(\?|\d+)$/);const a=+m[1],b=+m[2];const ans=m[3]==='?'? a*(+m[4])/b : b*(+m[3])/a; if(String(ans)!==q.answer)bad(q,'missing'); for(const w of q.wrong)if(String(ans)===w)bad(q,'missing w'); continue;}
 else if(name==='qWhichEquiv'){const t=parse(q.en.match(/equal to (\S+)\?/)[1]);if(!eq(parse(q.answer),t))bad(q,'eqv');for(const w of q.wrong)if(eq(parse(w),t))bad(q,'eqv wrong');continue;}
 else if(name==='qBiggest'){const L=q.list.map(f=>f[0]/f[1]);const v=parse(q.answer);const tgt=q.big?Math.max(...L):Math.min(...L);if(Math.abs(v[0]/v[1]-tgt)>1e-12)bad(q,'big');if(new Set(L).size!==4)bad(q,'tie');continue;}
 else if(name==='qOf'){const m=q.frame.match(/^(\d+)\/(\d+) of €?(\d+)/);E=[+m[1]*+m[3]/+m[2],1];}
 else if(name==='qPieces'){const m=q.en.match(/(\d+) (m|litres)[^\d]+(\d+\/\d+)/);E=op([+m[1],1],'÷',parse(m[3]));}
 else if(name==='qRest'){const m=q.en.match(/€(\d+)\. She spends (\d+\/\d+) of it.*then (\d+\/\d+)/);const D=+m[1],a=parse(m[2]),b=parse(m[3]);E=[(D-D*a[0]/a[1])*b[0]/b[1],1];}
 else if(name==='qWhole'){const m=q.en.match(/^(\d+)\/(\d+) .*That's (\d+) students/);E=[+m[3]*+m[2]/+m[1],1];}
 if(!E){bad(q,'no check '+name);continue;}
 if(!eq(parse(q.answer),E))bad(q,'WRONG ANSWER '+name);
 if(['qAdd','qSub','qMixedAdd','qMixedSub','qMul','qDiv','qMixedMul','qMixedDiv','qAddSame'].includes(name)&&!lowestForm(q.answer))bad(q,'not lowest');
 if(['qMixedAdd','qMixedSub','qMul','qDiv','qMixedMul','qMixedDiv','qAdd','qSub'].includes(name)){const v=parse(q.answer);if(v[0]>v[1]&&v[1]!==1&&!/ /.test(q.answer))bad(q,'should be mixed');}
 for(const w of q.wrong)if(eq(parse(w),E))bad(q,'wrong option is right '+name);
}
console.log(n,'questions,',probs,'problems');
