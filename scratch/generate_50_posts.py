import os
import re
from datetime import datetime

# Estrutura das 50 postagens (5 de cada uma das 10 categorias)
posts = {
    "Praias e Natureza": [
        "As melhores praias de Balneário Piçarras para conhecer neste verão",
        "Praia de Piçarras: por que ela possui certificação Bandeira Azul?",
        "Mapa completo das praias de Balneário Piçarras: qual escolher?",
        "Trilhas ecológicas em Balneário Piçarras para os amantes da natureza",
        "Ilhas Itacolomi: como visitar e o que fazer nesse paraíso em Piçarras"
    ],
    "O Que Fazer": [
        "O que fazer em Balneário Piçarras: roteiro completo de 3 dias",
        "O que fazer em Balneário Piçarras com chuva? 7 atrações imperdíveis",
        "Pontos turísticos de Balneário Piçarras que você não pode deixar de visitar",
        "Passeio pelo molhe de Balneário Piçarras: vistas e dicas",
        "O que fazer de graça em Balneário Piçarras: roteiro econômico"
    ],
    "Gastronomia": [
        "Onde comer em Balneário Piçarras: top 10 restaurantes imperdíveis",
        "Melhores frutos do mar de Balneário Piçarras (Guia atualizado)",
        "Pizzarias e hamburguerias em Balneário Piçarras para um lanche noturno",
        "Bares e barzinhos em Balneário Piçarras: onde curtir a noite",
        "5 cafés charmosos em Balneário Piçarras para conhecer à tarde"
    ],
    "Hospedagem e Airbnb": [
        "Onde ficar em Balneário Piçarras: melhores bairros para turistas",
        "Por que fechar um Airbnb em Balneário Piçarras é melhor que hotel?",
        "Casas de temporada frente ao mar em Balneário Piçarras: como escolher",
        "Aluguel de temporada em Piçarras para famílias grandes: dicas práticas",
        "Como escolher o Airbnb ideal em Balneário Piçarras para casais"
    ],
    "Morar e Investir": [
        "Como é morar em Balneário Piçarras? (Vantagens e qualidade de vida)",
        "Mercado imobiliário de Piçarras: por que os preços estão subindo?",
        "Custo de vida em Balneário Piçarras: guia completo e sincero",
        "Melhores bairros para comprar imóvel em Balneário Piçarras",
        "Balneário Piçarras é uma cidade segura? Taxas de criminalidade"
    ],
    "Viagem em Família": [
        "Guia prático de viagem para Balneário Piçarras com bebês",
        "Parquinhos e praças para crianças em Balneário Piçarras",
        "Onde levar os filhos para jantar em Piçarras (Espaço Kids)",
        "Cuidados essenciais com as crianças nas praias do litoral de SC",
        "Lojas de artigos de praia e brinquedos na cidade de Piçarras"
    ],
    "Dicas de Viagem": [
        "Como chegar a Balneário Piçarras: guia de voos, ônibus e rodovias",
        "Qual é o aeroporto mais próximo de Balneário Piçarras?",
        "Uber e táxi em Balneário Piçarras: como se locomover na cidade?",
        "Guia de supermercados em Balneário Piçarras para quem faz mercado",
        "Estacionamento nas ruas de Piçarras: como funciona na alta temporada?"
    ],
    "Atrações Vizinhas": [
        "Como ir de Balneário Piçarras ao Beto Carrero World (Guia de transporte)",
        "Hospedar em Piçarras ou Penha? Qual é a melhor opção?",
        "5 atrações na cidade vizinha de Penha para conhecer em 1 dia",
        "Visita bate-volta ao Cristo Luz em Balneário Camboriú saindo de Piçarras",
        "Roteiro de meio dia em Itajaí para quem está em Balneário Piçarras"
    ],
    "Cultura e História": [
        "A história de Balneário Piçarras: de vila de pescadores a sucesso imobiliário",
        "Museu Oceanográfico da Univali: por que vale a visita? (Próximo à Piçarras)",
        "Festas culturais e tradicionais que acontecem ao longo do ano em Piçarras",
        "Artesanato local de Piçarras: onde comprar lembrancinhas",
        "A origem do nome Piçarras: uma curiosidade histórica"
    ],
    "Nichos Específicos": [
        "Balneário Piçarras no Inverno: O que fazer na baixa temporada?",
        "Semana Santa e feriados de Páscoa: dicas de viagem para Piçarras",
        "Ecoturismo: observação de pássaros e baleias em diferentes épocas",
        "Piçarras para terceira idade: rotas calmas e acessíveis",
        "Roteiro romântico em Balneário Piçarras para Lua de Mel"
    ]
}

def generate_slug(title):
    # Transliteration for common portuguese characters
    accents = {
        'a': ['á', 'à', 'â', 'ã', 'ä'],
        'e': ['é', 'è', 'ê', 'ë'],
        'i': ['í', 'ì', 'î', 'ï'],
        'o': ['ó', 'ò', 'ô', 'õ', 'ö'],
        'u': ['ú', 'ù', 'û', 'ü'],
        'c': ['ç']
    }
    
    slug = title.lower()
    for char, accented_chars in accents.items():
        for ac in accented_chars:
            slug = slug.replace(ac, char)
            
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    return slug

def generate_frontmatter(title, slug, category):
    today = datetime.now().strftime("%Y-%m-%d")
    
    template = f"""---
title: "{title}"
description: "Guia completo sobre {title.lower()}. O que você precisa saber para aproveitar o melhor de Balneário Piçarras."
pubDate: {today}
heroImage: "/images/blog/{slug}.avif"
tags: ["Balneário Piçarras", "{category}"]
---

## Problema

[Insira aqui a dor ou dúvida principal do leitor relacionada a este tema. O que ele está buscando resolver? Ex: Aumentar faturamento, escolher a praia certa, encontrar segurança para as crianças...]

## Agitação

[Aprofunde o problema. O que acontece se ele tomar a decisão errada? (Turista: frustração na viagem | Proprietário: perda de dinheiro e dor de cabeça)]

## Solução

[Apresente as dicas, guia ou instruções como a solução ideal. Estruture em listas, passos ou tópicos detalhados sobre {title}.]

### Conclusão

[Resuma os pontos principais respondendo a promessa inicial do título.]

*** 

### CTA (Chamada para Ação)

**Para Proprietários:** Se você tem um imóvel em Balneário Piçarras e quer transformar ele em uma máquina de rendimento sem ter dores de cabeça com a operação, fale com a **Anfitrião Piçarras**. Somos especialistas na gestão profissional de Airbnb e aluguéis de temporada na cidade. [Saiba como podemos te ajudar.](/gestao-de-imoveis)

**Para Turistas:** Planejando sua viagem para a região do Beto Carrero e Balneário Piçarras? Escolha a segurança de se hospedar com um anfitrião profissional. [Confira nossos imóveis disponíveis para a sua próxima viagem.](/)
"""
    return template

# Executar a criação na pasta blog
base_path = r"c:\Users\Osmar Junior\Documents\01 Antigravity\Anfitriao-Picarras\anfitriao-piçarras\src\content\blog"

os.makedirs(base_path, exist_ok=True)

count = 0
for category, titles in posts.items():
    for title in titles:
        slug = generate_slug(title)
        filename = f"{slug}.md"
        filepath = os.path.join(base_path, filename)
        
        if not os.path.exists(filepath):
            content = generate_frontmatter(title, slug, category)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            print(f"Criado: {filename}")
        else:
            print(f"Já existe: {filename}")

print(f"\\nProcesso concluí. {count} novos arquivos foram gerados com sucesso na estrutura PAS e SEO.")
