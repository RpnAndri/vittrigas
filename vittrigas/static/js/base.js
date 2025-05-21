hamburger = document.getElementsByClassName("hamburger")[0];
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

document.addEventListener("DOMContentLoaded", function () {
    const slides = document.querySelectorAll(".slide");
    const dots = document.querySelectorAll(".dot");
    const prevBtn = document.querySelector(".slider-btn.prev");
    const nextBtn = document.querySelector(".slider-btn.next");
    let currentIndex = 0;
    let interval;

    function showSlide(index) {
      slides.forEach((slide, i) => {
        slide.classList.toggle("active", i === index);
        dots[i].classList.toggle("active", i === index);
      });
    }

    function nextSlide() {
      currentIndex = (currentIndex + 1) % slides.length;
      showSlide(currentIndex);
    }

    function prevSlide() {
      currentIndex = (currentIndex - 1 + slides.length) % slides.length;
      showSlide(currentIndex);
    }

    function startAutoplay() {
      interval = setInterval(nextSlide, 3000); // every 3 seconds
    }

    function stopAutoplay() {
      clearInterval(interval);
    }

    nextBtn.addEventListener("click", () => {
      stopAutoplay();
      nextSlide();
      startAutoplay();
    });

    prevBtn.addEventListener("click", () => {
      stopAutoplay();
      prevSlide();
      startAutoplay();
    });

    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        stopAutoplay();
        currentIndex = i;
        showSlide(currentIndex);
        startAutoplay();
      });
    });

    // Start carousel
    showSlide(currentIndex);
    startAutoplay();
  });
