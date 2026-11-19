// Runs every Paragraph Builder maker N times outside the page and prints the questions as JSON lines for src/test_paragraph_builder.py.
// Usage: N=400 node src/test_sentence_surgeon.js paragraph-builder.html > /tmp/pb.jsonl
const fs=require("fs");const html=fs.readFileSync(process.argv[2]||"paragraph-builder.html","utf8");
const js=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes("__leimTest"));
const el=()=>({style:{},classList:{add(){}},children:[],appendChild(){},setAttribute(){},scrollIntoView(){}});
global.window={};global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
eval(js);const T=window.__leimTest,N=+process.env.N||400;
for(const m in T.MAKERS)T.MAKERS[m].forEach((f,i)=>{for(let k=0;k<N;k++){const q=f();console.log(JSON.stringify({mode:m,i,en:q.en,html:q.html,answer:q.answer,wrong:q.wrong,why:q.why,data:q.data}));}});
