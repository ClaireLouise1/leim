// echo '{"name":"nl({lo:3,loIn:false,hi:null},\"R\",-2,8)"}' | node src/number_line_figs_bridge.js
// Evaluates figure calls (nl, graphSVG) with Number-Line Shade's own kit, so PDFs use the game's drawings.
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.join(__dirname,'number-line-shade.script.html'),'utf8');
const code=html.replace(/^<script>/,'').replace(/<\/script>\s*$/,'');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};global.window={};eval(code);
const K=window.__leimTest.kit,nl=K.nl,graphSVG=K.graphSVG;
const F=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in F){out[k]=eval(F[k]);if(!out[k])throw new Error('no figure: '+k);}
process.stdout.write(JSON.stringify(out));
