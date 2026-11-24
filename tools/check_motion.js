/* Focused checks for viewport motion, route refresh and reduced-motion fallback. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../assets/motion.js'),'utf8');
function element(){
  const classes=new Set(),styles=new Map();
  return {style:{setProperty:(name,value)=>styles.set(name,value),getPropertyValue:name=>styles.get(name)},classList:{add:c=>classes.add(c),remove:c=>classes.delete(c),contains:c=>classes.has(c),
    toggle:(c,on)=>on?classes.add(c):classes.delete(c)}};
}
function setup({reduced=false,supported=true}={}){
  const hero=element(),timeline=element(),targets=[element(),element()];
  const events={},observers=[],media={matches:reduced,addEventListener:(_,cb)=>{media.change=cb;}};
  class Observer{
    constructor(callback){this.callback=callback;this.observed=new Set();observers.push(this);}
    observe(el){this.observed.add(el);}
    unobserve(el){this.observed.delete(el);}
    disconnect(){this.disconnected=true;this.observed.clear();}
    emit(target,isIntersecting){this.callback([{target,isIntersecting}]);}
  }
  const document={querySelector:()=>hero,querySelectorAll:selector=>selector==='.timeline'?[timeline]:selector==='.motion-pending'?targets.filter(e=>e.classList.contains('motion-pending')):targets,
    addEventListener:(name,cb)=>{events[name]=cb;}};
  vm.runInNewContext(source,{document,matchMedia:()=>media,IntersectionObserver:Observer,
    window:supported?{IntersectionObserver:Observer}:{}});
  return {hero,timeline,targets,events,observers,media};
}
const normal=setup();
assert(normal.hero.classList.contains('motion-enter'));
assert.equal(normal.observers[0].observed.size,2);
assert(normal.targets.every(e=>e.classList.contains('motion-pending')));
normal.observers[0].emit(normal.targets[0],true);
assert(normal.targets[0].classList.contains('motion-enter'));
assert(!normal.observers[0].observed.has(normal.targets[0]));
assert(!normal.targets[0].classList.contains('motion-pending'));
normal.observers[1].emit(normal.timeline,true);
assert(normal.timeline.classList.contains('timeline-active'));
normal.observers[1].emit(normal.timeline,false);
assert(!normal.timeline.classList.contains('timeline-active'));
normal.media.matches=true;normal.media.change();
assert(normal.observers.every(o=>o.disconnected));
assert(!normal.timeline.classList.contains('timeline-active'));
assert(normal.targets.every(e=>!e.classList.contains('motion-pending')));
normal.media.matches=false;normal.media.change();
assert(!normal.observers[2].observed.has(normal.targets[0]),'Do not repeat completed entrances');
const newCard=element();normal.targets.push(newCard);normal.events['workex:page-ready']();
assert(normal.observers[4].observed.has(newCard),'New route content must be observed');
const stagger=setup();
stagger.observers[0].callback(stagger.targets.map(target=>({target,isIntersecting:true})));
assert.equal(stagger.targets[0].style.getPropertyValue('--enter-delay'),'0ms');
assert.equal(stagger.targets[1].style.getPropertyValue('--enter-delay'),'65ms');
for(const fallback of [setup({reduced:true}),setup({supported:false})]){
  assert.equal(fallback.observers.length,0);
  assert(fallback.targets.every(e=>!e.classList.contains('motion-pending')));
  assert(!fallback.hero.classList.contains('motion-enter'));
  assert(!fallback.timeline.classList.contains('timeline-active'));
}
console.log('Passed: staged entrances, reveal preparation, route refresh and visible motion fallbacks.');
