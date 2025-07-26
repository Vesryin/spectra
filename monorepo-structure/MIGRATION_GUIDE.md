# 🚀 SpectraAI Monorepo Migration Guide

## 📋 Pre-Migration Checklist

### ✅ Current Working Components
- [x] OpenHermes-2.5-Mistral-7B model integration
- [x] Core AI logic (ai_manager, memory, personality, emotions)
- [x] Basic configuration system
- [x] Memory storage system
- [x] Cleanup and setup utilities

### 🛠️ What We'll Preserve
- All working Python modules
- Configuration files and data
- Model setup scripts
- Memory data (`memory_store.json`)
- Test files

## 🎯 Migration Steps

### Step 1: Create Target Directory
```bash
# Outside your current workspace
mkdir SpectraAI-Monorepo
cd SpectraAI-Monorepo
```

### Step 2: Run Migration Script
```bash
# Copy the migration script to your current directory
python migrate_to_monorepo.py ../spectra ./

# Or manually run each step below
```

### Step 3: Manual Migration (Alternative)

If you prefer to do it manually:

#### 3.1 Create Directory Structure
```bash
mkdir -p spectra-core/{src,tests,data}
mkdir -p spectra-api/{src/{api,websockets,middleware,models,utils},tests}
mkdir -p spectra-ui/{public,src/{components,services,hooks,utils,types}}
mkdir -p spectra-tools/{setup,scripts,docker,ci}
mkdir -p spectra-dev-notes/{research,todos,logs,ui-mockups}
mkdir -p docs
```

#### 3.2 Copy Core Files
```bash
# Core AI modules
cp ../spectra/core/*.py spectra-core/src/
cp ../spectra/logic/*.py spectra-core/src/
cp ../spectra/config/settings.py spectra-core/src/config.py
cp ../spectra/config/openai_config.py spectra-core/src/

# Data files
cp ../spectra/data/memory_store.json spectra-core/data/
cp ../spectra/requirements.txt spectra-core/

# Test files
cp ../spectra/tests/*.py spectra-core/tests/

# Tools and scripts
cp ../spectra/setup_local_ai.py spectra-tools/setup/install_models.py
cp ../spectra/setup.bat spectra-tools/scripts/
cp ../spectra/launcher.py spectra-tools/scripts/
cp ../spectra/spectra_cleanup.py spectra-tools/scripts/cleanup.py
```

#### 3.3 Create Configuration Files

**Root package.json:**
```json
{
  "name": "spectra-ai-monorepo",
  "version": "1.0.0",
  "private": true,
  "workspaces": ["spectra-ui"],
  "scripts": {
    "setup:all": "npm install && cd spectra-ui && npm install",
    "dev": "concurrently \"npm run dev:api\" \"npm run dev:ui\"",
    "dev:api": "cd spectra-api && python src/main.py",
    "dev:ui": "cd spectra-ui && npm start"
  },
  "devDependencies": {
    "concurrently": "^8.2.0"
  }
}
```

**spectra-api/requirements.txt:**
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
websockets>=12.0
pydantic>=2.5.0
python-multipart>=0.0.6
python-dotenv>=1.0.0
```

**spectra-ui/package.json:**
```json
{
  "name": "spectra-ui",
  "version": "1.0.0",
  "dependencies": {
    "@mui/material": "^5.15.0",
    "@mui/icons-material": "^5.15.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^4.9.5"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  },
  "proxy": "http://localhost:8000"
}
```

### Step 4: Create Initial API Structure

**spectra-api/src/main.py:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add spectra-core to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../spectra-core/src'))

from ai_manager import AIManager
from memory import MemorySystem
from personality import PersonalitySystem

app = FastAPI(title="SpectraAI API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core systems
ai_manager = AIManager()
memory_system = MemorySystem()
personality_system = PersonalitySystem()

@app.get("/")
async def root():
    return {"message": "SpectraAI API Server"}

@app.get("/api/status")
async def get_status():
    return {
        "status": "online",
        "active_provider": ai_manager.get_current_provider(),
        "memory_count": len(memory_system.get_all_memories()),
        "uptime": "Just started"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Step 5: Create Basic React App

**spectra-ui/src/App.tsx:**
```tsx
import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Box, Typography, Paper } from '@mui/material';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#00d4aa' },
    background: { default: '#0a0e1a', paper: '#16213e' }
  }
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ p: 3 }}>
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>
            ✨ SpectraAI Console
          </Typography>
          <Typography variant="body1">
            Monorepo migration successful! 🎉
          </Typography>
        </Paper>
      </Box>
    </ThemeProvider>
  );
}

export default App;
```

**spectra-ui/src/index.tsx:**
```tsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(<App />);
```

**spectra-ui/public/index.html:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>SpectraAI Console</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>
```

### Step 6: Test the Migration

```bash
# Install dependencies
npm install

# Install UI dependencies
cd spectra-ui && npm install && cd ..

# Test API server
cd spectra-api && python src/main.py

# In another terminal, test UI
cd spectra-ui && npm start
```

## 🎯 Post-Migration Tasks

### Immediate (Day 1)
- [ ] Verify all core modules import correctly
- [ ] Test basic API endpoints
- [ ] Ensure React app builds and runs
- [ ] Check that memory data is accessible

### Short-term (Week 1)
- [ ] Implement complete API endpoints
- [ ] Build React components for chat interface
- [ ] Setup WebSocket communication
- [ ] Create memory management UI

### Medium-term (Month 1)
- [ ] Add comprehensive testing
- [ ] Setup CI/CD pipeline
- [ ] Docker containerization
- [ ] Production deployment setup

## 🚨 Troubleshooting

### Common Issues

**Import Errors:**
- Ensure `sys.path.append()` is correct in API main.py
- Check that all Python modules are in the right locations

**Node Module Issues:**
- Run `npm install` in both root and spectra-ui
- Clear node_modules and reinstall if needed

**Port Conflicts:**
- API runs on port 8000
- UI runs on port 3000
- Change ports in configuration if needed

## 🎊 Success Indicators

✅ **Migration Complete When:**
- [ ] API server starts without errors
- [ ] React UI builds and displays
- [ ] Core AI modules import successfully
- [ ] Memory system loads existing data
- [ ] Basic chat functionality works

---

*Remember: This migration preserves all your working code while setting up a professional, scalable structure for future development!*
