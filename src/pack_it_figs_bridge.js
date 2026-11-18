// Bridge for build_volume_pdfs.py: reads {name: "js expression"} on stdin, evaluates each with the Pack It
// geometry kit in scope (render, cuboid, cube, triPrism, gable, cylinder, sphere, silo, netCuboid, netTri, netCyl, FIX) and prints {name: svg}.
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'pack-it.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const K=window.__leimTest.kit;const {render,cuboid,cube,triPrism,gable,cylinder,sphere,silo,netCuboid,netTri,netCyl,FIX}=K;
const spec=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in spec)out[k]=eval(spec[k]);
process.stdout.write(JSON.stringify(out));
