
import { getCollection } from 'astro:content';

const posts = await getCollection('blog');
posts.forEach(post => {
    console.log(`Slug: ${post.slug} -> URL local: /blog/${post.slug}/`);
});
