document.addEventListener("DOMContentLoaded", function() {
    const sortForm= document.getElementById("sortForm");
    sortForm.addEventListener("change", function() {
        this.submit();
    });

    const filterForm = document.getElementById("filterForm");
    const tagCheckboxes = document.querySelectorAll("input[name='tags']");
    tagCheckboxes.forEach(function(checkbox) {
        checkbox.addEventListener("change", function() {
            filterForm.submit();
        });
    });
});
