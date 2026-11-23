/* Keep the globe mounted in its hero; only its camera and the page copy change. */
(() => {
  'use strict';
  const groups=JSON.parse(document.querySelector('#footprint-data').textContent);
  const routes=new Map([['index.html','home'],...groups.map(g=>[g.id+'.html',g.id])]);
  const cache=new Map();
  const main=document.querySelector('#main');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  let busy=false,pendingPop=null;

  function pageId(url){return routes.get(url.pathname.split('/').pop()||'index.html');}
  async function readPage(url){
    const key=url.pathname;
    if(!cache.has(key)){
      const controller=new AbortController();
      const timeout=setTimeout(()=>controller.abort(),15000);
      try{
        const response=await fetch(url.href,{signal:controller.signal});
        if(!response.ok) throw new Error('Page unavailable');
        const text=await response.text();
        const parsed=new DOMParser().parseFromString(text,'text/html');
        if(parsed.body.dataset.page!==pageId(url)||!parsed.querySelector('#main .globe-figure')) throw new Error('Unexpected page');
        cache.set(key,text);
      }finally{clearTimeout(timeout);}
    }
    return new DOMParser().parseFromString(cache.get(key),'text/html');
  }
  function returnToGlobe(){
    if(reduced.matches){window.scrollTo({top:0,behavior:'instant'});return Promise.resolve();}
    window.scrollTo({top:0,behavior:'smooth'});
    const start=performance.now();
    return new Promise(resolve=>{
      function check(now){
        if(window.scrollY<2||now-start>750) resolve();
        else requestAnimationFrame(check);
      }
      requestAnimationFrame(check);
    });
  }
  function copySurfaces(){
    return [main.querySelector('.intro'),...Array.from(main.children).filter(child=>!child.classList.contains('hero'))];
  }
  function fadeCopy(visible){
    if(reduced.matches)return [];
    return copySurfaces().filter(element=>element.animate).map(element=>element.animate(
      [{opacity:visible?0:1},{opacity:visible?1:0}],
      {duration:visible?200:140,easing:'ease-out',fill:'both'}
    ));
  }
  function activateNavigation(id){
    document.body.dataset.page=id;
    document.querySelectorAll('#main-nav a').forEach(anchor=>{
      if(pageId(new URL(anchor.href))===id) anchor.setAttribute('aria-current','page');
      else anchor.removeAttribute('aria-current');
    });
  }
  async function navigate(url,{push=true,animated=true}={}){
    if(busy)return;
    busy=true;
    let succeeded=false;
    const animations=[];
    main.setAttribute('aria-busy','true');
    document.body.dataset.routePhase='returning';
    const surfaces=[main,document.querySelector('.topbar'),document.querySelector('.footer')];
    surfaces.forEach(element=>{element.inert=true;});
    document.querySelector('#main-nav').classList.remove('open');
    document.querySelector('.menu-toggle').setAttribute('aria-expanded','false');
    try{
      const [next,globe]=await Promise.all([readPage(url),window.workexGlobeReady,returnToGlobe()]);
      const id=pageId(url);
      const figure=document.querySelector('.globe-figure');
      const shouldAnimate=animated&&!reduced.matches;
      document.body.dataset.routePhase='focusing';
      const outgoing=shouldAnimate?fadeCopy(false):[];
      animations.push(...outgoing);
      await Promise.all([
        globe?.flyTo(id,{milliseconds:shouldAnimate?850:0,spin:id==='home'}),
        ...outgoing.map(animation=>animation.finished.catch(()=>{}))
      ]);
      const destination=next.querySelector('#main');
      const hero=main.querySelector('.hero');
      const nextHero=destination.querySelector('.hero');
      hero.querySelector('.intro').replaceWith(nextHero.querySelector('.intro'));
      hero.className=nextHero.className;
      Array.from(main.children).filter(child=>child!==hero).forEach(child=>child.remove());
      main.append(...Array.from(destination.children).filter(child=>child!==nextHero));
      figure.setAttribute('aria-label',id==='home'?'Career footprint overview':groups.find(g=>g.id===id).title+' geographic footprint');
      document.title=next.title;
      document.querySelector('meta[name="description"]').content=next.querySelector('meta[name="description"]').content;
      activateNavigation(id);
      if(push&&!pendingPop)history.pushState({workex:true},'',url.href);
      globe?.resize();
      document.body.dataset.routePhase='revealing';
      const incoming=shouldAnimate?fadeCopy(true):[];
      animations.push(...incoming);
      await Promise.all(incoming.map(animation=>animation.finished.catch(()=>{})));
      if(url.hash){
        document.getElementById(decodeURIComponent(url.hash.slice(1)))?.scrollIntoView({behavior:'instant',block:'start'});
      }
      succeeded=true;
    }catch(error){
      // Opening files directly or a failed fetch still follows the original HTML link.
      window.location.assign(url.href);
    }finally{
      animations.forEach(animation=>animation.cancel());
      surfaces.forEach(element=>{element.inert=false;});
      if(succeeded) main.focus({preventScroll:true});
      main.removeAttribute('aria-busy');
      document.body.dataset.routePhase='idle';
      busy=false;
      if(pendingPop){
        const destination=pendingPop;pendingPop=null;
        navigate(destination,{push:false,animated:false});
      }
    }
  }
  document.addEventListener('click',event=>{
    const anchor=event.target.closest?.('a[href]');
    if(!anchor||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey||anchor.target||anchor.hasAttribute('download'))return;
    const url=new URL(anchor.href);
    if(url.origin!==location.origin||!pageId(url))return;
    if(url.pathname===location.pathname&&url.hash)return;
    event.preventDefault();
    navigate(url);
  });
  window.addEventListener('popstate',()=>{
    const url=new URL(location.href);
    if(busy) pendingPop=url;
    else navigate(url,{push:false,animated:false});
  });
  if('scrollRestoration' in history) history.scrollRestoration='manual';
})();
