import os
import re
from PIL import Image
import pillow_avif

blog_img_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\public\images\blog"
blog_content_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"

processed_count = 0
converted_map = {}

# 1. Convert Images
print("Convertendo imagens para AVIF...")
for filename in os.listdir(blog_img_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        input_path = os.path.join(blog_img_dir, filename)
        basename = os.path.splitext(filename)[0]
        output_filename = f"{basename}.avif"
        output_path = os.path.join(blog_img_dir, output_filename)
        
        try:
            with Image.open(input_path) as img:
                img.save(output_path, "AVIF", quality=75)
            processed_count += 1
            converted_map[filename] = output_filename
            # Optional: remove original
            # os.remove(input_path) 
        except Exception as e:
            print(f"Erro ao converter {filename}: {e}")

print(f"Total de {processed_count} imagens convertidas.")

# 2. Update Blog Posts (.md)
print("Atualizando caminhos nos arquivos Markdown...")
for filename in os.listdir(blog_content_dir):
    if filename.endswith('.md'):
        path = os.path.join(blog_content_dir, filename)
        with open(path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        new_content = content
        # Replace image extensions in heroImage: "/images/blog/name.ext"
        new_content = re.sub(r'(/images/blog/[^"]+)\.(png|jpg|jpeg|webp)', r'\1.avif', new_content)
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Atualizado: {filename}")

# 3. Update Components/Pages (Optional but good)
print("Verificando outros arquivos do projeto...")
search_dirs = [
    r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\components",
    r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\pages"
]

for sdir in search_dirs:
    if not os.path.exists(sdir): continue
    for filename in os.listdir(sdir):
        if filename.endswith(('.astro', '.ts', '.js')):
            path = os.path.join(sdir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = re.sub(r'(/images/blog/[^"\' }]+)\.(png|jpg|jpeg|webp)', r'\1.avif', content)
            
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  Atualizado: {filename}")

print("Finalizado!")
