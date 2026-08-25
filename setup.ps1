param(
    [Parameter(Mandatory=$true)][string]$Username,
    [Parameter(Mandatory=$true)][string]$Name,
    [Parameter(Mandatory=$true)][string]$Image,
    [switch]$Circle
)

Write-Host "Installing dependency (pillow)..."
pip install pillow

Write-Host "Replacing placeholders in README.md and workflows..."
$files = @("README.md", ".github/workflows/metrics.yml")
foreach ($f in $files) {
    (Get-Content $f) -replace "YOUR_USERNAME", $Username -replace "YOUR NAME", $Name -replace "Shafiq-456", $Username | Set-Content $f
}

Write-Host "Generating portrait..."
$circleFlag = ""
if ($Circle) { $circleFlag = "--circle" }
python scripts/dotify.py $Image -o assets/portrait --cols 100 --equalize --detail 0.5 --color $circleFlag

Write-Host "Generating radars..."
python scripts/radar.py --data assets/skills.json -o assets/radar
python scripts/radar.py --github $Username -o assets/radar-langs --limit 7 --values --curve 0.4 --exclude "shell,makefile,dockerfile,batchfile,procfile"

Write-Host "Generating stat + project cards..."
python scripts/cards.py --user $Username --out assets

Write-Host "Done. Open preview.html to check the result before pushing."
