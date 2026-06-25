const slides = document.querySelectorAll('.carousel-slide');
const indicators = document.querySelectorAll('.indicator');
const submitBtn = document.getElementById('submitBtn');
let current = 0;
let interval;

function goToSlide(index) {
    // Remove active from current
    slides[current].classList.remove('active');
    indicators[current].classList.remove('active');

    current = index;

    // Activate new slide
    slides[current].classList.add('active');
    indicators[current].classList.add('active');

    // Update accent color
    const color = slides[current].dataset.color;
    applyAccentColor(color);
}

function applyAccentColor(color) {
    document.documentElement.style.setProperty('--accent', color);
    if (submitBtn) {
        submitBtn.style.background = color;
    }
}

function nextSlide() {
    goToSlide((current + 1) % slides.length);
}

function startAutoplay() {
    interval = setInterval(nextSlide, 4000);
}

function resetAutoplay() {
    clearInterval(interval);
    startAutoplay();
}

// Indicator clicks
indicators.forEach((dot, i) => {
    dot.addEventListener('click', () => {
        goToSlide(i);
        resetAutoplay();
    });
});

// Init — apply first slide color immediately
applyAccentColor(slides[0].dataset.color);
startAutoplay();
