param(
    [string]$Url,
    [string]$OutputDir = ".\src\content\blog"
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    "Accept" = "text/html,application/xhtml+xml"
    "Accept-Language" = "pt-BR,pt;q=0.9"
}

function Clean-Html {
    param([string]$text)
    $text = $text -replace '<strong>([^<]*)</strong>', '**$1**'
    $text = $text -replace '<b>([^<]*)</b>', '**$1**'
    $text = $text -replace '<em>([^<]*)</em>', '*$1*'
    $text = $text -replace '<i>([^<]*)</i>', '*$1*'
    $text = $text -replace '<a[^>]+href="([^"]+)"[^>]*>([^<]*)</a>', '[$2]($1)'
    $text = $text -replace '<br\s*/?>', "`n"
    $text = $text -replace '<[^>]+>', ''
    $text = $text -replace '&nbsp;', ' '
    $text = $text -replace '&hellip;', '...'
    $text = $text -replace '&amp;', '&'
    $text = $text -replace '&#8211;', '-'
    $text = $text -replace '&#8220;|&#8221;', '"'
    $text = $text -replace '&#8217;', "'"
    $text = $text -replace '&#8216;', "'"
    $text = $text -replace '&#8230;', '...'
    $text = $text -replace '\s+', ' '
    return $text.Trim()
}

try {
    $response = Invoke-WebRequest -Uri $Url -Headers $headers -UseBasicParsing
    $bytes = $response.RawContentStream.ToArray()
    $html = [System.Text.Encoding]::UTF8.GetString($bytes)

    $slug = ($Url -replace 'https://anfitriaopicarras.com/', '' -replace '/$', '').Trim()

    # Extract title
    $title = ""
    if ($html -match '<title>([^<]+)</title>') {
        $title = $matches[1] -replace '\s*-\s*Anfitri.*$', ''
        $title = $title.Trim()
    }

    # Extract date
    $date = "2024-01-01"
    if ($html -match 'article:published_time"\s+content="([^"]+)"') {
        $date = ($matches[1] -split 'T')[0]
    }

    # Extract meta description
    $metaDesc = ""
    if ($html -match 'property="og:description"\s+content="([^"]+)"') {
        $metaDesc = $matches[1]
        $metaDesc = Clean-Html $metaDesc
    } elseif ($html -match 'name="description"\s+content="([^"]+)"') {
        $metaDesc = Clean-Html $matches[1]
    }
    if ($metaDesc.Length -gt 200) {
        $metaDesc = $metaDesc.Substring(0, 197) + "..."
    }

    # Extract first body image for hero
    $heroImage = ""
    $bodyImages = @()
    $imgMatches = [regex]::Matches($html, '<img[^>]+src="([^"]+)"[^>]*>')
    foreach ($m in $imgMatches) {
        $src = $m.Groups[1].Value
        if ($src -notmatch 'logo|icon|avatar|gravatar|pixel|tracking|plugins|svg|data:' -and $src -match '\.(jpg|jpeg|png|webp|avif)') {
            $bodyImages += $src
        }
    }
    if ($bodyImages.Count -gt 0) {
        $heroImage = $bodyImages[0]
    }

    $heroImageLocal = ""
    if ($heroImage) {
        $imgName = [System.IO.Path]::GetFileName(($heroImage -split '\?')[0])
        $heroImageLocal = "/images/blog/$imgName"
    }

    # ===== Extract content using regex (not line-by-line) =====
    $opts = [System.Text.RegularExpressions.RegexOptions]::Singleline
    $articleContent = [System.Collections.ArrayList]@()

    # Find all content elements in order of appearance
    $allElements = [regex]::Matches($html, '<(h[1-6]|p|li|ul|ol|blockquote)[^>]*>(.*?)</\1>', $opts)
    
    $skipPatterns = @(
        'Prepare-se para explorar novos horizontes',
        'Estamos ansiosos para compartilhar',
        'Anfitrião Piçarras',
        'Compartilhe:',
        'Veja também:',
        'Colocamos o seu imóvel',
        'Conheça nosso serviços',
        'Deixe-nos ajudá-lo',
        'Copyright',
        'Todos os direitos reservados',
        'Atendimento personalizado e dinâmico',
        'A locação de temporada permite',
        'Além de ganhar mais',
        'A locação de temporada é mais rentável',
        'Você trabalhou duro para construir',
        '\(47\)',
        'Posts recentes',
        'Categorias'
    )
    
    $startedContent = $false
    $lastWasList = $false
    
    foreach ($el in $allElements) {
        $tag = $el.Groups[1].Value
        $inner = $el.Groups[2].Value
        $cleanText = Clean-Html $inner
        
        # Skip empty or very short
        if ($cleanText.Length -lt 3) { continue }
        
        # Skip known non-content
        $skip = $false
        foreach ($sp in $skipPatterns) {
            if ($cleanText -match $sp) { $skip = $true; break }
        }
        if ($skip) { 
            if ($startedContent) { break }  # Stop if we hit footer after content started
            continue 
        }
        
        switch -Regex ($tag) {
            'h1' {
                if (-not $startedContent -and $cleanText -ne 'Blog') {
                    $startedContent = $true
                }
            }
            'h2' {
                if ($cleanText -match 'Compartilhe|Veja também|Sobre|Contato|Anfitrião') { break }
                $startedContent = $true
                if ($lastWasList) { [void]$articleContent.Add(""); $lastWasList = $false }
                [void]$articleContent.Add("")
                [void]$articleContent.Add("## $cleanText")
                [void]$articleContent.Add("")
            }
            'h3' {
                $startedContent = $true
                if ($lastWasList) { [void]$articleContent.Add(""); $lastWasList = $false }
                [void]$articleContent.Add("")
                [void]$articleContent.Add("### $cleanText")
                [void]$articleContent.Add("")
            }
            'h4' {
                $startedContent = $true
                [void]$articleContent.Add("")
                [void]$articleContent.Add("#### $cleanText")
                [void]$articleContent.Add("")
            }
            'p' {
                if ($startedContent -and $cleanText.Length -gt 10) {
                    if ($lastWasList) { [void]$articleContent.Add(""); $lastWasList = $false }
                    [void]$articleContent.Add($cleanText)
                    [void]$articleContent.Add("")
                }
            }
            'li' {
                if ($startedContent -and $cleanText.Length -gt 2) {
                    [void]$articleContent.Add("* $cleanText")
                    $lastWasList = $true
                }
            }
        }
    }

    # Build markdown
    $titleFM = $title -replace '"', '\"'
    $metaDescFM = $metaDesc -replace '"', '\"'

    $md = @()
    $md += "---"
    $md += "title: `"$titleFM`""
    $md += "description: `"$metaDescFM`""
    $md += "pubDate: $date"
    if ($heroImageLocal) {
        $md += "heroImage: `"$heroImageLocal`""
    }
    $md += "---"
    $md += ""
    $md += ($articleContent -join "`n")
    $md += ""

    $content = $md -join "`n"
    $outputPath = Join-Path $OutputDir "$slug.md"
    [System.IO.File]::WriteAllText($outputPath, $content, [System.Text.Encoding]::UTF8)

    Write-Output "OK: $slug.md ($($articleContent.Count) linhas)"
    Write-Output "    Titulo: $title"
    Write-Output "    Data: $date"
    Write-Output "    Hero: $heroImageLocal"
    
    # Download hero image
    if ($heroImage) {
        $imgDir = ".\public\images\blog"
        if (-not (Test-Path $imgDir)) { New-Item -ItemType Directory -Path $imgDir -Force | Out-Null }
        $imgName = [System.IO.Path]::GetFileName(($heroImage -split '\?')[0])
        $imgPath = Join-Path $imgDir $imgName
        if (-not (Test-Path $imgPath)) {
            try {
                Invoke-WebRequest -Uri $heroImage -OutFile $imgPath -UseBasicParsing -Headers @{"User-Agent"="Mozilla/5.0"}
                Write-Output "    IMG OK: $imgName"
            } catch {
                Write-Output "    IMG ERRO: $imgName - $_"
            }
        } else {
            Write-Output "    IMG existe: $imgName"
        }
    }
}
catch {
    Write-Error "ERRO: $Url - $_"
}
