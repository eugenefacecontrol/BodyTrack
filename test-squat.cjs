const assert=require('node:assert/strict'),M=require('./dist/assets/squat-model.js');
const p=M.parameters(),norm=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
for(const s of M.cycle(p)){
 assert(Math.abs(norm(s.ankle,s.knee)-p.shin)<1e-12);
 assert(Math.abs(norm(s.knee,s.hip)-p.thigh)<1e-12);
 assert(Math.abs(norm(s.hip,s.shoulder)-p.torso)<1e-12);
 assert(Math.abs(s.bodies.reduce((n,v)=>n+v.m,0)-p.mass-p.load)<1e-10);
 for(const v of [...Object.values(s.moments),s.Fx,s.Fy,s.com.x])assert(Number.isFinite(v));
}
let s=M.state(p,0,'static');assert(Math.abs(s.moments.hip)<1e-10);assert(Math.abs(s.moments.knee)<1e-10);assert(Math.abs(s.Fy-(p.mass+p.load)*M.G)<1e-9);
s=M.state(p,.5,'static');assert(Math.abs(s.angles.knee-p.depth)<1e-10);assert(Math.abs(s.cop-s.com.x)<1e-10);
const upper=s.bodies.filter(v=>['upper','bar'].includes(v.name));const expected=upper.reduce((n,v)=>n+v.m*M.G*(v.c.x-s.hip.x),0)/2;assert(Math.abs(expected-s.moments.hip)<1e-10);
const samePose=M.pose(p,.8),loaded={...p,load:80},sameLoaded=M.pose(loaded,.8);assert(samePose.angles.trunk!==sameLoaded.angles.trunk);
const slow=M.parameters({period:12}),fast=M.parameters({period:2});for(const k of ['hip','knee','ankle']){const stat=M.state(slow,.25,'static').moments[k],ds=M.state(slow,.25).moments[k]-stat,df=M.state(fast,.25).moments[k]-stat;assert(Math.abs(df-ds*36)<.01);}
assert(Math.abs(M.state(p,.2).moments.hip-M.state(p,1.2).moments.hip)<.001);
assert.throws(()=>M.parameters({mass:NaN}));assert.throws(()=>M.parameters({period:0}));
let limited=0;for(const depth of [30,90,145])for(const thigh of [.3,.65])for(const shinAngle of [5,45])for(const load of [0,200])for(const q of [0,.25,.5,.75,1]){const a=M.state(M.parameters({depth,thigh,shinAngle,load}),q);for(const n of Object.values(a.moments))assert(Number.isFinite(n));if(!a.valid)limited++;}assert(limited>0);
const double=M.state(M.parameters({mass:160,load:80}),.3),single=M.state(p,.3);for(const k of ['hip','knee','ankle'])assert(Math.abs(double.moments[k]-2*single.moments[k])<.001);
console.log('PASS: squat geometry, mass, free-body moments, COP, inertial T^-2 scaling, limits and 120 parameter states.');
