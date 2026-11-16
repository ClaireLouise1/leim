// Draws the fixed Exam-corner diagrams for Construction Steps with the game's own render(),
// and pastes them into src/construction-steps.main.html between <!--FIG:name--> … <!--/FIG--> markers.
// node src/build_construction_figs.js  (then re-run src/assemble_game.py). Also used by build_constructions_pdfs.py (FIGS export).
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'construction-steps.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const T=window.__leimTest,{S,A,AR,N,M,RT,LEN,W,DOT,FILL,pt,cc,dist,ang,U}=T.el;
function R(els,label,box){return T.render(els.map(e=>[e,1]),label,box||[300,230],-1);}
const F={};
{const a=[0,0],b=[9*U,0],r=6*U,X=cc(a,r,b,r),c=X[0],d=X[1],m=[4.5*U,0];
 F.ex1=R([S(a,b),N(a,"A",180),N(b,"B",0),AR(a,c,16),AR(a,d,16),AR(b,c,16),AR(b,d,16),N(c,"C",35),N(d,"D",-35),S(pt(c,90,20),pt(d,270,20)),RT(m,0),N(m,"M",135),LEN(a,b,"9 cm",-1)],"Perpendicular bisector of a 9 cm line segment");}
{const p=[0,0],q=[8*U,0],r=pt(p,55,6*U);
 F.ex2=R([FILL([p,q,r]),S(p,q),S(p,pt(p,55,6*U+40)),M(p,0,55,"55°"),AR(p,r,13),S(r,q),N(p,"P",210),N(q,"Q",-30),N(r,"R",145),LEN(p,q,"8 cm",-1),LEN(p,r,"6 cm",1)],"Triangle PQR: 8 cm, 55 degrees, 6 cm");}
{const c=[0,0],d=[10*U,0],ph=35,s=55,m=[1,2,3].map(i=>pt(c,ph,i*s)),els=[S(c,d),N(c,"C",200),N(d,"D",-20),S(c,pt(c,ph,3*s+40)),LEN(c,d,"10 cm",-1)];
 m.forEach((x,i)=>els.push(AR(i?m[i-1]:c,x,10),DOT(x)));els.push(S(m[2],d));
 [1,2].forEach(i=>{const X=[d[0]*i/3,0];els.push(S(m[i-1],pt(X,ang(m[2],d),12)),DOT(X));});
 F.ex3=R(els,"A 10 cm line segment divided into three equal parts");}
{const y=[0,0],z=pt(y,0,150),x=pt(y,70,150),rr=70,dd=pt(y,70,rr),ee=pt(y,0,rr),r2=62,X=cc(dd,r2,ee,r2),f=dist(X[0],y)>dist(X[1],y)?X[0]:X[1];
 F.ex4=R([S(y,x),S(y,z),N(x,"X",160),N(y,"Y",215),N(z,"Z",-90),A(y,rr,-12,82),AR(dd,f,18),AR(ee,f,18),S(y,pt(y,35,175)),M(y,0,35,"35°"),M(y,35,35,"35°")],"The bisector of a 70 degree angle");}
if(require.main===module){
 const mp=path.resolve(__dirname,'construction-steps.main.html');let m=fs.readFileSync(mp,'utf8');
 for(const k in F){const re=new RegExp('<!--FIG:'+k+'-->[\\s\\S]*?<!--/FIG-->');if(!re.test(m))throw 'missing marker '+k;m=m.replace(re,'<!--FIG:'+k+'-->'+F[k]+'<!--/FIG-->');}
 fs.writeFileSync(mp,m);console.log('figures:',Object.keys(F).join(' '));}
module.exports=F;
