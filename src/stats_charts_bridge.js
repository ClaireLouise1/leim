// Bridge for build_statistics2_pdfs.py: reads {name: "js expression"} on stdin, evaluates each with the Average Ace
// chart kit in scope (barSVG, pieSVG, dotSVG, histSVG, slHTML, btbHTML, freqHTML) and prints {name: svg/html}.
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'average-ace.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const {barSVG,pieSVG,dotSVG,histSVG,slHTML,btbHTML,freqHTML}=window.__leimTest.draw;
const spec=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in spec)out[k]=eval(spec[k]);
process.stdout.write(JSON.stringify(out));
