// Auto-submit filter form when any dropdown changes
document.querySelectorAll('.filter-select').forEach(function(select) {
    select.addEventListener('change', function() {
        this.closest('form').submit();
    });
});
