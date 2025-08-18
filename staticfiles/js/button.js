document.addEventListener("DOMContentLoaded", function () {
    const container = document.getElementById('game-slider');
    const btnLeft = document.getElementById('scroll-left');
    const btnRight = document.getElementById('scroll-right');
    if (btnLeft && btnRight && container) {
        btnLeft.addEventListener('click', () => {
            container.scrollBy({left: -260, behavior: 'smooth'});
        });

        btnRight.addEventListener('click', () => {
            container.scrollBy({left: 260, behavior: 'smooth'});
        });
    }
});