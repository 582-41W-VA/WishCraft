const posts = [];
let images = [];
let imageIndex = 0;

async function fetchImages(){
	const response = await fetch(`https://api.unsplash.com/photos/random?count=28&client_id=bibKns9LUjPwC0w9CUmuuwHjhmDBlYalqz5Yf806V6o`);
	const data = await response.json();
	images = data.map(photo => photo.urls.small);

	for (let i = 1; i <= 20; i++) {
		let randomNumber = Math.floor(Math.random() * 1001);

		let item = {
			id: i,
			title: `Post ${i}`,
			likes: Math.floor(Math.random() * 1001),
			image: images[imageIndex % images.length],
		};
		imageIndex++;
		posts.push(item);
	}
}
    fetchImages().catch(error => console.error(error));

console.log(posts);
export { posts, images, imageIndex, fetchImages };
