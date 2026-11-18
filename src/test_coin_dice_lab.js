// node src/test_coin_dice_lab.js > /tmp/cdl.json ; python3 src/test_coin_dice_lab.py /tmp/cdl.json   (env CDL=<file> tests a mutated copy, env N=<count> per maker)
const fs=require('fs');
const html=fs.readFileSync(require('path').resolve(__dirname,(process.env.CDL||'coin-dice-lab.script.html')+''),'utf8');
const code=html.replace(/^<script>/,'').replace(/<\/script>\s*$/,'');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){},toggle(){}},hidden:false,scrollIntoView(){},setAttribute(){},dataset:{}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(code);
const N=+(process.env.N||400),out=[],M=window.__leimTest.MAKERS,done=new Set();
for(const mode in M)for(const mk of M[mode]){if(mode==='mixed'||done.has(mk.name)&&mode!=='lab')continue;done.add(mk.name);for(let i=0;i<N;i++){const q=mk();out.push({mode,mk:mk.name,en:q.en,frame:q.frame,html:q.html,answer:q.answer,wrong:q.wrong,data:q.data,why:q.why,review:q.review});}}
process.stdout.write(JSON.stringify(out));
