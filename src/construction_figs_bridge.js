// Bridge for the Constructions PDF builder: reads {name: "js expression"} on stdin, evaluates each with the Construction Steps
// game's own builders and drawing kit in scope (BUILD, NAMES, draw, render, withSeed, upto, S, A, AR, N, M, RT, LEN, W, DOT, FILL, pt, cc, dist, ang, U),
// and prints {name: result} (results can be SVG strings or any JSON).
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'construction-steps.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const T=window.__leimTest,{BUILD,NAMES,draw,render,withSeed,upto}=T,{S,A,AR,N,M,RT,LEN,W,DOT,FILL,pt,cc,dist,ang,U}=T.el;
// a seeded construction: {k, title, steps: [texts], svgs: [drawing after step j, newest in red], full}
function con(k,seed,box){return withSeed(seed,()=>{const c=BUILD[k]();const n=c.steps.length;
  return {k:c.k,n:c.n,title:c.title,start:c.start,steps:c.steps.map(s=>s.tx),mist:c.mist,svgs:[...Array(n+1).keys()].map(j=>draw(c,j,box)),full:draw(c,n,box,false)};});}
const spec=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in spec)out[k]=eval(spec[k]);
process.stdout.write(JSON.stringify(out));
