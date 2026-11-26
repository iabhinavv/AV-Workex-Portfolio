/* Short, one-time entrances; primary content stays visible without this script. */
(() => {
  'use strict';
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const targets='.timeline-entry .experience-tile,.timeline-entry .timeline-date,.work-card,.work-visual,.project,.locations>li,.education-entry,.certificate,.sop-link,.stats>div,.chapter-contact,.sop-content>h2,.sop-content>.table-scroll';
  let entrances,journey;
  function refresh(initial=false){
    entrances?.disconnect();
    journey?.disconnect();
    document.querySelectorAll('.motion-pending').forEach(element=>element.classList.remove('motion-pending'));
    document.querySelectorAll('.timeline').forEach(element=>element.classList.remove('timeline-active'));
    if(reduced.matches||!('IntersectionObserver' in window))return;
    if(initial)document.querySelector('.intro,.document-header')?.classList.add('motion-enter');
    entrances=new IntersectionObserver(entries=>{
      entries.filter(entry=>entry.isIntersecting).forEach((entry,index)=>{
        entry.target.style.setProperty('--enter-delay',Math.min(index,3)*65+'ms');
        entry.target.classList.remove('motion-pending');
        entry.target.classList.add('motion-enter');
        entrances.unobserve(entry.target);
      });
    },{threshold:.08,rootMargin:'0px 0px -20px 0px'});
    document.querySelectorAll(targets).forEach(element=>{
      if(!element.classList.contains('motion-enter')){
        element.classList.add('motion-pending');
        entrances.observe(element);
      }
    });
    journey=new IntersectionObserver(entries=>{
      entries.forEach(entry=>entry.target.classList.toggle('timeline-active',entry.isIntersecting));
    });
    document.querySelectorAll('.timeline').forEach(element=>journey.observe(element));
  }
  document.addEventListener('workex:page-ready',()=>refresh());
  reduced.addEventListener('change',()=>refresh());
  refresh(true);
})();
