
hamburger = document.getElementById("hamburger");
nav_pop = document.getElementsByClassName("nav-pop")[0];
line_one = document.getElementsByClassName("line1")[0];
line_two = document.getElementsByClassName("line2")[0];
line_three = document.getElementsByClassName("line3")[0];

hamburger.addEventListener("click", () => {
    nav_pop.classList.toggle('active');
    line_one.classList.toggle('bend');
    line_two.classList.toggle('bend');
    line_three.classList.toggle('bend');
});

