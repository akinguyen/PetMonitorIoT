$(function() {
  var red = new Particle(
    {
      name: "fish",
      custom: true,
      infinite: true,
      width: 50
    },
    new Vector(600, 100),
    new Vector(-0.2, 0.1),
    new Vector(-0.03, 0.01)
  );
  red.seekMouse();

  $(window).resize(function() {
    $(".seaweed").css({
      "margin-top": `${window.innerHeight - 400}px`,
      "margin-left": `${window.innerWidth - 400}px`
    });
    $(".cave").css({ height: `${window.innerHeight + 100}px` });
    $(".water").css({ "margin-left": `${window.innerWidth - 200}px` });
  });

  $(".seaweed").css({
    "margin-top": `${window.innerHeight - 400}px`,
    "margin-left": `${window.innerWidth - 400}px`
  });
  $(".cave").css({ height: `${window.innerHeight + 100}px` });
  $(".water").css({ "margin-left": `${window.innerWidth - 200}px` });
});
