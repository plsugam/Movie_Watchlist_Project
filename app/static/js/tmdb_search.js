// TMDB Search Integration
// Requires TMDB_API_KEY to be set in the page via a data attribute

const TMDB_KEY = document.getElementById('add-form')?.dataset.tmdbKey;
const titleInput = document.getElementById('title');
const dropdown = document.getElementById('tmdb-dropdown');
const posterPreview = document.getElementById('poster-preview');
const posterUrlInput = document.getElementById('poster_url');
const yearInput = document.getElementById('year');
const genreInput = document.getElementById('genre');

let searchTimeout = null;

const GENRE_MAP = {
    28: 'Action', 12: 'Adventure', 16: 'Animation', 35: 'Comedy',
    80: 'Crime', 99: 'Documentary', 18: 'Drama', 10751: 'Family',
    14: 'Fantasy', 36: 'History', 27: 'Horror', 10402: 'Music',
    9648: 'Mystery', 10749: 'Romance', 878: 'Sci-Fi', 53: 'Thriller',
    10752: 'War', 37: 'Western', 10759: 'Action & Adventure',
    10762: 'Kids', 10763: 'News', 10764: 'Reality', 10765: 'Sci-Fi & Fantasy',
    10766: 'Soap', 10767: 'Talk', 10768: 'War & Politics'
};

if (titleInput && TMDB_KEY) {
    titleInput.addEventListener('input', function () {
        const query = this.value.trim();
        clearTimeout(searchTimeout);

        if (query.length < 2) {
            hideDropdown();
            return;
        }

        searchTimeout = setTimeout(() => searchTMDB(query), 350);
    });

    titleInput.addEventListener('blur', function () {
        setTimeout(hideDropdown, 200);
    });
}

async function searchTMDB(query) {
    try {
        const url = `https://api.themoviedb.org/3/search/multi?api_key=${TMDB_KEY}&query=${encodeURIComponent(query)}&page=1`;
        const res = await fetch(url);
        const data = await res.json();

        const results = (data.results || [])
            .filter(r => r.media_type === 'movie' || r.media_type === 'tv')
            .slice(0, 6);

        renderDropdown(results);
    } catch (err) {
        hideDropdown();
    }
}

function renderDropdown(results) {
    if (!results.length) { hideDropdown(); return; }

    dropdown.innerHTML = results.map(r => {
        const title = r.title || r.name || '';
        const year = (r.release_date || r.first_air_date || '').slice(0, 4);
        const type = r.media_type === 'movie' ? 'Movie' : 'Series';
        const poster = r.poster_path
            ? `https://image.tmdb.org/t/p/w92${r.poster_path}`
            : '';

        return `
        <div class="tmdb-item" data-title="${escAttr(title)}"
             data-year="${year}"
             data-type="${r.media_type}"
             data-genre-ids="${(r.genre_ids || []).join(',')}"
             data-poster="${r.poster_path ? 'https://image.tmdb.org/t/p/w500' + r.poster_path : ''}">
            ${poster
                ? `<img src="${poster}" alt="${escAttr(title)}" class="tmdb-thumb">`
                : `<div class="tmdb-thumb tmdb-no-poster"></div>`
            }
            <div class="tmdb-info">
                <span class="tmdb-title">${escHtml(title)}</span>
                <span class="tmdb-meta">${type}${year ? ' · ' + year : ''}</span>
            </div>
        </div>`;
    }).join('');

    dropdown.classList.add('visible');

    dropdown.querySelectorAll('.tmdb-item').forEach(item => {
        item.addEventListener('mousedown', function () {
            selectResult(this);
        });
    });
}

function selectResult(item) {
    const title = item.dataset.title;
    const year = item.dataset.year;
    const mediaType = item.dataset.type;
    const genreIds = item.dataset.genreIds.split(',').map(Number).filter(Boolean);
    const poster = item.dataset.poster;

    // Fill form fields
    titleInput.value = title;
    if (yearInput) yearInput.value = year;

    // Map genre
    if (genreInput && genreIds.length) {
        const genreName = GENRE_MAP[genreIds[0]] || '';
        genreInput.value = genreName;
    }

    // Set type dropdown
    const typeSelect = document.getElementById('type');
    if (typeSelect) {
        typeSelect.value = mediaType === 'movie' ? 'movie' : 'series';
    }

    // Set poster
    if (posterUrlInput) posterUrlInput.value = poster;
    if (posterPreview && poster) {
        posterPreview.src = poster;
        posterPreview.style.display = 'block';
    }

    hideDropdown();
}

function hideDropdown() {
    if (dropdown) dropdown.classList.remove('visible');
}

function escAttr(str) {
    return str.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function escHtml(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}
