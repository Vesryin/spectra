#!/bin/bash
# Complete Git Repository Setup Script
# Initializes git, commits all files, creates GitHub repo, links remote, and pushes to main

set -e  # Exit on any error

PROJECT_NAME="spectra"
DESCRIPTION="SpectraAI - Advanced AI Assistant with Memory, Emotions, and Personality"

echo "🚀 Starting Git repository setup for $PROJECT_NAME..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed or not in PATH"
    echo "Please install Git first: https://git-scm.com/download"
    exit 1
fi

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI is not installed or not in PATH"
    echo "Please install GitHub CLI first: https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated with GitHub CLI
if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated with GitHub CLI"
    echo "Please run: gh auth login"
    exit 1
fi

# Get current directory name for project
CURRENT_DIR=$(basename "$(pwd)")
echo "📁 Current directory: $CURRENT_DIR"

# Step 1: Initialize Git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git config --local init.defaultBranch main
else
    echo "📁 Git repository already exists"
fi

# Step 2: Configure Git user if not set globally
if [ -z "$(git config --global user.name)" ]; then
    echo "⚙️ Git user not configured globally, using GitHub info..."
    GITHUB_USER=$(gh api user --jq .login)
    GITHUB_EMAIL=$(gh api user --jq .email)
    if [ "$GITHUB_EMAIL" != "null" ] && [ -n "$GITHUB_EMAIL" ]; then
        git config --local user.email "$GITHUB_EMAIL"
    else
        git config --local user.email "$GITHUB_USER@users.noreply.github.com"
    fi
    git config --local user.name "$(gh api user --jq .name)"
fi

# Step 3: Add all files to staging
echo "📦 Adding all files to staging..."
git add .

# Step 4: Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️ No changes to commit"
else
    # Show what will be committed
    echo "📋 Files to be committed:"
    git status --short
    
    # Step 5: Create initial commit
    echo "💾 Creating initial commit..."
    git commit -m "Initial commit - uploading complete workspace"
fi

# Step 6: Get GitHub username
GITHUB_USER=$(gh api user --jq .login)
echo "👤 GitHub user: $GITHUB_USER"

# Step 7: Check if GitHub repository already exists
if gh repo view "$GITHUB_USER/$PROJECT_NAME" &> /dev/null; then
    echo "⚠️ GitHub repository $GITHUB_USER/$PROJECT_NAME already exists"
    echo "🔗 Repository URL: https://github.com/$GITHUB_USER/$PROJECT_NAME"
else
    # Step 8: Create GitHub repository
    echo "🌐 Creating GitHub repository: $PROJECT_NAME..."
    gh repo create "$PROJECT_NAME" \
        --public \
        --description "$DESCRIPTION" \
        --clone=false
    
    echo "✅ GitHub repository created successfully!"
fi

# Step 9: Add remote origin if not already added
if ! git remote get-url origin &> /dev/null; then
    echo "🔗 Adding remote origin..."
    git remote add origin "https://github.com/$GITHUB_USER/$PROJECT_NAME.git"
else
    echo "🔗 Remote origin already exists"
    # Update remote URL to ensure it's correct
    git remote set-url origin "https://github.com/$GITHUB_USER/$PROJECT_NAME.git"
fi

# Step 10: Push to GitHub
echo "⬆️ Pushing to GitHub..."
if git push -u origin main; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "⚠️ Push failed, trying to pull first..."
    git pull origin main --allow-unrelated-histories
    git push -u origin main
fi

echo ""
echo "🎉 Repository setup completed successfully!"
echo "🔗 Repository URL: https://github.com/$GITHUB_USER/$PROJECT_NAME"
echo "📊 Repository stats:"
gh repo view "$GITHUB_USER/$PROJECT_NAME" --json name,description,visibility,defaultBranch,pushedAt | jq -r '"Name: " + .name, "Description: " + .description, "Visibility: " + .visibility, "Default Branch: " + .defaultBranch, "Last Push: " + .pushedAt'

echo ""
echo "📝 Next steps:"
echo "1. Visit your repository on GitHub to verify the upload"
echo "2. Consider setting up branch protection rules"
echo "3. Add collaborators if needed"
echo "4. Set up CI/CD workflows"
echo "5. Add repository topics/tags for discoverability"
