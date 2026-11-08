const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),M=require('./dist/assets/squat-model.js');
let saved=null;
for(const lang of ['en','ru']){
 const html=fs.readFileSync(`dist/${lang}/squat.html`,'utf8'),nodes={};for(const m of html.matchAll(/id="([^"]+)"/g))nodes[m[1]]={value:0,dataset:{unit:''},handlers:{},attrs:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,v){this.handlers[k]=v}};
 nodes.phase.value=50;let nextFrame;const handlers={},context={window:{SquatModel:M,addEventListener:(k,f)=>handlers[k]=f},document:{getElementById:id=>nodes[id],addEventListener(){}},sessionStorage:{getItem:()=>saved,setItem:(k,v)=>saved=v},requestAnimationFrame:f=>{nextFrame=f;return 1},cancelAnimationFrame:()=>{nextFrame=null}};
 vm.runInNewContext(html.match(/<script>(window.SQUAT_COPY=.*?)<\/script>/s)[1],context);
 vm.runInNewContext(fs.readFileSync('dist/assets/squat-ui.js','utf8'),context);
 assert(nodes.scene.innerHTML.includes('<circle'));assert(nodes.chart.innerHTML.includes('<path'));assert(nodes.hipMoment.textContent.includes('N·m'));
 nodes.load.value=90;nodes.load.handlers.input();assert(nodes.loadOut.textContent.startsWith('90'));nodes.mode.value='static';nodes.mode.handlers.change();nodes.phase.value=0;nodes.phase.handlers.input();assert.equal(parseFloat(nodes.hipMoment.textContent),0);
 nodes.play.handlers.click();assert.equal(nodes.play.attrs['aria-pressed'],'true');nextFrame(100);nextFrame(200);assert(+nodes.phase.value>0);
 nodes.play.handlers.click();assert.equal(nodes.play.attrs['aria-pressed'],'false');handlers.pagehide();assert.equal(JSON.parse(saved).p.load,90);
 nodes.reset.handlers.click();assert.equal(+nodes.load.value,40);assert.equal(+nodes.phase.value,50);assert.equal(nodes.mode.value,'dynamic');
}
console.log('PASS: EN/RU actual page configuration, SVG render, load/mode/scrub, playback, state storage, reset.');
