// node src/test_proof_builder.js > /tmp/fp.json ; python3 src/test_proof_builder.py /tmp/fp.json   (env PB2=<file> tests a mutated copy, N=<count> per maker)
const fs=require('fs');
const html=fs.readFileSync(process.env.PB2||require('path').join(__dirname,'proof-builder.script.html'),'utf8');
const code=html.replace(/^<script>/,'').replace(/<\/script>\s*$/,'');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(code);
const N=+(process.env.N||400),out=[];
for(const mode in window.__leimTest.MAKERS){const seen=new Set();for(const mk of window.__leimTest.MAKERS[mode]){if(seen.has(mk))continue;seen.add(mk);for(let i=0;i<N;i++){const q=mk();out.push({mode,mk:mk.name,en:q.en,frame:q.frame,html:q.html,answer:q.answer,wrong:q.wrong,data:q.data,why:q.why,review:q.review});}}}
process.stdout.write(JSON.stringify(out));
