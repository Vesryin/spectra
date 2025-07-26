# 🛠️ SpectraAI Developer Tooling Guide

## Overview

SpectraAI uses a modern, modular developer tooling setup designed for 2025 standards. This guide covers all the tools, configurations, and workflows implemented for maintaining code quality, consistency, and reliability.

## 🎯 Tooling Philosophy

Our developer tooling follows these core principles:

- **Modular**: Each tool has a specific purpose and can be updated independently
- **Adaptive**: Version ranges allow automatic minor/patch updates
- **Fast**: Optimized configurations for quick feedback loops
- **Consistent**: Unified code style across frontend and backend
- **Maintainable**: Well-documented configurations that evolve with the project

## 🌐 Frontend Tooling (apps/web)

### ESLint Configuration
- **File**: `.eslintrc.js`
- **Purpose**: Code quality and consistency enforcement
- **Features**:
  - TypeScript support with strict type checking
  - React/Next.js optimizations
  - Accessibility compliance (jsx-a11y)
  - Import organization and optimization
  - Testing Library integration
  - Prettier integration

### Prettier Configuration
- **File**: `.prettierrc.js`
- **Purpose**: Consistent code formatting
- **Features**:
  - Modern JavaScript/TypeScript formatting
  - File-specific overrides for optimal formatting
  - JSX and React-specific rules
  - Integration with ESLint

### Jest Testing Framework
- **File**: `jest.config.js` + `jest.setup.js`
- **Purpose**: Comprehensive testing with Next.js 14 support
- **Features**:
  - ESM modules support
  - React Testing Library integration
  - Coverage reporting with thresholds
  - Next.js App Router compatibility
  - Parallel test execution

### Available Scripts
```bash
# Linting and formatting
npm run lint           # Check code quality
npm run lint:fix       # Fix linting issues automatically
npm run format         # Format code with Prettier
npm run format:check   # Check formatting consistency

# Testing
npm run test           # Run all tests
npm run test:watch     # Run tests in watch mode
npm run test:coverage  # Run tests with coverage

# Building and development
npm run dev            # Start development server
npm run build          # Build for production
npm run type-check     # TypeScript type checking
```

## 🐍 Backend Tooling (apps/api)

### Ruff Configuration
- **File**: `pyproject.toml` (tool.ruff section)
- **Purpose**: Fast Python linting and code quality
- **Features**:
  - Modern Python syntax enforcement (Python 3.11+)
  - Comprehensive rule sets (security, performance, style)
  - Import sorting and organization
  - FastAPI-specific optimizations
  - Per-file rule customization

### Black Configuration
- **File**: `pyproject.toml` (tool.black section)
- **Purpose**: Consistent Python code formatting
- **Features**:
  - Modern Python version targeting
  - Preview features for latest syntax
  - Integration with Ruff for optimal workflow

### MyPy Configuration
- **File**: `pyproject.toml` (tool.mypy section)
- **Purpose**: Static type checking for Python
- **Features**:
  - Strict type checking mode
  - Comprehensive error reporting
  - Third-party library compatibility
  - Incremental type checking

### Pytest Configuration
- **File**: `pyproject.toml` (tool.pytest.ini_options section)
- **Purpose**: Comprehensive Python testing
- **Features**:
  - Async testing support
  - Coverage reporting with thresholds
  - Test markers for organization
  - FastAPI testing integration

### Available Scripts
```bash
# Linting and formatting (run from apps/api)
ruff check .           # Check code quality
ruff check --fix .     # Fix issues automatically
black .                # Format code with Black
black --check .        # Check formatting consistency
mypy app tests         # Type checking

# Testing
pytest                 # Run all tests
pytest -v              # Verbose test output
pytest --cov=app       # Run with coverage
pytest -m "not slow"   # Skip slow tests
```

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow
- **File**: `.github/workflows/ci.yml`
- **Purpose**: Automated quality assurance and deployment
- **Features**:
  - Matrix builds for multiple environments
  - Parallel job execution for speed
  - Comprehensive caching for performance
  - Security scanning and vulnerability checks
  - Deployment previews for pull requests

### Workflow Jobs

1. **Frontend CI** (🌐)
   - Node.js 18 & 20 matrix
   - ESLint, Prettier, TypeScript checks
   - Jest testing with coverage
   - Next.js build verification

2. **Backend CI** (🐍)
   - Python 3.11 & 3.12 matrix
   - Ruff linting, Black formatting
   - MyPy type checking
   - Pytest execution with coverage

3. **Security Scan** (🔒)
   - NPM audit for frontend dependencies
   - Bandit security scan for Python
   - Safety dependency vulnerability check

4. **Integration Tests** (🔗)
   - Cross-service testing
   - Database integration
   - End-to-end scenarios

5. **Deploy Preview** (🚀)
   - Automatic preview environments
   - PR comments with preview links

## 📦 Monorepo Management

### Turborepo Configuration
- **File**: `turbo.json`
- **Purpose**: Optimized monorepo task execution
- **Features**:
  - Parallel task execution
  - Intelligent caching
  - Dependency-aware builds
  - Cross-package script coordination

### Root Package Scripts
```bash
# Monorepo-wide operations
npm run lint           # Lint all packages
npm run format         # Format all packages
npm run test           # Test all packages
npm run build          # Build all packages

# Quality assurance
npm run quality:check  # Run all quality checks
npm run security:audit # Security audit across packages
npm run ci             # Complete CI pipeline locally
```

## 🔧 Development Workflow

### Initial Setup
```bash
# Clone repository
git clone https://github.com/Vesryin/spectra.git
cd spectra

# Install root dependencies
npm install

# Install frontend dependencies
cd apps/web && npm install && cd ../..

# Install backend dependencies
cd apps/api && pip install -r requirements.txt -r requirements-dev.txt && cd ../..
```

### Daily Development
```bash
# Start development servers
npm run dev

# Run quality checks before committing
npm run quality:check

# Run tests
npm run test

# Fix formatting issues
npm run format
```

### Pre-commit Checklist
- [ ] `npm run lint` passes
- [ ] `npm run format:check` passes
- [ ] `npm run type-check` passes
- [ ] `npm run test` passes
- [ ] All new code has appropriate tests
- [ ] Security audit clean: `npm run security:audit`

## 📊 Code Coverage

### Frontend Coverage
- **Target**: 80% minimum coverage
- **Reports**: HTML, LCOV, JSON summary
- **Location**: `apps/web/coverage/`

### Backend Coverage
- **Target**: 80% minimum coverage
- **Reports**: HTML, XML, terminal
- **Location**: `apps/api/htmlcov/`, `apps/api/coverage.xml`

### Coverage Commands
```bash
# Frontend coverage
cd apps/web && npm run test:coverage

# Backend coverage
cd apps/api && pytest --cov=app --cov-report=html

# View HTML reports
# Frontend: open apps/web/coverage/index.html
# Backend: open apps/api/htmlcov/index.html
```

## 🛡️ Security

### Dependency Scanning
- **Frontend**: NPM audit with moderate threshold
- **Backend**: Safety and Bandit security scanning
- **Automation**: Runs on every pull request

### Security Best Practices
- Regular dependency updates with Dependabot
- Automated vulnerability scanning in CI
- Security headers in production deployment
- Environment variable validation

## 🚀 Performance Optimization

### Build Performance
- Turborepo caching reduces build times by 50-80%
- Parallel task execution across packages
- Incremental builds with dependency tracking

### Test Performance
- Jest parallel execution with worker processes
- Pytest with optimized test discovery
- Coverage collection only when needed

### CI Performance
- Matrix builds run in parallel
- Comprehensive caching strategy
- Optimized Docker layers for faster builds

## 📚 Maintenance

### Updating Dependencies
```bash
# Check for updates
npm outdated
pip list --outdated

# Update frontend dependencies
cd apps/web && npm update && cd ../..

# Update backend dependencies
cd apps/api && pip install --upgrade -r requirements.txt -r requirements-dev.txt
```

### Configuration Updates
- ESLint rules: Update `.eslintrc.js` with new rules
- Prettier options: Modify `.prettierrc.js` formatting
- Ruff rules: Adjust `pyproject.toml` [tool.ruff] section
- CI workflow: Update `.github/workflows/ci.yml` for new steps

### Tool Version Management
All tools use flexible version ranges (e.g., `^8.0.0`) allowing:
- Automatic patch updates (8.0.1, 8.0.2, etc.)
- Automatic minor updates (8.1.0, 8.2.0, etc.)
- Manual major version updates (9.0.0+)

## 🎓 Learning Resources

### Documentation Links
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Prettier Options](https://prettier.io/docs/en/options.html)
- [Ruff Rules](https://docs.astral.sh/ruff/rules/)
- [Jest API](https://jestjs.io/docs/api)
- [Pytest Documentation](https://docs.pytest.org/)
- [Turborepo Docs](https://turbo.build/repo/docs)

### Best Practices
- Write tests before fixing bugs
- Use descriptive commit messages
- Keep pull requests focused and small
- Document complex business logic
- Follow established naming conventions
- Regularly update dependencies

---

**Last Updated**: July 26, 2025  
**Tooling Version**: 3.0.0  
**Compatibility**: Node.js 18+, Python 3.11+
