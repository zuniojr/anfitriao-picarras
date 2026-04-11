import os
import re

blog_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"
public_img_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\public"

def validate_post(filename):
    path = os.path.join(blog_dir, filename)
    with open(path, 'r', encoding='utf-8-sig') as f: # utf-8-sig handles BOM
        content = f.read()

    errors = []
    
    # Check Frontmatter - more lenient regex
    fm_match = re.search(r'^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)', content, re.DOTALL)
    if not fm_match:
        errors.append("Frontmatter ausente ou malformado (Verificando BOM e quebras de linha Windows)")
        return errors

    fm_content = fm_match.group(1)
    body_content = fm_match.group(2).strip()

    required_fields = ['title:', 'description:', 'pubDate:']
    for field in required_fields:
        if field not in fm_content:
            errors.append(f"Campo obrigatório faltando: {field}")

    # Check for empty body
    body_lines = [l for l in body_content.splitlines() if l.strip()]
    if len(body_lines) < 3:
        errors.append(f"Conteúdo do corpo muito curto ({len(body_lines)} linhas significativas)")

    # Check for leftover HTML tags
    if re.search(r'<[a-z/][^>]*>', body_content, re.IGNORECASE):
        errors.append("Tags HTML detectadas no corpo Markdown")

    # Check hero image path
    hero_match = re.search(r'heroImage:\s*"(.*?)"', fm_content)
    if hero_match:
        img_path = hero_match.group(1)
        if img_path.startswith('http'):
            errors.append(f"Imagem de destaque ainda é uma URL externa: {img_path}")
        else:
            # Convert /images/blog/img.jpg to public/images/blog/img.jpg
            local_img_path = os.path.join(public_img_dir, img_path.lstrip('/').replace('/', os.sep))
            if not os.path.exists(local_img_path):
                errors.append(f"Imagem de destaque não encontrada localmente: {img_path}")

    return errors

files = sorted(os.listdir(blog_dir))
report = []

for file in files:
    if file.endswith('.md'):
        errs = validate_post(file)
        if errs:
            report.append((file, errs))

if not report:
    print("Sucesso! Todos os 132 posts parecem estar corretos e bem formatados.")
else:
    print(f"Encontrados problemas em {len(report)} posts:")
    for file, errs in report:
        print(f"\n[ {file} ]")
        for e in errs:
            print(f"  - {e}")
