function spinUp(fieldId, max) {
    const input = document.getElementById(fieldId);
    if (input) {
        const currentValue = parseInt(input.value) || 0;
        if (currentValue < max) {
            input.value = currentValue + 1;
        }
    }
}

function spinDown(fieldId, min) {
    const input = document.getElementById(fieldId);
    if (input) {
        const currentValue = parseInt(input.value) || 0;
        if (currentValue > min) {
            input.value = currentValue - 1;
        }
    }
}
