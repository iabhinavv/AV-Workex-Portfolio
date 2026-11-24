/* Shared navigation and a non-interactive spherical globe. No WebGL required. */
(() => {
  'use strict';
  let resolveGlobe;
  window.workexGlobeReady = new Promise(resolve => { resolveGlobe = resolve; });
  const canvas = document.querySelector('#globe');
  const fallback = () => {
    canvas.hidden = true;
    document.querySelector('.globe-fallback').hidden = false;
  };
  const script = src => new Promise((resolve, reject) => {
    const tag = document.createElement('script');
    tag.src = src;
    tag.onload = resolve;
    tag.onerror = reject;
    document.head.append(tag);
  });
  const start = async () => {
    try {
      const ctx = canvas.getContext('2d');
      if (!ctx) { fallback(); resolveGlobe(null); return; }
      await Promise.all([
        script('assets/vendor/d3-array.min.js').then(() => script('assets/vendor/d3-geo.min.js')),
        script('assets/vendor/topojson-client.min.js'),
        script('assets/vendor/world-data.js')
      ]);
      resolveGlobe(createGlobe(ctx));
    } catch (error) {
      fallback();
      resolveGlobe(null);
      console.warn('Globe illustration fallback:', error.message);
    }
  };

  function createGlobe(ctx) {
    const groups = JSON.parse(document.querySelector('#footprint-data').textContent);
    let page = document.body.dataset.page;
    let home = page === 'home';
    let locations = home ? groups.flatMap(g => g.locations) : groups.find(g => g.id === page).locations;
    const land = topojson.feature(window.WORKEX_WORLD, window.WORKEX_WORLD.objects.countries);
    const graticule = d3.geoGraticule10();
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    let width, height, radius, frame = 0, lastTime = 0, transitionStart = 0;
    let duration = 1450, complete;
    let spinning = true, paused = motion.matches, camera, target, from;
    let prior;
    try { prior = JSON.parse(sessionStorage.getItem('workex-camera')); } catch { /* Storage is optional. */ }
    if (!prior || !['lon', 'lat', 'zoom'].every(k => Number.isFinite(prior[k]))) prior = null;
    if (prior) {
      prior.zoom=Math.max(.8,Math.min(1.22,prior.zoom));
      prior.offsetX=0;prior.offsetY=0;
    }

    // Keep the full sphere visible instead of magnifying it into a rectangular map.
    function focus() {
      if (home) return {lon: 32, lat: 16, zoom: 1, offsetX: 0, offsetY: 0};
      let lon, lat;
      if (page === 'hsbc') { lon = 12; lat = 22; }
      else {
        const vector = locations.reduce((v, [,x,y]) => {
          const a = x * Math.PI / 180, b = y * Math.PI / 180;
          return [v[0] + Math.cos(b) * Math.cos(a), v[1] + Math.cos(b) * Math.sin(a), v[2] + Math.sin(b)];
        }, [0,0,0]);
        lon = Math.atan2(vector[1], vector[0]) * 180 / Math.PI;
        lat = Math.atan2(vector[2], Math.hypot(vector[0], vector[1])) * 180 / Math.PI;
      }
      return {lon, lat, zoom: page==='hsbc'?1.08:1.22, offsetX:0, offsetY:0};
    }
    function resize() {
      const bounds = canvas.getBoundingClientRect();
      if (width === bounds.width && height === bounds.height) return;
      width = bounds.width; height = bounds.height;
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(width*dpr); canvas.height = Math.round(height*dpr);
      ctx.setTransform(dpr,0,0,dpr,0,0);
      radius = Math.min(width,height) * .37;
      target = focus();
      if (camera) {
        if (home) target.lon = camera.lon;
        from = {...target};
        duration = 0;
      } else {
        from = prior ? { ...prior, offsetX: prior.offsetX || 0, offsetY: prior.offsetY || 0 } : {lon:32, lat:16, zoom:1, offsetX:0, offsetY:0};
      }
      // Keep navigation continuity, while reduced motion always starts at the destination.
      camera = motion.matches ? {...target} : {...from};
      transitionStart = performance.now();
      schedule();
    }
    function schedule() { if (!frame && !document.hidden) frame = requestAnimationFrame(draw); }
    function interpolate(a,b,t) {
      let delta = b.lon-a.lon;
      delta = ((delta+540)%360)-180;
      return {lon:a.lon+delta*t,lat:a.lat+(b.lat-a.lat)*t,zoom:a.zoom+(b.zoom-a.zoom)*t,offsetX:a.offsetX+(b.offsetX-a.offsetX)*t,offsetY:a.offsetY+(b.offsetY-a.offsetY)*t};
    }
    function path(ctx, projection, feature, fill, stroke, lineWidth=1) {
      ctx.beginPath();
      d3.geoPath(projection,ctx)(feature);
      if (fill) {ctx.fillStyle=fill;ctx.fill();}
      if (stroke) {ctx.strokeStyle=stroke;ctx.lineWidth=lineWidth;ctx.stroke();}
    }
    function draw(now) {
      frame = 0;
      const elapsed = motion.matches || !duration ? 1 : Math.min(1, (now-transitionStart)/duration);
      if (elapsed < 1) {
        camera = interpolate(from,target,elapsed*elapsed*(3-2*elapsed));
      } else if (complete) {
        camera = {...target};
      } else if (home && !paused) {
        if (lastTime) camera.lon = (camera.lon + Math.min(50,now-lastTime)*.004)%360;
      } else if (!home || motion.matches) camera = {...target};
      lastTime = now;
      const scale = radius*camera.zoom;
      const cx=width/2+camera.offsetX*scale, cy=height/2+camera.offsetY*scale;
      const projection = d3.geoOrthographic().rotate([-camera.lon,-camera.lat]).translate([cx,cy]).scale(scale).clipAngle(90).precision(.5);
      ctx.clearRect(0,0,width,height);
      const ocean=ctx.createRadialGradient(cx-scale*.3,cy-scale*.3,0,cx,cy,scale);
      ocean.addColorStop(0,'#214a62');ocean.addColorStop(.6,'#112e42');ocean.addColorStop(1,'#081927');
      path(ctx,projection,{type:'Sphere'},ocean,'#669eaf88',1);
      path(ctx,projection,graticule,null,'#91c4d326',.6);
      path(ctx,projection,land,'#2e5668','#8cbdc688',.6);
      const shade=ctx.createRadialGradient(cx-scale*.27,cy-scale*.22,scale*.3,cx+scale*.2,cy+scale*.1,scale*1.05);
      shade.addColorStop(0,'#00111d00');shade.addColorStop(.7,'#00081222');shade.addColorStop(1,'#000913bb');
      path(ctx,projection,{type:'Sphere'},shade,null);
      const labels=[];
      const markers=[];
      locations.forEach(([name,lon,lat,,status]) => {
        const planned=status==='planned';
        const distance=d3.geoDistance([camera.lon,camera.lat],[lon,lat]);
        const back=distance>Math.PI/2;
        if (home && back) return;
        const [x,y]=projection([lon,lat]);
        ctx.save();
        ctx.strokeStyle=planned?'#74c7d9':back?'#b1cfdc':'#f0b478';
        ctx.fillStyle=back?'#102e3d':'#ffd19d';
        ctx.lineWidth=1;
        ctx.setLineDash(planned?[4,3]:back?[2,2]:[]);
        ctx.beginPath();ctx.arc(x,y,back?5:4.5,0,Math.PI*2);ctx.stroke();
        ctx.setLineDash([]);
        if (!back&&!planned) {ctx.beginPath();ctx.arc(x,y,2,0,Math.PI*2);ctx.fill();}
        ctx.restore();
        const highlights=groups.find(group=>group.id===page)?.highlights[name]||[];
        markers.push({name,x,y,back,planned,highlights});
        if(!home) labels.push({name:planned?name+' · 2027':name,x,y,back,planned,highlights});
      });
      // A two-line label gives each place its work highlights without a label box.
      const labelBounds=[];
      const rowHeight=Math.min(34,(height-16)/Math.max(1,labels.length));
      labels.sort((a,b)=>a.y-b.y);
      const labelSpan=labels.length?Math.min(height-16,Math.max(labels.length*rowHeight,labels.at(-1).y-labels[0].y+28)):0;
      const labelStart=labels.length?Math.max(8,Math.min(height-8-labelSpan,(labels[0].y+labels.at(-1).y-labelSpan)/2)):0;
      labels.forEach((label,index)=>{
        const subtitle=label.highlights.join(' · ');
        ctx.font='12px ui-monospace, Menlo, monospace';
        const nameWidth=ctx.measureText(label.name).width;
        ctx.font='11px ui-sans-serif, system-ui, sans-serif';
        const tw=Math.max(nameWidth,ctx.measureText(subtitle).width);
        let lx=label.x<cx?label.x-tw-12:label.x+12;
        lx=Math.max(8,Math.min(width-tw-8,lx));
        const ly=labelStart+index*(labelSpan-28)/Math.max(1,labels.length-1);
        const overSphere=Math.hypot(lx+tw/2-cx,ly+14-cy)<scale;
        labelBounds.push({name:label.name,x:lx,y:ly,width:tw,height:28});
        ctx.beginPath();ctx.moveTo(label.x,label.y);ctx.lineTo(label.x<cx?lx+tw:lx,ly+8);
        ctx.strokeStyle=label.planned?'#176c8188':label.back?'#587c8488':'#9b542788';ctx.lineWidth=.6;ctx.stroke();
        ctx.font='12px ui-monospace, Menlo, monospace';
        ctx.lineJoin='round';ctx.lineWidth=2;ctx.strokeStyle=overSphere?'#102e3ddd':'#f5f8faee';
        ctx.strokeText(label.name,lx,ly+11);
        ctx.fillStyle=overSphere?(label.planned?'#95d2e0':label.back?'#c5d5dd':'#f2d1ad'):(label.planned?'#156579':label.back?'#536e76':'#663f28');ctx.fillText(label.name,lx,ly+11);
        ctx.font='11px ui-sans-serif, system-ui, sans-serif';
        ctx.strokeText(subtitle,lx,ly+25);
        ctx.fillStyle=overSphere?'#e1edf3':'#314c5d';ctx.fillText(subtitle,lx,ly+25);
      });
      canvas.dataset.ready='true';
      canvas.dataset.camera=JSON.stringify(camera);
      canvas.dataset.markers=JSON.stringify(markers);
      canvas.dataset.labels=JSON.stringify(labelBounds);
      canvas.dataset.transition=elapsed<1?'moving':'settled';
      if (elapsed === 1 && complete) {
        const finish = complete;
        complete = null;
        finish();
      }
      if ((elapsed<1 && !motion.matches)||(home&&!paused&&!motion.matches)) schedule();
    }
    function updateMotion() {
      paused=motion.matches||!spinning;
      lastTime=0;schedule();
    }
    motion.addEventListener('change',updateMotion);
    document.addEventListener('visibilitychange',()=>{
      lastTime=0;
      if(document.hidden){cancelAnimationFrame(frame);frame=0;}else schedule();
    });
    window.addEventListener('pagehide',()=>{
      try {sessionStorage.setItem('workex-camera',JSON.stringify(camera));} catch { /* Navigation works without storage. */ }
    });
    // Canvas receives no pointer, touch, wheel or keyboard gesture handlers.
    new ResizeObserver(resize).observe(canvas.parentElement);
    updateMotion();resize();
    return {
      resize,
      flyTo(id, {milliseconds=1200, spin=true}={}) {
        if (complete) {complete();complete=null;}
        page=id;home=id==='home';
        locations=home?groups.flatMap(g=>g.locations):groups.find(g=>g.id===id).locations;
        target=focus();from={...camera};
        spinning=spin;
        duration=motion.matches?0:milliseconds;
        transitionStart=performance.now();
        const figure=document.querySelector('.globe-figure');
        if(figure) figure.setAttribute('aria-label',home?'Career footprint overview':groups.find(g=>g.id===id).title+' geographic footprint');
        updateMotion();
        return new Promise(resolve=>{complete=resolve;schedule();});
      }
    };
  }
  if ('requestIdleCallback' in window) requestIdleCallback(start,{timeout:700});
  else setTimeout(start,0);
})();
