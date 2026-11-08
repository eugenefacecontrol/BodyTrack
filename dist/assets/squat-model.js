/* Sagittal, prescribed-motion inverse dynamics. See docs/squat-model.md. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.SquatModel=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const G=9.81,rad=Math.PI/180;
const defaults={mass:80,load:40,shin:.43,thigh:.45,torso:.60,depth:115,shinAngle:30,period:5};
const bounds={mass:[40,160],load:[0,200],shin:[.3,.6],thigh:[.3,.65],torso:[.4,.85],depth:[30,145],shinAngle:[5,45],period:[2,12]};
function parameters(input={}){const p={...defaults,...input};for(const k of Object.keys(defaults)){if(!Number.isFinite(p[k])||p[k]<bounds[k][0]||p[k]>bounds[k][1])throw Error('Invalid '+k);}return p;}
const add=(a,b)=>({x:a.x+b.x,y:a.y+b.y});
const lerp=(a,b,t)=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t});
function pose(p,u){
 const a=p.shinAngle*rad*u,b=(p.depth-p.shinAngle)*rad*u;
 const ankle={x:0,y:.08},knee=add(ankle,{x:p.shin*Math.sin(a),y:p.shin*Math.cos(a)}),hip=add(knee,{x:-p.thigh*Math.sin(b),y:p.thigh*Math.cos(b)});
 const shankCOM=lerp(ankle,knee,.5),thighCOM=lerp(knee,hip,.5),mS=p.mass*.10,mT=p.mass*.20,mU=p.mass*.67,mF=p.mass*.03;
 const numerator=-(mS*shankCOM.x+mT*thighCOM.x+(mU+p.load)*hip.x);
 const ratio=numerator/(p.torso*(mU*.55+p.load));
 const gamma=Math.asin(Math.max(-Math.sin(70*rad),Math.min(Math.sin(70*rad),ratio)));
 const shoulder=add(hip,{x:p.torso*Math.sin(gamma),y:p.torso*Math.cos(gamma)}),upperCOM=lerp(hip,shoulder,.55);
 const bodies=[{name:'foot',m:mF,c:{x:.055,y:.04},angle:0,I:0},{name:'shank',m:mS,c:shankCOM,angle:Math.PI/2-a,I:mS*p.shin**2/12},{name:'thigh',m:mT,c:thighCOM,angle:Math.PI/2+b,I:mT*p.thigh**2/12},{name:'upper',m:mU,c:upperCOM,angle:Math.PI/2-gamma,I:mU*p.torso**2/12},{name:'bar',m:p.load,c:shoulder,angle:0,I:0}];
 const total=p.mass+p.load,com={x:bodies.reduce((s,v)=>s+v.m*v.c.x,0)/total,y:bodies.reduce((s,v)=>s+v.m*v.c.y,0)/total};
 return {ankle,knee,hip,shoulder,com,bodies,angles:{ankle:a/rad,knee:(a+b)/rad,hip:(b+gamma)/rad,trunk:gamma/rad},limited:Math.abs(ratio)>Math.sin(70*rad)};
}
function state(p,phase,mode='dynamic'){
 if(!Number.isFinite(phase)||!['dynamic','static'].includes(mode))throw Error('Invalid state');
 // phase is a full repetition (0..1); smooth cosine descent and ascent.
 const t=phase*p.period,h=.0005;
 const at=time=>pose(p,(1-Math.cos(2*Math.PI*time/p.period))/2);
 const s=at(t),before=at(t-h),after=at(t+h);
 const bodies=s.bodies.map((v,i)=>({...v,ax:mode==='static'?0:(after.bodies[i].c.x-2*v.c.x+before.bodies[i].c.x)/h**2,ay:mode==='static'?0:(after.bodies[i].c.y-2*v.c.y+before.bodies[i].c.y)/h**2,alpha:mode==='static'?0:(after.bodies[i].angle-2*v.angle+before.bodies[i].angle)/h**2}));
 function moment(joint,names){return .5*bodies.filter(v=>names.includes(v.name)).reduce((sum,v)=>sum+(v.c.x-joint.x)*v.m*(G+v.ay)-(v.c.y-joint.y)*v.m*v.ax+v.I*v.alpha,0);}
 const moments={hip:moment(s.hip,['upper','bar']),knee:moment(s.knee,['thigh','upper','bar']),ankle:moment(s.ankle,['shank','thigh','upper','bar'])};
 const Fy=bodies.reduce((sum,v)=>sum+v.m*(G+v.ay),0),Fx=bodies.reduce((sum,v)=>sum+v.m*v.ax,0);
 const totalMoment=bodies.reduce((sum,v)=>sum+v.c.x*v.m*(G+v.ay)-v.c.y*v.m*v.ax+v.I*v.alpha,0),cop=Fy>0?totalMoment/Fy:null;
 return {...s,bodies,moments,Fx,Fy,cop,valid:!s.limited&&s.hip.y>=.08&&Fy>0&&cop>=-.09&&cop<=.20,phase};
}
function cycle(p,mode='dynamic',count=101){return Array.from({length:count},(_,i)=>state(p,i/(count-1),mode));}
return {G,defaults,bounds,parameters,pose,state,cycle};
});
