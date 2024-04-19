document.addEventListener("DOMContentLoaded", function () {
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

  // change tag color on selection

  // Get all checkboxes
  let checkboxes = document.querySelectorAll(".hidden_checkbox");

  // Add event listener to each checkbox
  checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener("change", function () {
      if (this.checked) {
        this.parentElement.classList.add("checked");
      } else {
        this.parentElement.classList.remove("checked");
      }
    });
  });

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
  const body = document.querySelector("body");

  logo.addEventListener("click", function (event) {
    event.stopPropagation();
    nav.classList.toggle("active");
  });

  body.addEventListener("click", function () {
    nav.classList.remove("active");
  });

  //hide label and add placeholder on focus

  const form = document.querySelector(".new_user");
  const inputs = form.querySelectorAll("input, textarea, select");

  inputs.forEach((input) => {

    const label = form.querySelector(`label[for="${input.id}"]`);
    if (label) {
      label.style.position = "absolute";
      label.style.width = "1px";
      label.style.height = "1px";
      label.style.padding = "0";
      label.style.margin = "-1px";
      label.style.overflow = "hidden";
      label.style.clip = "rect(0,0,0,0)";
      label.style.whiteSpace = "nowrap";
      label.style.border = "0";

      input.setAttribute("placeholder", label.innerText);
    }
  });
});
