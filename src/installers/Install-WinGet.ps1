# 1. Download the required WinGet application bundle from Microsoft
Invoke-WebRequest -Uri "https://aka.ms" -OutFile "$env:TEMP\winget.msixbundle"

# 2. Install it directly into the current user's app package layout
Add-AppxPackage -Path "$env:TEMP\winget.msixbundle"

# 3. Clean up the downloaded installer bundle
Remove-Item "$env:TEMP\winget.msixbundle" -Force