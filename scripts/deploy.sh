#!/usr/bin/env bash
# Copyright 2026 Sharexpress Contributors
# Production Git-based deployment script for Interleet
set -e

REPO_DIR="/root/projects/interleet"
FRONTEND_DEST="/var/www/interleet-frontend"

echo "=================================================="
echo "🚀 [Interleet Deploy] Git-based Deployment"
echo "=================================================="

cd "$REPO_DIR"

echo "📥 [1/4] Pulling latest tracked commits from GitHub..."
git fetch origin main
git reset --hard origin/main

echo "🧪 [2/4] Running frontend quality checks & build..."
cd "$REPO_DIR/frontend"
npm install --prefer-offline --no-audit --no-fund
npm run build

echo "🌐 [3/4] Updating /var/www/interleet-frontend..."
mkdir -p "$FRONTEND_DEST"
cp -r dist/* "$FRONTEND_DEST/"

echo "🔄 [4/5] Reloading backend services..."
cd "$REPO_DIR/backend"
if pm2 describe interleet-backend > /dev/null 2>&1; then
  pm2 reload interleet-backend --update-env
fi

echo "🌱 [5/5] Seeding database curriculum..."
if [ -f "$REPO_DIR/backend/.venv/bin/python" ]; then
  "$REPO_DIR/backend/.venv/bin/python" seed_sql_curriculum.py
fi

echo "=================================================="
echo "✅ [Interleet Deploy] Successfully deployed commit: $(git rev-parse --short HEAD)"
echo "   Branch: $(git branch --show-current)"
echo "   Time:   $(date)"
echo "=================================================="
