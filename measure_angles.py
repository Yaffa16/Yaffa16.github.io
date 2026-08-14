import os
from playwright.sync_api import sync_playwright
ROOT = "/home/claude/site/Yaffa16.github.io-main"

JS = """(function(){
  var stage = document.getElementById('stage');
  var P = parseFloat(getComputedStyle(stage).perspective);   // read it live
  var cs = [...document.querySelectorAll('.uv-card')]
    .filter(c => parseFloat(c.style.opacity) > 0.9);
  cs.sort((a,b) => parseInt(b.style.zIndex) - parseInt(a.style.zIndex));

  function quad(el){
    var w = el.offsetWidth, h = el.offsetHeight;
    var m = new DOMMatrix(getComputedStyle(el).transform);
    return [[-w/2,-h/2],[w/2,-h/2],[w/2,h/2],[-w/2,h/2]].map(function(p){
      var v = m.transformPoint(new DOMPoint(p[0], p[1], 0));
      var s = P/(P - v.z);          // perspective divide, live P
      return [v.x*s, v.y*s];
    });
  }
  function ang(a,b,c){
    var v1=[a[0]-b[0],a[1]-b[1]], v2=[c[0]-b[0],c[1]-b[1]];
    var d=(v1[0]*v2[0]+v1[1]*v2[1])/(Math.hypot(v1[0],v1[1])*Math.hypot(v2[0],v2[1]));
    return Math.acos(Math.max(-1,Math.min(1,d)))*180/Math.PI;
  }
  var all = cs.slice(0,6).map(function(el){
    var q = quad(el);
    return [ang(q[3],q[0],q[1]), ang(q[0],q[1],q[2]), ang(q[1],q[2],q[3]), ang(q[2],q[3],q[0])]
             .map(function(a){return +a.toFixed(1);});
  });
  var centres = cs.slice(0,6).map(function(c){
    var r=c.getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2];
  });
  var path=[];
  for (var i=0;i<centres.length-1;i++){
    var dx=centres[i+1][0]-centres[i][0], dy=centres[i][1]-centres[i+1][1];
    path.push(+(Math.atan2(dy,dx)*180/Math.PI).toFixed(1));
  }
  var flat=[].concat.apply([],all);
  return {perspective:P, corners:all[0], cornerMin:Math.min.apply(null,flat).toFixed(1),
          cornerMax:Math.max.apply(null,flat).toFixed(1), path:path};
})()"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(viewport={"width":1280,"height":768}).new_page()
    pg.goto("file://"+os.path.join(ROOT,"index.html"), wait_until="load")
    pg.wait_for_timeout(2600)
    pg.mouse.move(640, 752); pg.wait_for_timeout(400)
    m = pg.evaluate(JS)
    print("perspective read from CSS:", m["perspective"])
    print("front pane corners:", m["corners"])
    print("corner range across 6 panes: %s - %s   (reference 88.4 - 94.9)" % (m["cornerMin"], m["cornerMax"]))
    print("path angle per step:", m["path"], "  (reference 46.2)")
    b.close()
