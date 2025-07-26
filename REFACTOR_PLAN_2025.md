# 🎯 SpectraAI 2025 Refactor Plan
# Based on MCP Configuration Audit

## 🔥 **Aggressive Cleaning Phase**

### Files to DELETE (Legacy/Bloat):
```
# Old structure (keep core logic, delete structure)
/core/
/logic/  
/config/
/frontend/
/backend/
/tests/ (old)

# Legacy files
main.py
main_new.py
launcher.py
launch.py
demo_mode.py
demo_mode_new.py
simple_demo.py
spectra_gui.py
spectra_advanced_gui.py
test_*.py (root level)

# Old monorepo attempt
/monorepo-structure/

# Version folders
/0.25.0/
/2.0.0/
/2.5.0/
/23.0.0/
/4.35.0/
```

## 🚀 **New 2025 Architecture**

### Stack Alignment (MCP Config):
- ✅ Frontend: **Next.js 14 App Router + Tailwind + ShadCN**
- ✅ Backend: **FastAPI (async)**  
- ✅ Runtime: **Vercel (frontend), Railway (backend)**
- ✅ Database: **PostgreSQL + Prisma ORM**
- ✅ Auth: **Clerk.dev**
- ✅ AI: **OpenHermes 2.5 via Ollama**

### Directory Structure (2025):
```
spectra/
├── apps/
│   ├── web/                 # Next.js 14 App Router
│   │   ├── app/            # App Router structure  
│   │   ├── components/     # ShadCN components
│   │   ├── lib/           # Utilities
│   │   └── public/        
│   └── api/                # FastAPI backend
│       ├── app/           # FastAPI app
│       ├── core/          # Business logic
│       ├── db/            # Database models
│       └── tests/         # Backend tests
├── packages/
│   ├── ui/                # Shared ShadCN components
│   ├── types/             # Shared TypeScript types
│   └── utils/             # Shared utilities
├── prisma/                # Database schema
├── docs/                  # Documentation
└── tools/                 # Development tools
```

## 🧹 **Cleaning Tasks:**

### 1. **Preserve Core AI Logic**
- Extract working AI modules to `apps/api/core/`
- Keep: ai_manager.py, memory.py, personality.py, emotions.py
- Modernize: Add type hints, async patterns, proper error handling

### 2. **Delete Legacy Structure**  
- Remove all duplicate/old folders
- Clean out experimental files
- Remove version-specific folders

### 3. **Modernize Dependencies**
- Frontend: Next.js 14.2+, React 18+, ShadCN, Tailwind 3.4+
- Backend: FastAPI 0.110+, Prisma, modern Python libs
- Dev: Turborepo, TypeScript 5.4+, ESLint 9+

### 4. **Professional Configuration**
- Turbo monorepo setup
- Modern linting (ESLint 9, Ruff)
- Type safety enforcement
- Docker containerization
- CI/CD with GitHub Actions

## 📋 **Implementation Order:**

### Phase 1: Clean Slate
1. Backup working AI modules
2. Delete legacy structure
3. Create new 2025 architecture
4. Setup Turborepo + package.json

### Phase 2: Backend Modernization  
1. FastAPI with async patterns
2. PostgreSQL + Prisma setup
3. AI core integration
4. Type hints + documentation

### Phase 3: Frontend Rebuild
1. Next.js 14 App Router
2. ShadCN component library
3. Real-time chat interface
4. Memory/personality dashboard

### Phase 4: Production Ready
1. Authentication (Clerk)
2. Database deployment
3. CI/CD pipeline
4. Monitoring + logging

## 🎨 **Design Principles (MCP Aligned):**

- **Lyrical, clear, intelligent, minimalist**
- **Modular architecture enforced**
- **Type safety required**
- **Modern async patterns**
- **Test coverage required**
- **Auto-documentation**

---

**Ready to execute this aggressive refactor?** 🚀
