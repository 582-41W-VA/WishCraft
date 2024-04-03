const posts = [];

const images = [
  "https://source.unsplash.com/random?1",
  "https://source.unsplash.com/random?2",
  "https://source.unsplash.com/random?3",
  "https://source.unsplash.com/random?4",
  "https://source.unsplash.com/random?5",
  "https://source.unsplash.com/random?6",
  "https://source.unsplash.com/random?7",
  "https://source.unsplash.com/random?8",
  "https://source.unsplash.com/random?9",
  "https://source.unsplash.com/random?10",
  "https://source.unsplash.com/random?11",
  "https://source.unsplash.com/random?12",
];

let imageIndex = 0;

for (let i = 1; i <= 80; i++) {
  let item = {
    id: i,
    title: `Post ${i}`,
    icon: `
        <div class='like-icon'>
        <span class='like-count'>0</span>
            <i class='fas fa-heart'></i>
        </div>
    `,
    image: images[imageIndex],
  };
  posts.push(item);
  imageIndex++;
  if (imageIndex > images.length - 1) {
    imageIndex = 0;
  }
}

// console.log(posts);
export { posts, images, imageIndex };
