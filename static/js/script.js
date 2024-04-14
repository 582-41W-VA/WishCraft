document.addEventListener("DOMContentLoaded", function() {
  // Home Page
  // the sort form to submit the form when the value changes
  const sortForm = document.getElementById("sortForm");
  if (sortForm) {
    sortForm.addEventListener("change", function () {
      this.submit();
    });
  }

  // the filter form to submit the form when the value changes
  const filterForm = document.getElementById("filterForm");
  const tagCheckboxes = document.querySelectorAll("input[name='tags']");
  if (filterForm) {
    tagCheckboxes.forEach(function (checkbox) {
      checkbox.addEventListener("change", function () {
        filterForm.submit();
      });
    });
  }

  // the clear tags button to uncheck all checkboxes
  const clearTagsBtn = document.getElementById("clearTagsBtn");
  if (clearTagsBtn && filterForm) {
    clearTagsBtn.addEventListener("click", function () {
      let checkboxes = document.querySelectorAll(
        "input[type='checkbox'][name='tags']"
      );
      checkboxes.forEach(function (checkbox) {
        checkbox.checked = false;
      });
      filterForm.submit();
    });
  }

  // Admin Panel
  // the delete user form to confirm the deletion
  const deleteUser = document.getElementById("deleteUser");
  if (deleteUser) {
    deleteUser.addEventListener("submit", function (event) {
      if (
        !confirm(
          "Are you sure you want to delete this user? This action cannot be undone."
        )
      ) {
        event.preventDefault();
      }
    });
  }

  // the delete card form to confirm the deletion
  let deleteForm = document.querySelectorAll(".deleteCard");
  deleteForm.forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (
        !confirm(
          "Are you sure you want to delete this card? This action cannot be undone."
        )
      ) {
        event.preventDefault();
      }
    });
  });

  // mobile menu
  const logo = document.getElementById("logo");
  const nav = document.querySelector("nav");

  logo.addEventListener("click", function () {
    nav.classList.toggle("active");
  });

  console.log("script.js loaded");
});




