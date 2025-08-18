document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById('game-slider');
    const cont = document.getElementById('game-slider1');
    const btnLeft = document.getElementById('scroll-left');
    const btnRight = document.getElementById('scroll-right');
    const btnLeft1 = document.getElementById('scroll-left1');
    const btnRight1 = document.getElementById('scroll-right1');
    if (btnLeft && btnRight && container) {
        btnLeft.addEventListener('click', () => {
            container.scrollBy({left: -260, behavior: 'smooth'});
        });

        btnRight.addEventListener('click', () => {
            container.scrollBy({left: 260, behavior: 'smooth'});
        });
    }
    if (btnLeft1 && btnRight1 && cont) {
        btnLeft1.addEventListener('click', () => {
            cont.scrollBy({left: -260, behavior: 'smooth'});
        });

        btnRight1.addEventListener('click', () => {
            cont.scrollBy({left: 260, behavior: 'smooth'});
        });
    }
});