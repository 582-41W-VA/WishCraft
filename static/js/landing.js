const galleryContainer = document.querySelector(".gallery_container");

// Initialize Masonry with options (optional)
const masonry = new Masonry(galleryContainer, {
  itemSelector: ".gallery-image",
  columnWidth: 200,
  gutter: 10,
  percentPosition: true,
});

const images = Array.from(
  { length: 100 },
  () => "https://source.unsplash.com/random/200x200"
);

// Duplicate the images array to create a seamless loop
const allImages = [...images, ...images];

function appendImages() {
  const visibleImages = 10;
  for (let i = 0; i < visibleImages; i++) {
    const imageUrl = allImages[i];
    const img = document.createElement("img");
    img.src = imageUrl;
    img.onload = () => {
      img.classList.add("loaded");
      img.classList.add("gallery-image");
      console.log(img);
    };
    galleryContainer.appendChild(img);
  }
  masonry.layout();
}

document.addEventListener("DOMContentLoaded", function() {
  appendImages();
});

galleryContainer.addEventListener("scroll", () => {
  const scrollTop = galleryContainer.scrollTop;
  const scrollableHeight = galleryContainer.scrollHeight;
  const threshold = scrollableHeight - galleryContainer.clientHeight * 2; // Adjust the threshold as needed
  if (scrollTop >= threshold) {
    appendImages();
  }
});
