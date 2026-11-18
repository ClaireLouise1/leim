// Bridge for build_area_pdfs.py: reads {name: "js expression"} on stdin, evaluates each with the Floor Planner
// figure kit in scope (draw, rectFig, Lfig, triFig, rtFig, paraFig, gableFig, circleFig, semiFig, quarterFig, windowFig, trackFig, gridFig)
// and prints {name: svg}.
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'floor-planner.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const {draw,rectFig,Lfig,triFig,rtFig,paraFig,gableFig,circleFig,semiFig,quarterFig,windowFig,trackFig,gridFig}=window.__leimTest.draw;
const spec=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in spec)out[k]=eval(spec[k]);
process.stdout.write(JSON.stringify(out));
