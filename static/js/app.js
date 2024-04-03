import { posts, images, imageIndex } from './scroll_item.js';
const scrollContainer = document.querySelector(".container");

function generateMasonryGrid(columns, posts) {
  scrollContainer.innerHTML = "";

  let columnsWrappers = {};

  for (let i = 0; i < columns; i++) {
    columnsWrappers[`column${i}`] = [];
  }

  for (let i = 0; i < posts.length; i++) {
    const column = i % columns;
    columnsWrappers[`column${column}`].push(posts[i]);
  }

  for (let i = 0; i < columns; i++) {
    let columnPosts = columnsWrappers[`column${i}`];
    let div = document.createElement("div");
    div.classList.add("column");

    columnPosts.forEach((post) => {
      let postDiv = document.createElement("div");
      postDiv.classList.add("post");

      let image = document.createElement("img");
      image.src = post.image;

      let hoverOverlay = document.createElement("div");
      hoverOverlay.classList.add("overlay");

      let title = document.createElement("h3");
      title.innerText = post.title;

    let iconDiv = document.createElement("div");
    iconDiv.classList.add("like-icon");

    let heartIcon = document.createElement("i");
    heartIcon.classList.add("fas", "fa-heart");
    iconDiv.appendChild(heartIcon);

    let likeCount = document.createElement("span");
    likeCount.classList.add("like-count");
    let likeCountText = document.createTextNode(post.likes || "0"); // replace with actual like count
    likeCount.appendChild(likeCountText);
    iconDiv.appendChild(likeCount);

    hoverOverlay.appendChild(title);
    hoverOverlay.appendChild(iconDiv);
    postDiv.append(image, hoverOverlay);
    div.appendChild(postDiv);
    });

    scrollContainer.appendChild(div);
  }
}

let previousScreenSize = window.innerWidth;

window.addEventListener("resize", () => {
  imageIndex = 0;
  if (window.innerWidth < 600 && previousScreenSize >= 600) {
    generateMasonryGrid(1, posts);
  } else if (
    window.innerWidth >= 600 &&
    window.innerWidth < 1000 &&
    (previousScreenSize < 600 || previousScreenSize >= 1000)
  ) {
    generateMasonryGrid(2, posts);
  } else if (window.innerWidth >= 1000 && previousScreenSize < 1000) {
    generateMasonryGrid(4, posts);
  }
  previousScreenSize = window.innerWidth;
});

if (previousScreenSize < 600) {
  generateMasonryGrid(1, posts);
} else if (previousScreenSize >= 600 && previousScreenSize < 1000) {
  generateMasonryGrid(2, posts);
} else {
  generateMasonryGrid(4, posts);
}
