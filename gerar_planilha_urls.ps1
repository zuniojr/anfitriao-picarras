# =============================================================
# Script: gerar_planilha_urls.ps1
# Gera um CSV com todas as URLs do site e a URL da imagem hero
# =============================================================

$baseUrl = "https://anfitriao-picarras.com.br"
$blogDir = "$PSScriptRoot\src\content\blog"
$outputFile = "$PSScriptRoot\urls_site.csv"

$rows = [System.Collections.Generic.List[PSCustomObject]]::new()

# -------------------------------------------------------
# Funcao para ler o frontmatter de um arquivo markdown
# -------------------------------------------------------
function Get-Frontmatter {
    param([string]$filePath)
    $content = Get-Content $filePath -Raw -Encoding UTF8
    if ($content -match "(?s)^---\s*\n(.+?)\n---") {
        return $matches[1]
    }
    return ""
}

function Get-FrontmatterField {
    param([string]$frontmatter, [string]$field)
    if ($frontmatter -match "(?m)^$field\s*:\s*[`"']?(.+?)[`"']?\s*$") {
        return $matches[1].Trim('"').Trim("'").Trim()
    }
    return ""
}

# -------------------------------------------------------
# Paginas estaticas (nao-blog)
# -------------------------------------------------------
$staticPages = @(
    @{ Slug = "";                    Arquivo = "index.astro" },
    @{ Slug = "servicos";            Arquivo = "servicos.astro" },
    @{ Slug = "sobrenos";            Arquivo = "sobrenos.astro" },
    @{ Slug = "anuncie-seu-imovel";  Arquivo = "anuncie-seu-imovel.astro" },
    @{ Slug = "airbnb-picarras";     Arquivo = "airbnb-picarras.astro" }
)

foreach ($page in $staticPages) {
    $slug = $page.Slug
    $url  = if ($slug -eq "") { "$baseUrl/" } else { "$baseUrl/$slug/" }
    $rows.Add([PSCustomObject]@{
        Tipo      = "Pagina"
        URL       = $url
        URLImagem = ""
        Arquivo   = $page.Arquivo
    })
}

# -------------------------------------------------------
# Posts do Blog
# -------------------------------------------------------
$mdFiles = Get-ChildItem -Path $blogDir -Filter "*.md" | Sort-Object Name

foreach ($file in $mdFiles) {
    $fm     = Get-Frontmatter -filePath $file.FullName
    $hero   = Get-FrontmatterField -frontmatter $fm -field "heroImage"
    $slug   = $file.BaseName

    $pageUrl  = "$baseUrl/blog/$slug/"
    $imageUrl = if ($hero -ne "") { "$baseUrl$hero" } else { "" }

    $rows.Add([PSCustomObject]@{
        Tipo      = "Blog"
        URL       = $pageUrl
        URLImagem = $imageUrl
        Arquivo   = $file.Name
    })
}

# -------------------------------------------------------
# Exportar CSV
# -------------------------------------------------------
$rows | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8 -Delimiter ";"

Write-Host ""
Write-Host "Planilha gerada com sucesso!" -ForegroundColor Green
Write-Host "Arquivo: $outputFile" -ForegroundColor Cyan
Write-Host "Total de linhas: $($rows.Count)" -ForegroundColor Yellow

$comImagem = ($rows | Where-Object { $_.URLImagem -ne "" }).Count
$semImagem = ($rows | Where-Object { $_.URLImagem -eq "" }).Count
Write-Host ""
Write-Host "  Com imagem : $comImagem" -ForegroundColor Green
Write-Host "  Sem imagem : $semImagem" -ForegroundColor Red
Write-Host ""
