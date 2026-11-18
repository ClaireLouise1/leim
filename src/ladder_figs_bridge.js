// Bridge for build_pythagoras_pdfs.py: reads {name: "js expression"} on stdin, evaluates each with the Ladder Lab
// geometry kit in scope (G, L, MB, T, LEN, NM, POLY, pt, render, rtTri0, ladder, rectFig, isoFig, sqOn, lerp, mid, cen, FIX) and prints {name: svg}.
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'ladder-lab.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const K=window.__leimTest.kit;const {G,L,M,MB,T,LEN,NM,POLY,pt,render,rtTri,rtTri0,ladder,rectFig,isoFig,sqOn,lerp,mid,cen,FIX}=K;
const spec=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in spec)out[k]=eval(spec[k]);
process.stdout.write(JSON.stringify(out));
