class Particle {
  constructor(
    particleInfo,
    position = new Vector(100, 100),
    velocity = new Vector(2, 0),
    acceleration = new Vector(0, 0.1)
  ) {
    this.pos = position;
    this.vel = velocity;
    this.acc = acceleration;
    this.particleInfo = particleInfo;
    this.updatedInfo();
    this.update = this.update.bind(this);
    this.target = position;
    this.draw();
  }

  limitForce(maxForce) {
    this.maxForce = maxForce;
  }

  updatedInfo() {
    if (typeof this.particleInfo.custom === "undefined") {
      this.particleInfo.custom = false;
    }
    if (typeof this.particleInfo.color === "undefined") {
      this.particleInfo.color = "black";
    }
    if (typeof this.particleInfo.infinite === "undefined") {
      this.particleInfo.infinite = false;
    }
    if (typeof this.particleInfo.width === "undefined") {
      this.particleInfo.width = 10;
    }
    if (typeof this.particleInfo.height === "undefined") {
      this.particleInfo.height = 10;
    }
    if (typeof this.particleInfo.lifeSpan === "undefined") {
      this.particleInfo.lifeSpan = 0;
    }
  }
  applyForce(force) {
    this.acc = force;
  }

  terminate() {
    this.particle.remove();
  }

  getMousePos(event) {
    this.target = new Vector(event.clientX, event.clientY);
  }

  seekMouse() {
    $(window).mousemove(this.getMousePos.bind(this));
    this.lifeSpan = this.particleInfo.lifeSpan;
    this.limitForce(0.2);
    this.display = setInterval(this.update, 10);
  }

  seek(target) {
    clearInterval(this.display);
    this.target = target;
    this.lifeSpan = this.particleInfo.lifeSpan;
    this.limitForce(0.2);
    this.display = setInterval(this.update, 10);
    return 0;
  }

  //Following mouse
  update() {
    if (this.maxForce && this.acc.magnitude() > this.maxForce) {
      this.acc.normalize().mul(this.maxForce);
    }
    //console.log(this.pos);
    this.vel = Vector.add(this.vel, this.acc);
    this.pos = Vector.add(this.pos, this.vel);

    if (!this.particleInfo.infinite) {
      if (this.lifeSpan == 0) {
        clearInterval(this.display);
        return;
      } else {
        this.lifeSpan--;
      }
    }

    $(`.${this.particleInfo.name}`).css({
      position: "absolute",
      "margin-top": `${this.pos.y}px`,
      "margin-left": `${this.pos.x}px`,
      transform: `rotate(${(Math.atan2(this.vel.y, this.vel.x) * 180) /
        Math.PI}deg)`
    });

    var desired = Vector.sub(this.target, this.pos);

    var distance = desired.magnitude();
    desired.normalize();
    if (distance < 50) {
      var m = this.interpolation(distance, 0, 50, 0, 2);
      desired.mul(m);
    } else {
      desired.mul(2);
    }

    var steer = Vector.sub(desired, this.vel);
    this.applyForce(steer);
  }

  // Draw the initial position
  draw() {
    var particle = $(
      `<img src='http://kindersay.com/files/images/guinea-pig.png' class='${
        this.particleInfo.name
      }'></img>`
    );
    this.particle = particle;
    var animatedElement = {
      position: "absolute",
      "z-index": "5",
      "margin-top": `${this.pos.y}px`,
      "margin-left": `${this.pos.x}px`
    };

    if (!this.particleInfo.custom) {
      animatedElement.width = `${this.particleInfo.width}px`;
      animatedElement.height = `${this.particleInfo.height}px`;
      //animatedElement.background = `${this.particleInfo.color}`;
    }

    particle.css(animatedElement);
    $("body").append(particle);
  }

  interpolation(inputX, x1, x2, y1, y2) {
    var outputY = ((y2 - y1) / (x2 - x1)) * (inputX - x1);
    return outputY;
  }
}
