/* Check complete printing, cancellation restoration and reading controls. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../assets/sop-reader.js'),'utf8');
function setup(){
 const details=[{open:false},{open:true},{open:false}];
 const clicks={},events={},media={};let prints=0;
 const document={
  querySelectorAll:()=>details,
  querySelector:selector=>({addEventListener:(_,callback)=>{clicks[selector.match(/"(.*?)"/)[1]]=callback;}}),
 };
 const window={print:()=>{prints++;assert(details.every(item=>item.open));},addEventListener:(event,callback)=>{events[event]=callback;}};
 vm.runInNewContext(source,{document,window,matchMedia:()=>({addEventListener:(_,callback)=>{media.change=callback;}})});
 return {details,clicks,events,media,prints:()=>prints};
}
const normal=setup();
normal.clicks.expand();assert(normal.details.every(item=>item.open));
normal.clicks.collapse();assert(normal.details.every(item=>!item.open));
normal.details[1].open=true;
normal.clicks.print();normal.events.beforeprint();
assert.equal(normal.prints(),1);
normal.events.afterprint();
assert.deepEqual(normal.details.map(item=>item.open),[false,true,false]);
normal.events.beforeprint();normal.media.change({matches:true});
assert(normal.details.every(item=>item.open));
normal.media.change({matches:false});normal.events.afterprint();
assert.deepEqual(normal.details.map(item=>item.open),[false,true,false]);
console.log('Passed: expand/collapse, complete print copy, and restoration after print or cancellation.');
