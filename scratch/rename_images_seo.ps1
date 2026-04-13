# Script para renomear imagens unsplash para nomes SEO-friendly
# e atualizar as referencias nos posts Markdown

$blogImagesPath = "public\images\blog"
$postsPath = "src\content\blog"

# Mapa de renomemacao: nome-antigo -> nome-seo-novo
# Gerado com base nos titulos dos posts que usam cada imagem
$renameMap = @{}

# Pegar todos os posts e identificar quais usam imagens unsplash
$posts = Get-ChildItem -Path $postsPath -Filter "*.md"

foreach ($post in $posts) {
    $content = Get-Content $post.FullName -Raw -Encoding UTF8
    
    # Encontrar heroImage no frontmatter
    if ($content -match 'heroImage:\s*[''"]?(/images/blog/)(unsplash[^''">\s]+\.avif)[''"]?') {
        $oldImageName = $Matches[2]
        
        # Gerar nome SEO baseado no nome do arquivo do post (ja e SEO-friendly)
        $postSlug = $post.BaseName
        $newImageName = "$postSlug.avif"
        
        if (-not $renameMap.ContainsKey($oldImageName)) {
            $renameMap[$oldImageName] = $newImageName
            Write-Host "Mapeando: $oldImageName -> $newImageName"
        } else {
            # Imagem ja mapeada para outro post, precisa de sufixo unico
            $existing = $renameMap[$oldImageName]
            Write-Host "AVISO: $oldImageName ja mapeada para $existing, post $($post.Name) vai reusar"
        }
    }
}

Write-Host "`n=== RENOMEANDO ARQUIVOS ==="
$renamed = @{}

foreach ($oldName in $renameMap.Keys) {
    $newName = $renameMap[$oldName]
    $oldPath = Join-Path $blogImagesPath $oldName
    $newPath = Join-Path $blogImagesPath $newName
    
    if (Test-Path $oldPath) {
        if (-not (Test-Path $newPath)) {
            Rename-Item -Path $oldPath -NewName $newName
            Write-Host "OK: $oldName -> $newName"
            $renamed[$oldName] = $newName
        } else {
            Write-Host "SKIP (destino existe): $newName"
            $renamed[$oldName] = $newName
        }
    } else {
        Write-Host "NAO ENCONTRADO: $oldPath"
    }
}

Write-Host "`n=== ATUALIZANDO POSTS MARKDOWN ==="

foreach ($post in $posts) {
    $content = Get-Content $post.FullName -Raw -Encoding UTF8
    $updated = $false
    
    foreach ($oldName in $renamed.Keys) {
        $newName = $renamed[$oldName]
        if ($content -match [regex]::Escape($oldName)) {
            $content = $content -replace [regex]::Escape($oldName), $newName
            $updated = $true
            Write-Host "Atualizado: $($post.Name) [$oldName -> $newName]"
        }
    }
    
    if ($updated) {
        Set-Content -Path $post.FullName -Value $content -Encoding UTF8 -NoNewline
    }
}

Write-Host "`n=== CONCLUIDO ==="
Write-Host "Total de imagens renomeadas: $($renamed.Count)"
