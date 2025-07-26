#!/bin/bash
# Git Repository Setup Script for SpectraAI
# This script initializes a Git repository, commits all files, and pushes to GitHub

echo "🚀 Setting up Git repository for SpectraAI..."

# Step 1: Initialize Git repository
echo "📁 Initializing Git repository..."
git init

# Step 2: Configure Git (adjust these if needed)
echo "⚙️ Configuring Git..."
git config --local init.defaultBranch main

# Step 3: Add all files to staging
echo "📦 Adding all files to staging..."
git add .

# Step 4: Check what we're about to commit
echo "📋 Files to be committed:"
git status --short

# Step 5: Create initial commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit - uploading complete workspace"

# Step 6: Create GitHub repository (assumes GitHub CLI is installed and authenticated)
echo "🌐 Creating GitHub repository..."
gh repo create spectra --public --description "SpectraAI - Advanced AI Assistant with Memory, Emotions, and Personality" --clone=false

# Step 7: Add remote origin
echo "🔗 Adding remote origin..."
git remote add origin https://github.com/$(gh api user --jq .login)/spectra.git

# Step 8: Push to GitHub
echo "⬆️ Pushing to GitHub..."
git push -u origin main

echo "✅ Repository successfully created and pushed to GitHub!"
echo "🔗 Repository URL: https://github.com/$(gh api user --jq .login)/spectra"
echo ""
echo "Next steps:"
echo "1. Visit your repository on GitHub to verify the upload"
echo "2. Consider setting up branch protection rules"
echo "3. Add collaborators if needed"
echo "4. Set up CI/CD workflows"
