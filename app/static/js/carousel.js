const slides = document.querySelectorAll('.carousel-slide');
const indicators = document.querySelectorAll('.indicator');
const submitBtn = document.getElementById('submitBtn');
const backdrops = [
    [
        "https://image.tmdb.org/t/p/original/tsRy63Mu5cu8etL1X7ZLyf7UP1M.jpg",
        "https://image.tmdb.org/t/p/original/sp1RSDvoVsbvDouQx1A75ebU35e.jpg",
        "https://image.tmdb.org/t/p/original/84XPpjGvxNyExjSuLQe0SzioErt.jpg",
    ],
    [
        "https://image.tmdb.org/t/p/original/5XNQBqnBwPA9yT0jZ0p3s8bbLh0.jpg",
        "https://image.tmdb.org/t/p/original/8sNiAPPYU14PUepFNeSNGUTiHW.jpg",
        "https://image.tmdb.org/t/p/original/vgnoBSVzWAV9sNQUORaDGvDp7wx.jpg",
    ],
    [
        "https://image.tmdb.org/t/p/original/dzq83RHwQcnP6WGJ6YkenIqeaa5.jpg",
        "https://image.tmdb.org/t/p/original/wiE9doxiLwq3WCGamDIOb2PqBqc.jpg",
        "https://image.tmdb.org/t/p/original/l8v3gJDlASN0lNn51gR8zQJsu5O.jpg",
    ],
    [
        "https://image.tmdb.org/t/p/original/h61Kc0NC7d90jNwXfBx5js7DnSQ.jpg",
        "https://image.tmdb.org/t/p/original/qVgZu5BTx6pu4owCvVOm4zjTfOi.jpg",
        "https://image.tmdb.org/t/p/original/h3HsfV8Kn9Sz2QWUYYdP5ya23hx.jpg",
    ],
    [
        "https://image.tmdb.org/t/p/original/3jDXL4Xvj3AzDOF6UH1xeyHW8MH.jpg",
        "https://image.tmdb.org/t/p/original/75HgaphatW0PDI3XIHQWZUpbhn6.jpg",
        "https://image.tmdb.org/t/p/original/2VpSajCTI26zddsp5cSjqfCBKEa.jpg",
    ],
    [
        "https://image.tmdb.org/t/p/original/cUIqZd6jJCbO94Txt1CkTs7MSeP.jpg",
        "https://image.tmdb.org/t/p/original/neeNHeXjMF5fXoCJRsOmkNGC7q.jpg",
        "https://image.tmdb.org/t/p/original/ycnO0cjsAROSGJKuMODgRtWsHQw.jpg",
    ],
];

const backdropIndex = [0, 0, 0, 0, 0, 0];
let current = 0;
let interval;
let isTransitioning = false;
document.documentElement.style.setProperty('--accent-transition', '0.9s');

// Preload next image to avoid flash
function preloadImage(url) {
    const img = new Image();
    img.src = url;
}

// Preload all backdrops on init
backdrops.forEach(group => group.forEach(url => preloadImage(url)));

function applyAccentColor(color) {
    document.documentElement.style.setProperty('--accent', color);
    document.documentElement.style.setProperty('--accent-rgb', hexToRgb(color));
    if (submitBtn) {
        submitBtn.style.transition = 'background 0.9s ease';
        submitBtn.style.background = color;
    }
}

function hexToRgb(hex) {
    const normalized = hex.replace('#', '');
    const expanded = normalized.length === 3
        ? normalized.split('').map(char => char + char).join('')
        : normalized;
    const value = parseInt(expanded, 16);
    return `${(value >> 16) & 255}, ${(value >> 8) & 255}, ${value & 255}`;
}

function goToSlide(index) {
    if (isTransitioning || index === current) return;
    isTransitioning = true;

    const prev = current;
    current = index;

    // Advance backdrop for incoming slide
    backdropIndex[current] = (backdropIndex[current] + 1) % backdrops[current].length;
    const newUrl = backdrops[current][backdropIndex[current]];

    // Set incoming poster before it becomes visible
    const incomingPoster = slides[current].querySelector('.slide-poster');
    if (incomingPoster) {
        incomingPoster.style.backgroundImage = `url('${newUrl}')`;
    }

    // Preload the one after next
    const nextIndex = (current + 1) % slides.length;
    const nextBackdropIdx = (backdropIndex[nextIndex] + 1) % backdrops[nextIndex].length;
    preloadImage(backdrops[nextIndex][nextBackdropIdx]);

    // Fade out previous
    slides[prev].classList.remove('active');
    indicators[prev].classList.remove('active');

    // Fade in current after a brief pause
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            slides[current].classList.add('active');
            indicators[current].classList.add('active');
            applyAccentColor(slides[current].dataset.color);

            setTimeout(() => { isTransitioning = false; }, 900);
        });
    });
}

function nextSlide() {
    goToSlide((current + 1) % slides.length);
}

function startAutoplay() {
    interval = setInterval(nextSlide, 4500);
}

function resetAutoplay() {
    clearInterval(interval);
    startAutoplay();
}

indicators.forEach((dot, i) => {
    dot.addEventListener('click', () => {
        goToSlide(i);
        resetAutoplay();
    });
});

// Init
applyAccentColor(slides[0].dataset.color);
startAutoplay();
