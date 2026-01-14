# PowerShell script to setup Git and GitHub repository
# Run this script with: powershell -ExecutionPolicy Bypass -File setup-git.ps1

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "ALLOTMENT DASHBOARD - Git Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Git is installed
Write-Host "Step 1: Checking if Git is installed..." -ForegroundColor Yellow
$gitVersion = git --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Git is already installed: $gitVersion" -ForegroundColor Green
} else {
    Write-Host "Git is NOT installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "After installation, run this script again." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Step 2: Initializing git repository..." -ForegroundColor Yellow

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

Write-Host "✓ Git initialized" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Adding all files..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green
Write-Host ""

Write-Host "Step 4: Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit: Allotment Dashboard - Premium dental scheduling system"
Write-Host "✓ Initial commit created" -ForegroundColor Green
Write-Host ""

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to GitHub.com and create a NEW repository" -ForegroundColor Yellow
Write-Host "   - Click the '+' icon and select 'New repository'" -ForegroundColor Cyan
Write-Host "   - Name it: ALLOTMENT-TDB (or your preferred name)" -ForegroundColor Cyan
Write-Host "   - Description: Premium dental scheduling dashboard" -ForegroundColor Cyan
Write-Host "   - Choose visibility: Public or Private" -ForegroundColor Cyan
Write-Host "   - Click 'Create repository'" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Copy the repository URL from GitHub (https://github.com/YOUR_USERNAME/REPO_NAME.git)" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. Run this command in this folder:" -ForegroundColor Yellow
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Then run:" -ForegroundColor Yellow
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Setup Complete! ✓" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
