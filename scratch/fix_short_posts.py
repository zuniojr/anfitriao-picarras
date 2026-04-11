import os
import re
import requests
from bs4 import BeautifulSoup

blog_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"

def clean_html(inner_html):
    # Basic HTML to MD conversion
    text = str(inner_html)
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text)
    text = re.sub(r'<b>(.*?)</b>', r'**\1**', text)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text)
    text = re.sub(r'<i>(.*?)</i>', r'*\1*', text)
    text = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', text)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    # Entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&#8211;', '-')
    return text.strip()

def re_extract(url, filepath):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        req = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        # Try to find the content area
        content_area = soup.find('div', class_='entry-content') or \
                       soup.find('div', class_='post-content') or \
                       soup.find('div', class_='content') or \
                       soup.find('article')
        
        if not content_area:
            print(f"  Falha ao encontrar area de conteudo em {url}")
            return False

        # Extract elements
        elements = content_area.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'blockquote'])
        
        skip_patterns = [
            'Prepare-se para explorar', 'Anfitrião Piçarras', 'Compartilhe:', 
            'Veja também:', 'Colocamos o seu imóvel', 'Conheça nosso serviços',
            'Atendimento personalizado', '47', 'Copyright', 'Todos os direitos reservados'
        ]

        article_md = []
        started = False
        for el in elements:
            text = clean_html(el)
            if len(text) < 3: continue
            
            skip = False
            for p in skip_patterns:
                if p.lower() in text.lower():
                    skip = True
                    break
            if skip:
                if started: break
                continue
            
            tag = el.name
            if tag.startswith('h'):
                started = True
                level = tag[1]
                article_md.append(f"\n{'#' * int(level)} {text}\n")
            elif tag == 'p':
                started = True
                article_md.append(f"{text}\n")
            elif tag == 'li':
                started = True
                article_md.append(f"* {text}")
            elif tag == 'blockquote':
                started = True
                article_md.append(f"> {text}\n")
        
        if not article_md:
            print(f"  Conteudo vazio apos limpeza em {url}")
            return False

        # Read existing file to keep frontmatter
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            old_content = f.read()
        
        fm_match = re.match(r'^(---\s*.*?\n---\s*\n)', old_content, re.DOTALL)
        if fm_match:
            frontmatter = fm_match.group(1)
            new_body = "\n".join(article_md)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + "\n" + new_body)
            print(f"  Sucesso: {filepath}")
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
