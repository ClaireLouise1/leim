// node src/test_angle_chase.js > /tmp/ac.json ; python3 src/test_angle_chase.py /tmp/ac.json   (env AC=<file> tests a mutated copy)
const fs=require('fs');
const html=fs.readFileSync(require('path').resolve(__dirname,(process.env.AC||"angle-chase.script.html")+''),'utf8');
const code=html.replace(/^<script>/,'').replace(/<\/script>\s*$/,'');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(code);
const out=[];
for(const mode in window.__leimTest.MAKERS)for(const mk of window.__leimTest.MAKERS[mode])for(let i=0;i<400;i++){const q=mk();out.push({mode,mk:mk.name,en:q.en,frame:q.frame,html:q.html,answer:q.answer,wrong:q.wrong,data:q.data,why:q.why,review:q.review});}
process.stdout.write(JSON.stringify(out));
