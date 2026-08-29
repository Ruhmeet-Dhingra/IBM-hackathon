$shortcutPath = Join-Path ([Environment]::GetFolderPath("Startup")) "ROV.lnk"

if (Test-Path -LiteralPath $shortcutPath) {
    Remove-Item -LiteralPath $shortcutPath
}

Write-Output "ROV automatic startup has been removed."
