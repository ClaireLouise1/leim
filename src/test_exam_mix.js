// Dumps Exam Mix "Problem solver" questions as JSON lines for src/test_exam_mix.py.
// Usage: TL=<file> N=<count per maker> node src/test_exam_mix.js > out.jsonl
const fs=require('fs'),vm=require('vm');
const html=fs.readFileSync(process.env.TL||'exam-mix.html','utf8');
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const code=scripts.find(s=>s.includes('__leimTest'));
function el(){return {style:{},hidden:false,appendChild(){},setAttribute(){},classList:{add(){},remove(){}},children:[],textContent:'',innerHTML:'',scrollIntoView(){}};}
const ctx={document:{createElement:el,body:el(),head:el(),getElementById:()=>el(),querySelectorAll:()=>[],addEventListener(){}},Math,console,setTimeout:()=>0,setInterval:()=>0,clearInterval(){}};
ctx.window=ctx;vm.createContext(ctx);vm.runInContext(code,ctx);
const T=ctx.__leimTest,N=+(process.env.N||400);
for(const f of T.SOLVE){for(let i=0;i<N;i++){const q=f();
  const facts=[...q.html.matchAll(/<p>(.*?)<\/p>/g)].map(m=>m[1]);
  console.log(JSON.stringify({m:f.name,t:q.data.t,en:q.en,facts,answer:q.answer,wrong:q.wrong,why:q.why}));}}
