import os
import re
import requests
from urllib.parse import urlparse

blog_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"
public_img_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\public\images\blog"

if not os.path.exists(public_img_dir):
    os.makedirs(public_img_dir)

def download_image(url):
    try:
        # Generate a filename from URL parameters if it's Unsplash
        parsed = urlparse(url)
        if 'unsplash.com' in url:
            # photo-1551288049-bebda4e38f71
            photo_id = parsed.path.strip('/')
            ext = 'jpg' # Default for unsplash
            filename = f"unsplash-{photo_id}.{ext}"
        else:
            filename = os.path.basename(parsed.path)
            if not filename or '.' not in filename:
                filename = "downloaded_image.jpg"
        
        filepath = os.path.join(public_img_dir, filename)
        
        # Avoid redownloading
        if os.path.exists(filepath):
            return f"/images/blog/{filename}"

        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return f"/images/blog/{filename}"
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
    return None

files = os.listdir(blog_dir)
for file in files:
    if not file.endswith('.md'):
        continue
    
    path = os.path.join(blog_dir, file)
    with open(path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    # Match heroImage: "http..."
    match = re.search(r'heroImage:\s*"(http.*?)"', content)
    if match:
        url = match.group(1)
        print(f"Baixando imagem para {file}...")
        local_path = download_image(url)
        if local_path:
            new_content = content.replace(url, local_path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  OK: {local_path}")
        else:
            print(f"  FALHA: {url}")
