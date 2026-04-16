import { getCollection } from 'astro:content';

async function listPosts() {
    const posts = await getCollection('blog');
    console.log(posts.map(p => p.slug).sort());
}

listPosts();
