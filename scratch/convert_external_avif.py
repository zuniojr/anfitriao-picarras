import os
import requests
import re
from PIL import Image
import io

images_to_process = {
    # File : [(URL, SEO-friendly name without ext, replace string)]
    "src/components/Hero.astro": [
        ("https://images.unsplash.com/photo-1541604193435-225878996aba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85", "fachada-imovel-temporada-picarras", "https://images.unsplash.com/photo-1541604193435-225878996aba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85")
    ],
    "src/pages/anuncie-seu-imovel.astro": [
        ("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85", "praia-balneario-picarras-turismo", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85"),
        ("https://images.unsplash.com/photo-1519046904884-53103b34b206?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85", "relaxamento-praia-picarras", "https://images.unsplash.com/photo-1519046904884-53103b34b206?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85")
    ],
    "src/pages/servicos.astro": [
        ("https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85", "decoracao-imovel-airbnb", "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85"),
        ("https://images.unsplash.com/photo-1541604193435-225878996aba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85", "gestao-completa-aluguel-temporada", "https://images.unsplash.com/photo-1541604193435-225878996aba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85")
    ],
    "src/pages/sobrenos.astro": [
         ("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85", "paraiso-picarras-litoral-catarinense", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85")
    ],
    "src/pages/blog/index.astro": [
         ("https://images.unsplash.com/photo-1455587734955-081b22074882?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85", "blog-tecnologia-gestao-imoveis", "https://images.unsplash.com/photo-1455587734955-081b22074882?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=85")
    ]
}

def download_and_convert(url, output_path):
    print(f"Baixando: {url}")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        try:
            image = Image.open(io.BytesIO(response.content))
            image.save(output_path, "AVIF", quality=85)
            print(f"Salvo: {output_path}")
            return True
        except Exception as e:
            print(f"Erro ao converter {url}: {e}")
            return False
    print(f"Falha ao baixar (status {response.status_code}): {url}")
    return False

images_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\public\images"
os.makedirs(images_dir, exist_ok=True)

base_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras"

for filepath, items in images_to_process.items():
    full_path = os.path.join(base_dir, filepath)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        updated = False
        for url, seo_name, replace_str in items:
            avif_filename = f"{seo_name}.avif"
            avif_path = os.path.join(images_dir, avif_filename)
            
            if not os.path.exists(avif_path):
                 success = download_and_convert(url, avif_path)
            else:
                 success = True
                 
            if success:
                new_src = f"/images/{avif_filename}"
                content = content.replace(replace_str, new_src)
                updated = True
        
        if updated:
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Arquivo atualizado: {filepath}")
    else:
        print(f"Arquivo não encontrado: {full_path}")
