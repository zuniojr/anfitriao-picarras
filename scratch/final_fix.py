import os
import re

blog_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"

# Fixes for specific files
fixes = {
    "anfitriao-de-temporada.md": "Anfitriao-picarras.png",
    "como-ser-um-anfitriao-de-temporada-de-sucesso-em-picarras.md": "Anfitriao-picarras.png",
    "alugar-seu-imovel-ou-desfrutar.md": "unsplash-photo-1560185009-5bf9f3cd1bd8.jpg",
    "aluguel-de-temporada-em-balneario-picarras-guia-completo.md": "unsplash-photo-1541604193435-225878996aba.jpg",
    "as-vantagens-de-se-hospedar-em-uma-casa-com-piscina.md": "unsplash-photo-1540339832862-4745191f4134.jpg"
}

for filename, img_name in fixes.items():
    path = os.path.join(blog_dir, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Replace whatever is in heroImage: "..."
        new_content = re.sub(r'heroImage: ".*?"', f'heroImage: "/images/blog/{img_name}"', content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {filename}")

print("Final checks done.")
