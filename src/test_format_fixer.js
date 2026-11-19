// Runs every Format Fixer maker N times outside the page and prints the questions as JSON lines for src/test_format_fixer.py.
// Usage: N=400 node src/test_format_fixer.js format-fixer.html > /tmp/ff.jsonl
const fs=require("fs");const html=fs.readFileSync(process.argv[2]||"format-fixer.html","utf8");
const js=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes("__leimTest"));
const el=()=>({style:{},classList:{add(){}},children:[],appendChild(){},setAttribute(){},scrollIntoView(){}});
global.window={};global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
eval(js);const T=window.__leimTest,N=+process.env.N||400;
for(const m in T.MAKERS)T.MAKERS[m].forEach((f,i)=>{for(let k=0;k<N;k++){const q=f();console.log(JSON.stringify({mode:m,i,en:q.en,html:q.html,answer:q.answer,wrong:q.wrong,nw:q.nw,why:q.why,data:q.data}));}});
