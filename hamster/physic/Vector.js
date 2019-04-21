class Vector {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  static getDistance(vector1, vector2) {
    return this.sub(vector1, vector2).magnitude();
  }
  static add(vector1, vector2) {
    var x = vector1.x + vector2.x;
    var y = vector1.y + vector2.y;
    return new Vector(x, y);
  }

  static sub(vector1, vector2) {
    return this.add(vector1, vector2.reverse());
  }

  static dot(vector1, vector2) {
    return vector1.x * vector2.x + vector1.y * vector2.y;
  }

  static angleBetween(vector1, vector2) {
    var dot = this.dot(vector1, vector2);
    return Math.acos(dot / (vector1.magnitude() * vector2.magnitude()));
  }
  normalize() {
    return this.divide(this.magnitude());
  }

  magnitude() {
    return Math.sqrt(this.x * this.x + this.y * this.y);
  }

  getCopy() {
    return new Vector(this.x, this.y);
  }

  mul(scalar) {
    this.x *= scalar;
    this.y *= scalar;
    return this;
  }

  divide(scalar) {
    return this.mul(1.0 / scalar);
  }
  reverse() {
    var vectorCopy = new Vector(-1 * this.x, -1 * this.y);
    return vectorCopy;
  }
}
