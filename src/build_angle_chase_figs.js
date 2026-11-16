// Draws the fixed diagrams for the Angle Chase rules section + Exam corner with the game's own render(),
// and pastes them into src/angle-chase.main.html between <!--FIG:name--> … <!--/FIG--> markers.
// node src/build_angle_chase_figs.js  (then re-run src/assemble_game.py)
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.resolve(__dirname,'angle-chase.script.html'),'utf8');
const el=()=>({textContent:'',innerHTML:'',style:{},className:'',children:[],appendChild(){},classList:{add(){}},hidden:false,scrollIntoView(){},setAttribute(){}});
global.document={getElementById:el,querySelectorAll:()=>[],addEventListener(){},createElement:el};
global.window={};eval(html.replace(/^<script>/,'').replace(/<\/script>\s*$/,''));
const {G,L,M,MB,T,pt,render}=window.__leimTest.draw;
const O=[0,0],F={};
// straight line a + b = 180
{const g=G();L(g,[-100,0],[100,0]);L(g,O,pt(O,55,90));M(g,O,0,55,"a");M(g,O,55,125,"b");F.straight=render(g,"a and b on a straight line",[220,176]);}
{const g=G();[20,140,250].forEach(d=>L(g,O,pt(O,d,85)));M(g,O,20,120,"a");M(g,O,140,110,"b");M(g,O,250,130,"c");F.point=render(g,"a, b and c at a point",[190,152]);}
{const g=G();L(g,pt(O,25,100),pt(O,205,100));L(g,pt(O,125,100),pt(O,305,100));M(g,O,25,100,"a");M(g,O,205,100,"b");F.vo=render(g,"vertically opposite angles a and b",[210,168]);}
function par(a){const g=G(),h=60,dx=h/Math.tan(a*Math.PI/180),V1=[dx,h],V2=[-dx,-h];L(g,[-140,h],[140,h],1);L(g,[-140,-h],[140,-h],1);L(g,pt(V2,a+180,45),pt(V1,a,45));return {g,V1,V2,a};}
{const p=par(62);M(p.g,p.V1,180+62,118,"a");M(p.g,p.V2,62,118,"b");F.alt=render(p.g,"alternate angles a and b",[240,192]);}
{const p=par(62);M(p.g,p.V1,0,62,"a");M(p.g,p.V2,0,62,"b");F.cor=render(p.g,"corresponding angles a and b",[240,192]);}
{const p=par(62);M(p.g,p.V1,180+62,118,"a");M(p.g,p.V2,0,62,"b");F.coi=render(p.g,"co-interior angles a and b",[240,192]);}
function triP(A,B,base){const P0=[0,0],P1=[base,0],d=base*Math.sin(B*Math.PI/180)/Math.sin((A+B)*Math.PI/180);return [P0,P1,pt(P0,A,d)];}
{const P=triP(55,70,170),g=G();g.tris.push(P);L(g,P[0],P[1]);L(g,P[1],P[2]);L(g,P[2],P[0]);MB(g,P[0],P[1],P[2],"a");MB(g,P[1],P[2],P[0],"b");MB(g,P[2],P[0],P[1],"c");F.tri=render(g,"triangle with angles a, b and c",[210,168]);}
{const P=triP(68,68,150),g=G();g.tris.push(P);L(g,P[0],P[1]);L(g,P[1],P[2]);L(g,P[2],P[0]);T(g,P[0],P[2]);T(g,P[1],P[2]);MB(g,P[0],P[1],P[2],"a");MB(g,P[1],P[2],P[0],"b");F.iso=render(g,"isosceles triangle with base angles a and b",[190,152]);}
{const P=triP(55,65,150),g=G();g.tris.push(P);L(g,P[0],[235,0]);L(g,P[1],P[2]);L(g,P[2],P[0]);MB(g,P[0],P[1],P[2],"a");MB(g,P[2],P[0],P[1],"b");MB(g,P[1],[235,0],P[2],"e");F.ext=render(g,"exterior angle e with interior opposite angles a and b",[240,192]);}
// Exam corner
{const g=G();L(g,pt(O,20,110),pt(O,200,110));L(g,pt(O,78,110),pt(O,258,110));M(g,O,20,58,58);M(g,O,78,122,"a");M(g,O,200,58,"b");M(g,O,258,122,"c");F.ex1=render(g,"Two lines crossing: 58 degrees, a, b and c",[260,208]);}
{const p=par(65);M(p.g,p.V1,0,65,65);M(p.g,p.V2,0,65,"p");M(p.g,p.V1,180+65,115,"q");M(p.g,p.V2,65,115,"r");F.ex2=render(p.g,"Parallel lines: 65 degrees, p, q and r",[280,224]);}
{const P=triP(70,70,150),g=G();g.tris.push(P);L(g,P[0],[235,0]);L(g,P[1],P[2]);L(g,P[2],P[0]);T(g,P[0],P[2]);T(g,P[1],P[2]);MB(g,P[2],P[0],P[1],40);MB(g,P[0],P[1],P[2],"x");MB(g,P[1],[235,0],P[2],"y");
  g.names.push({p:pt(P[2],90,16),t:"A"},{p:[-14,-8],t:"B"},{p:[150,-16],t:"C"},{p:[235,-16],t:"D"});F.ex3=render(g,"Isosceles triangle ABC with angle A 40 degrees",[260,208]);}
{const P=triP(67,65,160),g=G();g.tris.push(P);L(g,P[0],[245,0]);L(g,P[1],P[2]);L(g,P[2],P[0]);MB(g,P[2],P[0],P[1],48);MB(g,P[0],P[1],P[2],67);MB(g,P[1],[245,0],P[2],"w");
  g.names.push({p:pt(P[2],90,16),t:"P"},{p:[-14,-8],t:"Q"},{p:[160,-16],t:"R"},{p:[245,-16],t:"S"});F.ex4=render(g,"Triangle PQR with QR extended to S",[260,208]);}
const mp=path.resolve(__dirname,'angle-chase.main.html');let m=fs.readFileSync(mp,'utf8');
for(const k in F){const re=new RegExp('<!--FIG:'+k+'-->[\\s\\S]*?<!--/FIG-->');if(!re.test(m))throw 'missing marker '+k;m=m.replace(re,'<!--FIG:'+k+'-->'+F[k]+'<!--/FIG-->');}
fs.writeFileSync(mp,m);console.log('figures:',Object.keys(F).join(' '));
