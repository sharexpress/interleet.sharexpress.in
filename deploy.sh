#!/bin/bash

# Interleet Deployment Script
# Automatically stages, pushes, and deploys to the remote server at 192.168.29.104

set -e

echo "🚀 Starting Interleet deployment..."

# 1. Commit and push local changes
echo "📦 Staging and pushing local changes to GitHub..."
git add -A
if ! git diff-index --quiet HEAD --; then
    echo "💾 Committing changes..."
    git commit -m "deploy: automated production deployment"
    echo "📤 Pushing to main..."
    git push origin main
else
    echo "✅ No local changes to commit."
fi

# 2. Upload backend .env file to remote server
echo "🔑 Copying backend environment configuration (.env) to remote server..."
sshpass -p 'santusht' scp -o StrictHostKeyChecking=no backend/.env santusht@192.168.29.104:/home/santusht/desktop/projects/interleet/backend/.env

# 3. Pull changes and build on remote server
echo "🖥️ Connecting to remote server to pull & build..."
sshpass -p 'santusht' ssh -o StrictHostKeyChecking=no santusht@192.168.29.104 'bash -s' << 'ENDSSH'
    set -e
    echo "⬇️ Pulling latest changes from Git..."
    cd /home/santusht/desktop/projects/interleet
    
    # Fetch and hard reset to match the rewritten remote history
    git fetch origin
    git reset --hard origin/main
    
    echo "🏗️ Building frontend assets..."
    cd frontend
    npm run build
    
    echo "⚙️ Updating Nginx configuration..."
    echo "santusht" | sudo -S cp /home/santusht/desktop/projects/interleet/nginx/interleet-backend.conf /etc/nginx/sites-available/interleet-backend
    echo "santusht" | sudo -S nginx -t
    echo "santusht" | sudo -S systemctl reload nginx
    
    echo "🔄 Starting load-balanced backend processes (PM2)..."
    # Delete the legacy single process if it exists to release port 8000
    pm2 delete interleet || true
    
    # Start or reload the 4 backend instances defined in the ecosystem config
    cd backend
    pm2 startOrReload ecosystem.config.cjs --update-env
    
    echo "🎉 Remote deployment successfully completed!"
ENDSSH

echo "✨ Deployment complete!"
