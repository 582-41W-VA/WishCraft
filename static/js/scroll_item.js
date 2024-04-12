const posts = [];
let images = [];
let imageIndex = 0;

async function fetchImages(){
	const response = await fetch(`https://api.unsplash.com/photos/random?count=30&client_id=bibKns9LUjPwC0w9CUmuuwHjhmDBlYalqz5Yf806V6o`);
	const data = await response.json();
	return data.map(photo => photo.urls.small);
}

async function createPosts(){
	images = await fetchImages();
	imageIndex = 0;
	
	for (let i = 1; i <= 28; i++) {	
		let item = {
			 id: i,
			 image: images[imageIndex],
		};
		imageIndex++;
		posts.push(item);
	}

	const columns = document.getElementsByClassName('column');
	posts.forEach((post, index) => {
		const img = document.createElement('img');
		img.src = post.image;

		const postDiv = document.createElement('div');
    	postDiv.className = 'post';
    	postDiv.appendChild(img);

		const column = columns[index % columns.length];
		column.appendChild(postDiv);
	});
}

createPosts().catch(error => console.error(error));

console.log(posts);
export { posts, images, imageIndex };