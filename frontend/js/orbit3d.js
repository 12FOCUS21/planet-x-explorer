/* Planet X Explorer / orbital illustration.
   Decorative interactive canvas render — NOT a scientific observation. */
(() => {
  function init() {
    const canvas=document.getElementById('orbit3d');
    if(!canvas || !canvas.getContext) return;
    const ctx=canvas.getContext('2d');
    if(!ctx) return;
    const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
    let width=0,height=0, phase=.45, pointer=0, visible=false, frame=0, last=0;
    const clamp=(v,min,max)=>Math.max(min,Math.min(max,v));
    function resize() {
      const rect=canvas.getBoundingClientRect();
      width=rect.width;height=rect.height;
      const d=clamp(devicePixelRatio||1,1,2);
      canvas.width=Math.max(1,Math.round(width*d));canvas.height=Math.max(1,Math.round(height*d));
      ctx.setTransform(d,0,0,d,0,0);
      draw();
    }
    function ring(cx,cy,r,start,end,alpha,thickness) {
      ctx.save();ctx.translate(cx,cy);ctx.rotate(-.32);
      ctx.lineWidth=thickness;
      ctx.strokeStyle=`rgba(180,235,244,${alpha})`;
      ctx.beginPath();ctx.ellipse(0,0,r*1.58,r*.39,0,start,end);ctx.stroke();
      ctx.lineWidth=1;
      ctx.strokeStyle=`rgba(255,197,151,${alpha*.58})`;
      ctx.beginPath();ctx.ellipse(0,0,r*1.77,r*.46,0,start,end);ctx.stroke();ctx.restore();
    }
    function draw() {
      if(!width||!height)return;
      ctx.clearRect(0,0,width,height);
      const cx=width*.50,cy=height*.49,r=Math.min(width,height)*.305;
      const halo=ctx.createRadialGradient(cx,cy,r*.45,cx,cy,r*1.7);
      halo.addColorStop(0,'rgba(61,189,211,.24)');halo.addColorStop(.65,'rgba(56,145,194,.11)');halo.addColorStop(1,'rgba(16,46,78,0)');
      ctx.fillStyle=halo;ctx.fillRect(0,0,width,height);
      // Distant inclined orbital ring behind the sphere.
      ring(cx,cy,r,Math.PI,Math.PI*2,.48,3.1);
      // Atmospheric rim.
      ctx.beginPath();ctx.arc(cx,cy,r+2,0,Math.PI*2);
      ctx.fillStyle='rgba(77,197,220,.2)';ctx.fill();
      // Spherical volume / terminator and a directional light.
      const globe=ctx.createRadialGradient(cx-r*.44,cy-r*.5,r*.05,cx+r*.3,cy+r*.25,r*1.38);
      globe.addColorStop(0,'#c5eff0');globe.addColorStop(.14,'#5db6ce');
      globe.addColorStop(.40,'#226a8e');globe.addColorStop(.68,'#173a62');
      globe.addColorStop(.91,'#071426');globe.addColorStop(1,'#030814');
      ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.fillStyle=globe;ctx.fill();
      ctx.save();ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.clip();
      // Rotating bands, slightly warped around the visible sphere.
      for(let i=-5;i<=5;i++) {
        const Y=i*r*.17, edge=Math.sqrt(Math.max(0,r*r-Y*Y));
        const wave=Math.sin(phase*1.7+i*.76)*r*.064;
        ctx.strokeStyle=i%3===0?'rgba(198,232,223,.17)':'rgba(100,198,226,.15)';
        ctx.lineWidth= i%3===0?9:4;
        ctx.beginPath();ctx.moveTo(cx-edge-10,cy+Y+wave);
        ctx.bezierCurveTo(cx-r*.45,cy+Y+wave-r*.04,cx+r*.24,cy+Y+wave+r*.06,cx+edge+10,cy+Y-wave);
        ctx.stroke();
      }
      const shading=ctx.createLinearGradient(cx-r,cy,cx+r,cy);
      shading.addColorStop(0,'rgba(255,255,255,.035)');shading.addColorStop(.52,'rgba(0,0,0,0)');shading.addColorStop(1,'rgba(0,1,15,.44)');
      ctx.fillStyle=shading;ctx.fillRect(cx-r,cy-r,r*2,r*2);
      ctx.restore();
      // Forward section passes in front of the sphere.
      ring(cx,cy,r,0,Math.PI,.72,3.2);
      // Orbital telemetry point on the outer ellipse.
      const a=phase*.5+1.2;
      const sx=cx+Math.cos(a)*r*1.58,sy=cy+Math.sin(a)*r*.39;
      ctx.beginPath();ctx.arc(sx,sy,3,0,Math.PI*2);ctx.fillStyle='#d7fb8e';ctx.shadowColor='#cafa70';ctx.shadowBlur=10;ctx.fill();ctx.shadowBlur=0;
    }
    function tick(timestamp){
      frame=0;
      if(!visible||document.hidden||reduced.matches)return;
      if(timestamp-last>33){phase+=.008;draw();last=timestamp;}
      frame=requestAnimationFrame(tick);
    }
    canvas.parentElement.addEventListener('pointermove', e=>{
      const box=canvas.getBoundingClientRect();pointer=(e.clientX-box.left)/Math.max(1,box.width)-.5;
      phase+=pointer*.02;if(reduced.matches)draw();
    });
    new ResizeObserver(resize).observe(canvas);
    const observer=new IntersectionObserver(entries=>{
      const next=entries[0].isIntersecting;
      visible=next;
      if(next){resize();if(!frame&&!reduced.matches)frame=requestAnimationFrame(tick);}
      else if(frame){cancelAnimationFrame(frame);frame=0;}
    });
    observer.observe(canvas);
    document.addEventListener('visibilitychange',()=>{if(!document.hidden&&visible&&!frame&&!reduced.matches)frame=requestAnimationFrame(tick);});
    reduced.addEventListener('change',()=>{draw();if(visible&&!reduced.matches&&!frame)frame=requestAnimationFrame(tick);});
    resize();
  }
  document.addEventListener('DOMContentLoaded',init);
})();
