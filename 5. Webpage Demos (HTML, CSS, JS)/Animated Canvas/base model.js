// GRAVITY MODEL
// https://www.desmos.com/calculator/uz5ryiujsz

let canv_width = 1500; //5px = 1 ft, rad ~ 1000/2/5 = 100ft

let room_rad = 90; //ft
let scalar = canv_width/2*0.9/room_rad;

let diameter, radius;

let center1, center2;

let RPM = 2;
let omega, theta;

let pos, start_pos;

let target_pos;
let target_dist;

let vel_mag, vel;

let angle_offset = 0;

let path, rot_path;

let t, dt;

let max_time, max_path_len;

let result_text;


let paused = false;
let min_dist;

let set_pos_button, set_target_button;
let start_button;

let set_omega_input, set_vel_input;
let set_omega_button, set_vel_button;
let set_angle_input, set_angle_button;


function setup() {
  createCanvas(canv_width, canv_width/2);

  diameter = 0.9 * width / 2;
  radius = diameter/2;

  omega = createVector(0, 0, 2 * Math.PI / 60 * RPM); //RPM = 2pi n/60
  theta = 0;

  pos = createVector(radius,0,0);
  start_pos = createVector(radius,0,0);
  target_pos = createVector(pos.x-radius,pos.y);

  vel_mag = 200; //ft/sec
  vel_mag = vel_mag*scalar; //5 px/sec = 1 ft/sec
  vel = createVector(-(pos.x-target_pos.x), -(pos.y-target_pos.y), 0);
  vel.setMag(vel_mag);

  t = 0;
  dt = 0.001;
  min_dist = Infinity;

  max_time = 50;
  max_path_len = 50;

  center1 = createVector(width / 4, height / 2, 0);
  center2 = createVector(3 * width / 4, height / 2, 0);

  path = [{"x": pos.x, "y": pos.y}, {"x": pos.x, "y": pos.y}];
  rot_path = [{"x": pos.x, "y": pos.y}, {"x": pos.x, "y": pos.y}];

  set_pos_button = createButton("set start pos");
  set_target_button = createButton("set target");
  start_button = createButton("reset");
  

  set_pos_button.position(width/2,0);
  set_target_button.position(set_pos_button.x, set_pos_button.y + set_pos_button.height);
  start_button.position(set_pos_button.x, set_target_button.y + set_target_button.height);

  set_pos_button.mouseReleased(()=> set_click_val("pos"));
  set_target_button.mouseReleased(()=> set_click_val("target"));
  start_button.mouseReleased(()=> {reset();});

  set_vel_input = createInput(vel_mag/scalar);
  set_omega_input = createInput(RPM);
  set_angle_input = createInput("0");

  set_angle_input.position(width/2, height - set_angle_input.height);
  set_omega_input.position(width/2, set_angle_input.y - set_omega_input.height);
  set_vel_input.position(width/2, set_omega_input.y - set_vel_input.height);

  set_omega_input.size(50);
  set_omega_button = createButton("set RPM")
  set_omega_button.position(set_omega_input.x+set_omega_input.width, set_omega_input.y);
  set_omega_button.mouseReleased(()=> set_no_click_val());

  set_vel_input.size(50);
  set_vel_button = createButton("set ft/s")
  set_vel_button.position(set_omega_input.x+set_vel_input.width, set_vel_input.y);
  set_vel_button.mouseReleased(()=> set_no_click_val());

  set_angle_input.size(50);
  set_angle_button = createButton("angle offset")
  set_angle_button.position(set_omega_input.x+set_angle_input.width, set_angle_input.y);
  set_angle_button.mouseReleased(()=> set_no_click_val());

  result_text = createElement('h2', '');
  result_text.position(0, height);


}

function reset() {
  theta = 0;
  t = 0;

  pos = createVector(start_pos.x,start_pos.y,0);

  vel = createVector(-(pos.x-target_pos.x), -(pos.y-target_pos.y), 0);
  vel.setMag(vel_mag);
  vel.rotate(angle_offset);

  path = [{"x": pos.x, "y": pos.y}, {"x": pos.x, "y": pos.y}];
  rot_path = [{"x": pos.x, "y": pos.y}, {"x": pos.x, "y": pos.y}];

  min_dist = Infinity;

  loop();
}

function set_click_val(to_set) {
  noLoop();
  mousePressed = function() {

    if (to_set === "pos") {
      pos.set(mouseX-center1.x, -(mouseY-center1.y), 0);
      start_pos.set(pos.x, pos.y, 0);
    } else if (to_set === "target") {
      target_pos.set(mouseX-center1.x, -(mouseY-center1.y), 0);
    }

    mousePressed = function() {};
    draw_circles();
  }
}



function set_no_click_val() {
  noLoop();
    omega.set(0, 0, 2 * Math.PI/60 * set_omega_input.value());
    vel_mag = set_vel_input.value()*scalar;
    angle_offset = -set_angle_input.value()*(-2)*Math.PI/360;
  reset();
}

function draw_circles() {
  noFill();
  background(0);
  stroke(255);
  strokeWeight(3);

  push();
  translate(center1.x, center1.y);
  circle(0, 0, diameter);
  circle(start_pos.x, start_pos.y, 10);
  stroke(0,255,255);
  circle(target_pos.x, target_pos.y, 10);
  stroke(100);
  strokeWeight(1);

  push();
  scale(1,-1);
  // image(token.img, token.x, token.y, token_size, token_size);

  for (i=-radius/(5*scalar); i<radius/(5*scalar)+1; i++) {
    if (i <radius/(5*scalar)) {
      text((-i+radius/(5*scalar)).toFixed(0), -radius-18, i*(5*scalar)+18);
      text((i+radius/(5*scalar)+1).toFixed(0), i*(5*scalar)+5, +radius+15);
    }
    line(-radius, i*(5*scalar), radius, i*(5*scalar));
    line(i*(5*scalar), -radius, i*(5*scalar), radius);
  }
  pop();

  pop();

  push();
  translate(center2.x, center2.y);
  rotate(theta);
  circle(0, 0, diameter);
  circle(start_pos.x, start_pos.y, 10);
  stroke(0,255,255);
  circle(target_pos.x, target_pos.y, 10);

  pop();
}

let looper = 0;
let looper2 = 0;

function keyPressed(){
  if (keyCode == ENTER) {
    set_no_click_val();
  }
  if (keyCode == ESCAPE) {
    noLoop();
  }
}


function draw() {
  scale(1, -1);
  translate(0, -height);
  // if (pos.mag() > radius*1.01) {
  //   noLoop();
  // }

  pos.add(p5.Vector.mult(vel, dt));
  let acc = createVector(0,0,0);
  acc.add(p5.Vector.mult(p5.Vector.cross(omega, vel), -2));
  acc.add(p5.Vector.mult(p5.Vector.cross(omega, p5.Vector.cross(omega, pos)), -1));
  acc.mult(dt);
  vel.add(acc);
  theta += omega.z * dt;
  t += dt;

  let cur_dist = pos.dist(target_pos);
  if (cur_dist < min_dist) {
    min_dist = cur_dist;
  } else {
    // noLoop();
    // console.log("missed by:", (min_dist/scalar).toFixed(1), "ft");
    // result_text.html(`dist: ${(min_dist/scalar).toFixed(1)} ft`);
  }

  looper2++;
  if (looper2 > 10) {
    draw_circles();

    update();
  }

  if (t > max_time) {
    noLoop();
    console.log("missed by:", (min_dist/scalar).toFixed(1), "ft");
    result_text.html(`dist: ${(min_dist/scalar).toFixed(1)} ft`);
  }
}

function update() {
  looper2=0;
  push();
  translate(center1.x, center1.y);
  stroke(255);
  stroke(255, 0, 0);
  circle(pos.x, pos.y, 10);


  looper++;
  if (looper >= 1) {
//    console.log(t.toFixed(2));

    path.unshift({
      "x": pos.x,
      "y": pos.y
    });
    rot_path.unshift({
      "x": cos(theta)*pos.x - sin(theta)*pos.y,
      "y": sin(theta)*pos.x + cos(theta)*pos.y,
    });
    looper = 0;
  }
  if (path.length > max_path_len) {
    path.pop();
    rot_path.pop();
  }

  stroke(0, 0, 255);
  for (let i = 1; i < path.length; i++) {
    line(path[i-1].x, path[i-1].y, path[i].x, path[i].y);
  }
  drawArrow(pos, p5.Vector.mult(vel, 0.2), 'green');

  pop();

  push();
  translate(center2.x, center2.y);
  stroke(0, 0, 255);
  for (let i = 1; i < path.length; i++) {
    line(rot_path[i-1].x, rot_path[i-1].y, rot_path[i].x, rot_path[i].y);
  }
  rotate(theta);
  drawArrow(pos, createVector(rot_path[0].x, rot_path[0].y).sub(createVector(rot_path[1].x, rot_path[1].y)).mult(0.02/dt).rotate(-theta), 'green');
  stroke(255,0,0);
  circle(pos.x, pos.y, 10);

  pop();

}


function drawArrow(base, vec, myColor) {
  push();
  stroke(myColor);
  strokeWeight(3);
  fill(myColor);
  translate(base.x, base.y);
  line(0, 0, vec.x/5, vec.y/5);
  rotate(vec.heading());
  let arrowSize = 7;
  translate(vec.mag()/5 - arrowSize, 0);
  triangle(0, arrowSize / 2, 0, -arrowSize / 2, arrowSize, 0);
  pop();
}
