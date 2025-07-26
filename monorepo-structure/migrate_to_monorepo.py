#!/usr/bin/env python3
"""
SpectraAI Monorepo Migration Script

This script helps migrate the existing SpectraAI project to the new monorepo structure.
It preserves working components while organizing them into a scalable architecture.
"""

import os
import shutil
import json
from pathlib import Path
from typing import Dict, List, Tuple

class SpectraAIMigrator:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.migration_log = []
        
    def log(self, message: str):
        """Log migration steps"""
        print(f"📝 {message}")
        self.migration_log.append(message)
    
    def create_directory_structure(self):
        """Create the monorepo directory structure"""
        directories = [
            "spectra-core/src",
            "spectra-core/tests",
            "spectra-api/src/api",
            "spectra-api/src/websockets", 
            "spectra-api/src/middleware",
            "spectra-api/src/models",
            "spectra-api/src/utils",
            "spectra-api/tests",
            "spectra-ui/public",
            "spectra-ui/src/components",
            "spectra-ui/src/services",
            "spectra-ui/src/hooks",
            "spectra-ui/src/utils",
            "spectra-ui/src/types",
            "spectra-tools/setup",
            "spectra-tools/scripts",
            "spectra-tools/docker",
            "spectra-tools/ci",
            "spectra-dev-notes/research",
            "spectra-dev-notes/todos",
            "spectra-dev-notes/logs",
            "spectra-dev-notes/ui-mockups",
            "docs"
        ]
        
        for directory in directories:
            dir_path = self.target_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            self.log(f"Created directory: {directory}")
    
    def migrate_core_files(self):
        """Migrate core AI files to spectra-core"""
        core_files = [
            ("core/emotions.py", "spectra-core/src/emotions.py"),
            ("core/memory.py", "spectra-core/src/memory.py"),
            ("core/personality.py", "spectra-core/src/personality.py"),
            ("core/reflection.py", "spectra-core/src/reflection.py"),
            ("logic/ai_manager.py", "spectra-core/src/ai_manager.py"),
            ("logic/ai_providers.py", "spectra-core/src/ai_providers.py"),
            ("logic/brain.py", "spectra-core/src/brain.py"),
            ("logic/planner.py", "spectra-core/src/planner.py"),
            ("logic/tools.py", "spectra-core/src/tools.py"),
            ("logic/voice.py", "spectra-core/src/voice.py"),
            ("config/settings.py", "spectra-core/src/config.py"),
            ("config/openai_config.py", "spectra-core/src/openai_config.py"),
        ]
        
        for source_file, target_file in core_files:
            self.copy_file_if_exists(source_file, target_file)
    
    def migrate_data_files(self):
        """Migrate data files"""
        data_files = [
            ("data/memory_store.json", "spectra-core/data/memory_store.json"),
            ("requirements.txt", "spectra-core/requirements.txt"),
        ]
        
        # Create data directory
        (self.target_dir / "spectra-core/data").mkdir(exist_ok=True)
        
        for source_file, target_file in data_files:
            self.copy_file_if_exists(source_file, target_file)
    
    def migrate_test_files(self):
        """Migrate test files"""
        test_files = [
            ("tests/test_emotions.py", "spectra-core/tests/test_emotions.py"),
            ("tests/test_memory.py", "spectra-core/tests/test_memory.py"),
            ("tests/test_personality.py", "spectra-core/tests/test_personality.py"),
            ("tests/conftest.py", "spectra-core/tests/conftest.py"),
        ]
        
        for source_file, target_file in test_files:
            self.copy_file_if_exists(source_file, target_file)
    
    def migrate_tools_and_scripts(self):
        """Migrate setup and utility scripts"""
        tool_files = [
            ("setup_local_ai.py", "spectra-tools/setup/install_models.py"),
            ("setup.bat", "spectra-tools/scripts/setup.bat"),
            ("launcher.py", "spectra-tools/scripts/launcher.py"),
            ("spectra_cleanup.py", "spectra-tools/scripts/cleanup.py"),
        ]
        
        for source_file, target_file in tool_files:
            self.copy_file_if_exists(source_file, target_file)
    
    def create_package_configurations(self):
        """Create package.json and other configuration files"""
        
        # Root package.json for workspace
        root_package = {
            "name": "spectra-ai-monorepo",
            "version": "1.0.0",
            "description": "SpectraAI - Advanced AI Assistant with Emotional Intelligence",
            "private": True,
            "workspaces": [
                "spectra-ui",
                "spectra-tools"
            ],
            "scripts": {
                "setup:all": "npm install && cd spectra-ui && npm install",
                "dev": "concurrently \"npm run dev:api\" \"npm run dev:ui\"",
                "dev:api": "cd spectra-api && python src/main.py",
                "dev:ui": "cd spectra-ui && npm start",
                "build:all": "npm run build:api && npm run build:ui",
                "build:api": "cd spectra-api && python -m build",
                "build:ui": "cd spectra-ui && npm run build",
                "test:all": "npm run test:core && npm run test:api && npm run test:ui",
                "test:core": "cd spectra-core && python -m pytest",
                "test:api": "cd spectra-api && python -m pytest",
                "test:ui": "cd spectra-ui && npm test",
                "lint:all": "npm run lint:api && npm run lint:ui",
                "lint:api": "cd spectra-api && python -m flake8 src/",
                "lint:ui": "cd spectra-ui && npm run lint"
            },
            "devDependencies": {
                "concurrently": "^8.2.0"
            },
            "engines": {
                "node": ">=18.0.0",
                "python": ">=3.11.0"
            }
        }
        
        self.write_json_file("package.json", root_package)
        
        # API requirements.txt
        api_requirements = [
            "fastapi>=0.104.1",
            "uvicorn[standard]>=0.24.0",
            "websockets>=12.0",
            "pydantic>=2.5.0",
            "python-multipart>=0.0.6",
            "python-dotenv>=1.0.0",
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.25.0"
        ]
        
        api_req_path = self.target_dir / "spectra-api/requirements.txt"
        with open(api_req_path, 'w') as f:
            f.write('\n'.join(api_requirements))
        self.log(f"Created API requirements.txt")
        
        # UI package.json
        ui_package = {
            "name": "spectra-ui",
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "@mui/material": "^5.15.0",
                "@mui/icons-material": "^5.15.0",
                "@emotion/react": "^11.11.0",
                "@emotion/styled": "^11.11.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-scripts": "5.0.1",
                "typescript": "^4.9.5",
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "framer-motion": "^10.16.0",
                "web-vitals": "^3.5.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject",
                "lint": "eslint src --ext .ts,.tsx"
            },
            "eslintConfig": {
                "extends": [
                    "react-app",
                    "react-app/jest"
                ]
            },
            "browserslist": {
                "production": [
                    ">0.2%",
                    "not dead",
                    "not op_mini all"
                ],
                "development": [
                    "last 1 chrome version",
                    "last 1 firefox version",
                    "last 1 safari version"
                ]
            },
            "proxy": "http://localhost:8000"
        }
        
        self.write_json_file("spectra-ui/package.json", ui_package)
    
    def create_docker_configurations(self):
        """Create Docker configurations"""
        
        # API Dockerfile
        api_dockerfile = '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
        
        self.write_file("spectra-api/Dockerfile", api_dockerfile)
        
        # UI Dockerfile
        ui_dockerfile = '''FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
'''
        
        self.write_file("spectra-ui/Dockerfile", ui_dockerfile)
        
        # Docker Compose
        docker_compose = '''version: '3.8'

services:
  spectra-api:
    build: ./spectra-api
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
    volumes:
      - ./spectra-core:/app/spectra-core
      - ./spectra-api/src:/app/src
    
  spectra-ui:
    build: ./spectra-ui
    ports:
      - "3000:80"
    depends_on:
      - spectra-api
    
  spectra-db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: spectra
      POSTGRES_USER: spectra
      POSTGRES_PASSWORD: spectra_dev_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
'''
        
        self.write_file("docker-compose.yml", docker_compose)
    
    def create_documentation(self):
        """Create initial documentation files"""
        
        # Core module README
        core_readme = '''# SpectraAI Core Engine

The heart of SpectraAI - contains all core AI processing logic.

## Components

- **AI Manager**: Model orchestration and provider management
- **Memory System**: Persistent knowledge and context storage  
- **Personality Engine**: Dynamic trait-based behavior system
- **Emotional Processing**: Real-time emotional state management
- **Brain Module**: Core reasoning and response generation

## Usage

```python
from spectra_core import SpectraAI

# Initialize SpectraAI
ai = SpectraAI()

# Process a message
response = ai.process_message("Hello, how are you?")
print(response)
```

## Configuration

See `config.py` for configuration options.
'''
        
        self.write_file("spectra-core/README.md", core_readme)
        
        # API README
        api_readme = '''# SpectraAI API Server

FastAPI-based backend providing REST and WebSocket APIs.

## Features

- RESTful endpoints for system management
- Real-time WebSocket chat interface
- Memory and personality management APIs
- System status and monitoring endpoints

## Development

```bash
cd spectra-api
pip install -r requirements.txt
python src/main.py
```

## API Documentation

Start the server and visit http://localhost:8000/docs for interactive API documentation.
'''
        
        self.write_file("spectra-api/README.md", api_readme)
        
        # UI README
        ui_readme = '''# SpectraAI Frontend

Modern React TypeScript frontend with Material-UI.

## Features

- Real-time chat interface with emotional indicators
- Memory viewer and management tools
- Personality configuration panel
- System status dashboard
- Responsive design with dark theme

## Development

```bash
cd spectra-ui
npm install
npm start
```

Open http://localhost:3000 to view the application.
'''
        
        self.write_file("spectra-ui/README.md", ui_readme)
    
    def copy_file_if_exists(self, source_path: str, target_path: str):
        """Copy file if it exists in source directory"""
        source_full = self.source_dir / source_path
        target_full = self.target_dir / target_path
        
        if source_full.exists():
            target_full.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_full, target_full)
            self.log(f"Copied: {source_path} → {target_path}")
        else:
            self.log(f"Skipped (not found): {source_path}")
    
    def write_file(self, path: str, content: str):
        """Write content to file"""
        file_path = self.target_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.log(f"Created: {path}")
    
    def write_json_file(self, path: str, data: dict):
        """Write JSON data to file"""
        file_path = self.target_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        self.log(f"Created: {path}")
    
    def run_migration(self):
        """Run the complete migration process"""
        print("🚀 Starting SpectraAI Monorepo Migration")
        print(f"📂 Source: {self.source_dir}")
        print(f"📁 Target: {self.target_dir}")
        print()
        
        try:
            self.create_directory_structure()
            self.migrate_core_files()
            self.migrate_data_files()
            self.migrate_test_files()
            self.migrate_tools_and_scripts()
            self.create_package_configurations()
            self.create_docker_configurations()
            self.create_documentation()
            
            print()
            print("✅ Migration completed successfully!")
            print(f"📝 Created {len(self.migration_log)} items")
            print()
            print("🎯 Next Steps:")
            print("1. cd to the new monorepo directory")
            print("2. Run: npm install")
            print("3. Review and test migrated components")
            print("4. Start development: npm run dev")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python migrate_to_monorepo.py <source_dir> <target_dir>")
        print("Example: python migrate_to_monorepo.py ./spectra ./SpectraAI-Monorepo")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    
    migrator = SpectraAIMigrator(source_dir, target_dir)
    migrator.run_migration()
