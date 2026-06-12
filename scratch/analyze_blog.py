import os
import glob

blog_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"
img_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\public"

md_files = glob.glob(os.path.join(blog_dir, "*.md"))
total_files = len(md_files)
missing_images = []
short_content = []
missing_faq = []

for file in md_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Check image
        hero_img = None
        for line in content.split('\n'):
            if line.startswith('heroImage:'):
                hero_img = line.split(':', 1)[1].strip().strip('"').strip("'")
                break
        
        if hero_img:
            # Check if image exists
            # image path starts with /images/blog/ so we append to public
            img_path = os.path.join(img_dir, hero_img.lstrip('/'))
            if not os.path.exists(img_path):
                missing_images.append((os.path.basename(file), hero_img))
        else:
            missing_images.append((os.path.basename(file), "No heroImage defined"))
            
        # check content length (number of words)
        words = len(content.split())
        if words < 800:
            short_content.append(os.path.basename(file))
            
        # check FAQ
        if 'Perguntas Frequentes' not in content and 'FAQ' not in content:
            missing_faq.append(os.path.basename(file))
            
print(f"Total de Artigos: {total_files}")
print(f"Artigos com imagens faltando ou quebradas ({len(missing_images)}):")
for f, img in missing_images:
    print(f"  - {f}: {img}")
    
print(f"\nArtigos precisando expansão de SEO (< 800 palavras) ({len(short_content)}):")
for f in short_content[:15]:
    print(f"  - {f}")
if len(short_content) > 15: print(f"  ... e mais {len(short_content)-15}")

print(f"\nArtigos sem a seção de FAQ (SEO) ({len(missing_faq)}):")
for f in missing_faq[:15]:
    print(f"  - {f}")
if len(missing_faq) > 15: print(f"  ... e mais {len(missing_faq)-15}")
