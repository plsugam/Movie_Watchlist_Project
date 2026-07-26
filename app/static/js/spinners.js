function spinUp(id, max) {
    const el = document.getElementById(id);
    const val = parseInt(el.value) || 0;
    if (val < max) el.value = val + 1;
}

function spinDown(id, min) {
    const el = document.getElementById(id);
    const val = parseInt(el.value);
    if (!isNaN(val) && val > min) el.value = val - 1;
}
