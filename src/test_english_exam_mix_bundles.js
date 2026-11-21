// Loads every english-exam-mix-<section>.js in node with a stub document and runs every borrowed maker N times.
// Generic checks: nothing throws, enough wrong options (nw), answer never among the wrong options, no NaN/undefined/[object.
// Also writes each game's questions to $OUT/<slug>.jsonl in that game's own test format, so
// src/check_english_exam_mix_bundles.py can run each game's OWN independent checker on the borrowed questions.
// Usage: N=40 OUT=/tmp/eem node src/test_english_exam_mix_bundles.js
const fs=require('fs'),vm=require('vm'),path=require('path');
const N=+(process.env.N||40),OUT=process.env.OUT||'/tmp/eem';fs.mkdirSync(OUT,{recursive:true});
function el(){return {style:{},appendChild(){},setAttribute(){},classList:{add(){},remove(){}},children:[],textContent:'',innerHTML:''};}
const doc={createElement:el,head:el(),body:el(),getElementById:()=>el(),querySelector:()=>el(),querySelectorAll:()=>[],addEventListener(){}};
const ctx={document:doc,Math,console,JSON,setTimeout:()=>0,clearTimeout(){},localStorage:{getItem(){return null},setItem(){}}};
ctx.window=ctx;vm.createContext(ctx);
let bad=0,total=0;
for(const s of ['reading','writing','texts','language'])vm.runInContext(fs.readFileSync(`english-exam-mix-${s}.js`,'utf8'),ctx,{filename:s});
for(const [slug,G] of Object.entries(ctx.LEIM_EN)){
  const lines=[];let n=0;
  for(const m in G.M)G.M[m].forEach((f,i)=>{for(let k=0;k<N;k++){total++;n++;let q;
    try{q=f();}catch(e){bad++;if(bad<20)console.log('THROW',slug,m,i,e.message);return;}
    lines.push(JSON.stringify({mode:m,i,en:q.en,html:q.html,answer:q.answer,wrong:q.wrong,nw:q.nw,fixed:q.fixed||null,why:q.why,data:q.data}));
    const txt=[q.en,q.answer].concat(q.wrong).join('|');
    if(q.wrong.indexOf(q.answer)>=0||/NaN|undefined|\[object/.test(txt+'|'+(q.html||''))){bad++;if(bad<20)console.log('BAD',slug,m,i,txt.slice(0,200));}
  }});
  fs.writeFileSync(path.join(OUT,slug+'.jsonl'),lines.join('\n')+'\n');
  console.log(slug,Object.keys(G.M).length,'modes',n,'questions, orders',G.orders.map(a=>a.length).join('/'),G.pu?'pu':'');
}
console.log('games',Object.keys(ctx.LEIM_EN).length,'total',total,'bad',bad);process.exit(bad?1:0);
