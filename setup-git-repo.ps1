# Git Repository Setup Script for SpectraAI
# This PowerShell script initializes a Git repository, commits all files, and pushes to GitHub

Write-Host "🚀 Setting up Git repository for SpectraAI..." -ForegroundColor Cyan

# Step 1: Initialize Git repository
Write-Host "📁 Initializing Git repository..." -ForegroundColor Yellow
git init

# Step 2: Configure Git
Write-Host "⚙️ Configuring Git..." -ForegroundColor Yellow
git config --local init.defaultBranch main

# Step 3: Add all files to staging
Write-Host "📦 Adding all files to staging..." -ForegroundColor Yellow
git add .

# Step 4: Check what we're about to commit
Write-Host "📋 Files to be committed:" -ForegroundColor Yellow
git status --short

# Step 5: Create initial commit
Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
git commit -m "Initial commit - uploading complete workspace"

# Step 6: Create GitHub repository (assumes GitHub CLI is installed and authenticated)
Write-Host "🌐 Creating GitHub repository..." -ForegroundColor Yellow
gh repo create spectra --public --description "SpectraAI - Advanced AI Assistant with Memory, Emotions, and Personality" --clone=$false

# Step 7: Add remote origin
Write-Host "🔗 Adding remote origin..." -ForegroundColor Yellow
$username = gh api user --jq .login
git remote add origin "https://github.com/$username/spectra.git"

# Step 8: Push to GitHub
Write-Host "⬆️ Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host "✅ Repository successfully created and pushed to GitHub!" -ForegroundColor Green
Write-Host "🔗 Repository URL: https://github.com/$username/spectra" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Visit your repository on GitHub to verify the upload"
Write-Host "2. Consider setting up branch protection rules"
Write-Host "3. Add collaborators if needed"
Write-Host "4. Set up CI/CD workflows"
