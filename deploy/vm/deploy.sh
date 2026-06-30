#!/bin/bash

# Define directories
BACKEND_DIR="/opt/apilog-backend"
FRONTEND_DIR="/opt/apilog-frontend"

# Deploy backend
echo "Deploying backend..."
cd $BACKEND_DIR || { echo "Backend directory not found!"; exit 1; }
git pull || { echo "Failed to pull backend repository!"; exit 1; }

# Activate virtual environment, install requirements, run migrations, and deactivate
echo "Setting up backend environment..."
source .venv/bin/activate || { echo "Failed to activate virtual environment!"; exit 1; }
pip install -r requirements.txt || { echo "Failed to install requirements!"; deactivate; exit 1; }
python manage.py migrate || { echo "Failed to run migrations!"; deactivate; exit 1; }
deactivate

sudo systemctl restart gunicorn.service || { echo "Failed to restart Gunicorn service!"; exit 1; }

# Deploy frontend
echo "Deploying frontend..."
cd $FRONTEND_DIR || { echo "Frontend directory not found!"; exit 1; }
git pull || { echo "Failed to pull frontend repository!"; exit 1; }
npm run build || { echo "Failed to build frontend!"; exit 1; }
sudo systemctl restart nginx || { echo "Failed to restart Nginx!"; exit 1; }

echo "Deployment completed successfully!"