import os
import re

blog_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"

short_posts = []

for file in os.listdir(blog_dir):
    if not file.endswith('.md'): continue
    
    path = os.path.join(blog_dir, file)
    with open(path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    fm_match = re.search(r'^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)', content, re.DOTALL)
    if fm_match:
        body = fm_match.group(2).strip()
        body_lines = [l for l in body.splitlines() if l.strip()]
        if len(body_lines) < 5:
            slug = file.replace('.md', '')
            short_posts.append(f"https://anfitriaopicarras.com/{slug}/")

for url in short_posts:
    print(url)
