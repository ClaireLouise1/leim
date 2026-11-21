// Runs every English Exam Mix exam-technique maker N times outside the page and prints the questions as JSON lines
// for src/test_english_exam_mix.py. (The borrowed game questions are tested by src/test_english_exam_mix_bundles.js.)
// Usage: N=400 node src/test_english_exam_mix.js english-exam-mix.html > /tmp/xm.jsonl
const fs=require("fs");const html=fs.readFileSync(process.argv[2]||"english-exam-mix.html","utf8");
const js=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes("__leimTest"));
const el=()=>({style:{},classList:{add(){}},children:[],appendChild(){},setAttribute(){},scrollIntoView(){}});
global.window={};global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el,body:el()};
eval(js);const T=window.__leimTest,N=+process.env.N||400;
T.MAKERS.tech.forEach((f,i)=>{for(let k=0;k<N;k++){const q=f();console.log(JSON.stringify({mode:"tech",i,src:q.src,en:q.en,html:q.html,answer:q.answer,wrong:q.wrong,nw:q.nw,why:q.why,data:q.data}));}});
