const galleryContainer = document.querySelector(".gallery_container");
galleryContainer.classList.add("masonry");
const threshold = 0.1;

const accessKey = "RhSD_j2EBqohnVKePimkTdJWF1MoqETW1tpbZKAWvWI";
let page = 1;

const fetchImages = async () => {
  const response = await fetch(
    `https://api.unsplash.com/photos?client_id=${accessKey}&per_page=30&page=${page}`
  );
  const images = await response.json();

  images.forEach((image) => {
    const img = document.createElement("img");
    img.src = image.urls.regular;
    img.onload = () => img.classList.add("loaded");
    galleryContainer.appendChild(img);
  });

  page++;
};

fetchImages();

window.addEventListener("scroll", () => {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

  if (scrollTop + clientHeight >= scrollHeight - 100) {
    fetchImages();
  }
});

function adjustColumnCount() {
  let masonryElements = document.querySelectorAll(".masonry");
  masonryElements.forEach(function (masonry) {
    masonry.classList.remove("four_columns");
    if (window.innerWidth >= 600 && window.innerWidth < 900) {
      masonry.classList.remove("six_columns");
      masonry.classList.add("four_columns");
    } else if (window.innerWidth >= 900) {
      masonry.classList.remove("four_columns");
      masonry.classList.add("six_columns");
    }
  });
}

adjustColumnCount();

window.addEventListener("resize", adjustColumnCount);


let scrollPosition = 0;
let scrollSpeed = 2; // Adjust scroll speed here

function autoScrollBackground() {
  scrollPosition += scrollSpeed;

  const backgroundContainer = document.querySelector(".gallery_container");
  backgroundContainer.style.transform = `translateY(-${scrollPosition}px)`;

  requestAnimationFrame(autoScrollBackground);
}

autoScrollBackground();
