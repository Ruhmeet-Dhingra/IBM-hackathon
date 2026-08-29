$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$pythonw = Join-Path $projectRoot ".venv\Scripts\pythonw.exe"
$launcher = Join-Path $projectRoot "rov_background.pyw"

if (-not (Test-Path -LiteralPath $pythonw)) {
    throw "ROV virtual-environment launcher not found: $pythonw"
}

if (-not (Test-Path -LiteralPath $launcher)) {
    throw "ROV background launcher not found: $launcher"
}

$startupDirectory = [Environment]::GetFolderPath("Startup")
$shortcutPath = Join-Path $startupDirectory "ROV.lnk"
$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $pythonw
$shortcut.Arguments = '"' + $launcher + '"'
$shortcut.WorkingDirectory = $projectRoot
$shortcut.Description = "Start the ROV desktop assistant after sign-in."
$shortcut.WindowStyle = 7
$shortcut.Save()

Write-Output "ROV will start automatically after your next Windows sign-in."
