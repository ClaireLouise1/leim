// Bridge for the PDF builders: reads {name: "js code"} on stdin, runs each with the Angle Chase drawing helpers
// (G, L, M, MB, T, pt, render, triP, par), and prints {name: svg}. Each snippet must end with an expression returning an SVG string.
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'angle-chase.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const {G,L,M,MB,T,pt,render}=window.__leimTest.draw,O=[0,0];
function triP(A,B,base){base=base||170;const P0=[0,0],P1=[base,0],d=base*Math.sin(B*Math.PI/180)/Math.sin((A+B)*Math.PI/180);return [P0,P1,pt(P0,A,d)];}
function triG(P){const g=G();g.tris.push(P);L(g,P[0],P[1]);L(g,P[1],P[2]);L(g,P[2],P[0]);return g;}
function par(a){const g=G(),h=60,dx=h/Math.tan(a*Math.PI/180),V1=[dx,h],V2=[-dx,-h],lo=Math.min(dx,-dx)-90,hi=Math.max(dx,-dx)+90;L(g,[lo,h],[hi,h],1);L(g,[lo,-h],[hi,-h],1);L(g,pt(V2,a+180,45),pt(V1,a,45));return {g,V:[V1,V2],st:[0,a,180,180+a],val:[a,180-a,a,180-a]};}
const spec=JSON.parse(fs.readFileSync(0,'utf8')),out={};
for(const k in spec)out[k]=eval(spec[k]);
process.stdout.write(JSON.stringify(out));
