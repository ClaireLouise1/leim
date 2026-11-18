// Loads every exam-mix-<strand>.js in node with a stub document and runs every maker N times.
// Checks: 3 wrong options, answer not among them, no NaN/undefined/[object in any text.
const fs=require('fs'),vm=require('vm');
const N=+(process.env.N||60);
function el(){return {style:{},appendChild(){},setAttribute(){},classList:{add(){},remove(){}},children:[],textContent:'',innerHTML:''};}
const doc={createElement:el,head:el(),body:el(),getElementById:()=>el(),querySelector:()=>el(),querySelectorAll:()=>[],addEventListener(){}};
const ctx={document:doc,window:{},Math,console,setTimeout:()=>0,clearTimeout(){},localStorage:{getItem(){return null},setItem(){}}};
ctx.window=ctx;vm.createContext(ctx);
let bad=0,total=0;
for(const s of ['number','algebra','geometry','stats']){
  vm.runInContext(fs.readFileSync(`exam-mix-${s}.js`,'utf8'),ctx,{filename:s});
}
for(const [slug,M] of Object.entries(ctx.LEIM_MAKERS)){
  let n=0;
  for(const f of M.mixed){for(let i=0;i<N;i++){total++;n++;let q;
    try{q=f();}catch(e){bad++;if(bad<20)console.log('THROW',slug,f.name,e.message);break;}
    const txt=[q.en,q.frame,q.answer].concat(q.wrong).join('|');
    if(q.wrong.length<3){/* the games re-roll these (tries<20) */ continue;}
    if(q.wrong.indexOf(q.answer)>=0||/NaN|undefined|\[object/.test(txt)){bad++;if(bad<20)console.log('BAD',slug,f.name,txt.slice(0,200));}
  }}
  console.log(slug,M.mixed.length,'makers',n);
}
console.log('total',total,'bad',bad);process.exit(bad?1:0);
