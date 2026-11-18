// Bridge for build_trigonometry_pdfs.py: reads {name: "js expression"} on stdin, evaluates each with the Clinometer Challenge
// geometry kit in scope (G, L, M, MB, LEN, NM, render, ttri, scene, ladderT, FIX) and prints {name: svg}.
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'clinometer-challenge.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const K=window.__leimTest.kit;const {G,L,M,MB,LEN,NM,render,ttri,scene,ladderT,FIX}=K;
const spec=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in spec)out[k]=eval(spec[k]);
process.stdout.write(JSON.stringify(out));
