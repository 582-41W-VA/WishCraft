// when on the landing page, hide the navbar
document.getElementById("home-link").style.display = "none";
document.getElementById("create-card-link").style.display = "none";
document.getElementById("wishlist-link").style.display = "none";
document.getElementById("search-form").style.display = "none";

document.addEventListener("DOMContentLoaded", function () {
  const header = document.querySelector("header");

  console.log("Landing.js is connected");


  window.addEventListener("scroll", function () {
    console.log(window.scrollY);
    if (window.scrollY >= 200) {
      if (!header.classList.contains("show")) {
        header.classList.add("show");
      }
    } else {
      if (header.classList.contains("show")) {
        header.classList.remove("show");
      }
    }
  });
});

