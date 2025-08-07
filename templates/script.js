document.addEventListener("DOMContentLoaded", function () {
  const carousel = document.querySelector('.carousel');
  const items = document.querySelectorAll('.carousel-item');
  const prevBtn = document.querySelector('.carousel-control.prev');
  const nextBtn = document.querySelector('.carousel-control.next');
  let currentIndex = 0;
  let intervalId = null;

  function showSlide(index) {
    items[currentIndex].classList.remove('active');
    currentIndex = (index + items.length) % items.length;
    items[currentIndex].classList.add('active');
  }

  function startAutoPlay() {
    if (intervalId) return; // prevent duplicate intervals
    intervalId = setInterval(() => {
      showSlide(currentIndex + 1);
    }, 3000);
  }

  function stopAutoPlay() {
    clearInterval(intervalId);
    intervalId = null;
  }

  prevBtn.addEventListener('click', () => {
    stopAutoPlay();
    showSlide(currentIndex - 1);
    startAutoPlay();
  });

  nextBtn.addEventListener('click', () => {
    stopAutoPlay();
    showSlide(currentIndex + 1);
    startAutoPlay();
  });

  carousel.addEventListener('mouseenter', stopAutoPlay);    
  carousel.addEventListener('mouseleave', startAutoPlay);

  showSlide(currentIndex);
  startAutoPlay();
});
