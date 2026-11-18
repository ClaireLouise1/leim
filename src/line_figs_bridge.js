// Bridge for build_coordinate_line_pdfs.py: reads {name: "js expression"} on stdin, evaluates each with the Line Lab
// grid kit in scope (plane, eq, gen, F, FIX) and prints {name: svg}.
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'line-lab.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const {plane,eq,gen,F,FIX}=window.__leimTest.kit;
const spec=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in spec)out[k]=eval(spec[k]);
process.stdout.write(JSON.stringify(out));
