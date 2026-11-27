/* Expandable SOP reading and a complete print copy without changing reading preferences. */
(() => {
  'use strict';
  const details=Array.from(document.querySelectorAll('.sop-content details'));
  let readingState=null;
  function preparePrint(){
    if(readingState)return;
    readingState=details.map(element=>element.open);
    details.forEach(element=>{element.open=true;});
  }
  function restoreReading(){
    if(!readingState)return;
    details.forEach((element,index)=>{element.open=readingState[index];});
    readingState=null;
  }
  document.querySelector('[data-sop-action="expand"]')?.addEventListener('click',()=>{
    details.forEach(element=>{element.open=true;});
  });
  document.querySelector('[data-sop-action="collapse"]')?.addEventListener('click',()=>{
    details.forEach(element=>{element.open=false;});
  });
  document.querySelector('[data-sop-action="print"]')?.addEventListener('click',()=>{
    preparePrint();
    window.print();
  });
  window.addEventListener('beforeprint',preparePrint);
  window.addEventListener('afterprint',restoreReading);
  matchMedia('print').addEventListener('change',event=>{
    if(event.matches)preparePrint();else restoreReading();
  });
})();
