param(
    [Parameter(Mandatory=$true, HelpMessage="Enter your GitHub username")]
    [string]$GitHubUsername,

    [Parameter(Mandatory=$false)]
    [string]$RepoName = "groww-sip-suite"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "DEPLOYING GROWW SIP SUITE TO GITHUB FOR STREAMLIT CLOUD" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "GitHub Username: $GitHubUsername"
Write-Host "Repository Name: $RepoName"
Write-Host ""

$targetDir = "c:\Users\jangr\Documents\NextLeap\Project\Project2"
Set-Location $targetDir

# Check if origin already exists
$existingRemote = git remote get-url origin 2>$null
$remoteUrl = "https://github.com/$GitHubUsername/$RepoName.git"

if ($existingRemote) {
    Write-Host "Updating existing git remote origin to: $remoteUrl" -ForegroundColor Yellow
    git remote set-url origin $remoteUrl
} else {
    Write-Host "Adding git remote origin: $remoteUrl" -ForegroundColor Green
    git remote add origin $remoteUrl
}

git branch -M main

Write-Host "Pushing code to $remoteUrl..." -ForegroundColor Green
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Code is live on GitHub." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Step: Deploy on Streamlit Cloud (share.streamlit.io):" -ForegroundColor Cyan
    Write-Host "1. Visit: https://share.streamlit.io"
    Write-Host "2. Click 'New App'"
    Write-Host "3. Select Repository: $GitHubUsername/$RepoName"
    Write-Host "4. Branch: main"
    Write-Host "5. Main file path: app.py"
    Write-Host "6. In 'Advanced Settings' -> 'Secrets', add:"
    Write-Host "   GEMINI_API_KEY = `"YOUR_KEY`""
    Write-Host "7. Click 'Deploy'!"
} else {
    Write-Host "Push failed. Ensure you have created the empty repository on GitHub first at: https://github.com/new" -ForegroundColor Red
}

