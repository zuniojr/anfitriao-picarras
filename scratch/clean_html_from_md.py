import os
import re

blog_dir = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"

def html_to_md(text):
    # Convert common tags
    text = re.sub(r'<(strong|b)>(.*?)</\1>', r'**\2**', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<(em|i)>(.*?)</\1>', r'*\2*', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    # Remove all other tags
    text = re.sub(r'<[^>]+>', '', text)
    # Final cleanup of entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&#8211;', '-').replace('&#8217;', "'")
    return text

files_cleaned = 0

for filename in os.listdir(blog_dir):
    if filename.endswith('.md'):
        path = os.path.join(blog_dir, filename)
        with open(path, 'r', encoding='utf-8-sig') as f:
            full_content = f.read()
        
        # Preserve frontmatter
        parts = re.split(r'(---\s*\r?\n)', full_content, maxsplit=2)
        if len(parts) >= 4:
            # parts[0] is empty, parts[1] is '---', parts[2] is frontmatter, parts[3] is '---', parts[4] is body
            # But re.split with capture group keeps the delimiter
            # More reliable split:
            match = re.search(r'^(---\s*\r?\n.*?\r?\n---\s*\r?\n)(.*)', full_content, re.DOTALL)
            if match:
                frontmatter = match.group(1)
                body = match.group(2)
                
                new_body = html_to_md(body)
                
                if new_body.strip() != body.strip():
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(frontmatter + new_body)
                    files_cleaned += 1

print(f"Limpeza concluída! {files_cleaned} arquivos foram limpos de tags HTML.")
