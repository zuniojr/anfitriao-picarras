import os
import re
import requests
from bs4 import BeautifulSoup

blog_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"

def clean_html(tag):
    # Basic HTML to MD conversion
    text = ""
    for child in tag.descendants:
        if isinstance(child, str):
            text += child
        elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text += f"\n\n{'#' * int(child.name[1])} "
        elif child.name == 'p':
            text += "\n\n"
        elif child.name == 'li':
            text += "\n* "
        elif child.name == 'br':
            text += "\n"
    
    # Clean up
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def re_extract(url, filepath):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        req = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        # Elementor specific containers found by subagent
        content_area = soup.select_one('.elementor-widget-theme-post-content') or \
                       soup.select_one('.elementor-widget-container') or \
                       soup.select_one('.entry-content') or \
                       soup.select_one('article')
        
        if not content_area:
            print(f"  Falha ao encontrar area de conteudo em {url}")
            return False

        # Extract text while preserving some structure
        text_content = clean_html(content_area)
        
        skip_patterns = [
            'Prepare-se para explorar', 'Anfitrião Piçarras', 'Compartilhe:', 
            'Veja também:', 'Colocamos o seu imóvel', 'Conheça nosso serviços',
            'Atendimento personalizado', '47', 'Copyright', 'Todos os direitos reservados'
        ]

        lines = text_content.splitlines()
        filtered_lines = []
        started = False
        for line in lines:
            line = line.strip()
            if not line: 
                filtered_lines.append("")
                continue
            
            skip = False
            for p in skip_patterns:
                if p.lower() in line.lower():
                    skip = True
                    break
            
            if skip:
                if started: break
                continue
            
            started = True
            filtered_lines.append(line)
        
        final_body = "\n".join(filtered_lines).strip()

        if len(final_body) < 100:
            print(f"  Conteudo ainda muito curto ({len(final_body)} chars) em {url}")
            return False

        # Read existing file to keep frontmatter
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            old_content = f.read()
        
        fm_match = re.match(r'^(---\s*.*?\n---\s*\n)', old_content, re.DOTALL)
        if fm_match:
            frontmatter = fm_match.group(1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + "\n" + final_body)
            print(f"  Sucesso: {filepath} ({len(final_body)} chars)")
            return True
    except Exception as e:
        print(f"  Erro em {url}: {e}")
    return False

# List from previous check
short_urls = [
    "https://anfitriaopicarras.com/ahoy-marujos-embarquem-em-uma-aventura-inesquecivel-no-passeio-de-barco-pirata-em-picarras/",
    "https://anfitriaopicarras.com/beto-carrero-world/",
    "https://anfitriaopicarras.com/como-alugar-seu-imovel-em-picarras-e-atrair-mais-turistas/",
    "https://anfitriaopicarras.com/como-atrair-mais-hospedes-para-seu-aluguel-de-temporada-em-picarras/",
    "https://anfitriaopicarras.com/como-funciona-o-airbnb-entenda-o-conceito-e-beneficios/",
    "https://anfitriaopicarras.com/dicas-essenciais-para-anfitrioes-de-airbnb-em-picarras/",
    "https://anfitriaopicarras.com/dicas-essenciais-para-o-proprietario-de-aluguel-de-temporada-em-picarras/",
    "https://anfitriaopicarras.com/dicas-para-viajantes-economize-tempo-e-dinheiro/",
    "https://anfitriaopicarras.com/explorando-as-profundezas-a-experiencia-do-museu-oceanografico-da-univali/",
    "https://anfitriaopicarras.com/guia-completo-para-ser-um-anfitriao-de-sucesso-em-picarras/",
    "https://anfitriaopicarras.com/guia-rapido-preparacao-para-receber-hospedes-no-airbnb/",
    "https://anfitriaopicarras.com/marina-park-o-melhor-local-para-sua-experiencia-nautica-em-balneario-picarras/",
    "https://anfitriaopicarras.com/o-que-fazer-em-picarras/",
    "https://anfitriaopicarras.com/quanto-cobrar-na-diaria-do-seu-imovel-de-airbnb/",
    "https://anfitriaopicarras.com/trilha-ecologica-morro-do-quininho-aventura-e-natureza-em-balneario-picarras/",
    "https://anfitriaopicarras.com/viajando-com-criancas-por-que-escolher-um-imovel-de-temporada/"
]

for url in short_urls:
    slug = url.replace("https://anfitriaopicarras.com/", "").strip("/")
    path = os.path.join(blog_dir, f"{slug}.md")
    if os.path.exists(path):
        print(f"Corrigindo {url}...")
        re_extract(url, path)
