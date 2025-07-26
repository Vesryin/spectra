/**
 * 🎨 Prettier Configuration for SpectraAI Frontend
 * Modern formatting rules following 2025 best practices
 *
 * Philosophy:
 * - Consistency over personal preference
 * - Optimized for team collaboration and readability
 * - Framework-specific optimizations (React, Next.js, TypeScript)
 * - File-type specific formatting for better maintainability
 * - CI/CD integration friendly
 *
 * Features:
 * - Adaptive line lengths based on file type
 * - Context-aware formatting for different languages
 * - Team workflow optimization
 * - Editor-agnostic configuration
 * - Performance optimized for large codebases
 *
 * Maintenance:
 * - Overrides are organized by file type
 * - Comments explain formatting decisions
 * - Compatible with ESLint and other tools
 * - Easily extendable for new file types
 */

module.exports = {
  // ===== CORE FORMATTING RULES =====
  // Semicolons for explicit statement termination
  semi: true,

  // Trailing commas improve git diffs and future-proof object literals
  trailingComma: 'es5',

  // Single quotes for consistency and readability
  singleQuote: true,

  // 80 characters - optimal for code review and side-by-side editing
  printWidth: 80,

  // 2 spaces for clean, consistent indentation
  tabWidth: 2,
  useTabs: false,

  // LF line endings for cross-platform compatibility
  endOfLine: 'lf',

  // ===== REACT & JSX SPECIFIC =====
  // Single quotes in JSX for consistency with JavaScript
  jsxSingleQuote: true,

  // Bracket formatting for better readability
  bracketSpacing: true,
  bracketSameLine: false,

  // Arrow function parentheses only when necessary
  arrowParens: 'avoid',

  // ===== ADVANCED FORMATTING OPTIONS =====
  // Embedded language formatting (CSS-in-JS, etc.)
  embeddedLanguageFormatting: 'auto',

  // HTML whitespace handling for proper rendering
  htmlWhitespaceSensitivity: 'css',

  // Pragma handling for conditional formatting
  insertPragma: false,
  requirePragma: false,

  // Prose formatting for documentation
  proseWrap: 'preserve',

  // Quote properties only when necessary
  quoteProps: 'as-needed',

  // Vue.js specific (for potential future use)
  vueIndentScriptAndStyle: false,

  // ===== FILE-SPECIFIC OVERRIDES =====
  overrides: [
    // ===== MARKDOWN FILES =====
    // Documentation and README files
    {
      files: ['*.md', '*.mdx'],
      options: {
        printWidth: 100,
        proseWrap: 'always',
        tabWidth: 2,
        // Preserve emphasis markers
        embeddedLanguageFormatting: 'auto',
      },
    },

    // ===== JSON FILES =====
    // Configuration and data files
    {
      files: ['*.json', '*.jsonc'],
      options: {
        printWidth: 100,
        tabWidth: 2,
        // Keep JSON compact but readable
        trailingComma: 'none',
      },
    },

    // ===== YAML FILES =====
    // CI/CD and configuration files
    {
      files: ['*.yml', '*.yaml'],
      options: {
        tabWidth: 2,
        singleQuote: false, // YAML prefers double quotes
        // Maintain YAML structure integrity
        proseWrap: 'preserve',
      },
    },

    // ===== CONFIGURATION FILES =====
    // Build tools and framework configs
    {
      files: [
        '*.config.js',
        '*.config.ts',
        '*.config.mjs',
        '*.config.cjs',
        '.eslintrc.js',
        'tailwind.config.js',
        'next.config.js',
        'jest.config.js',
        'vite.config.js',
        'rollup.config.js',
        'webpack.config.js',
      ],
      options: {
        printWidth: 100,
        tabWidth: 2,
        // Configuration files can be slightly longer
        singleQuote: true,
      },
    },

    // ===== PACKAGE.JSON =====
    // Special handling for package manifests
    {
      files: ['package.json'],
      options: {
        printWidth: 120,
        tabWidth: 2,
        // Keep dependencies readable
        trailingComma: 'none',
      },
    },

    // ===== CSS & STYLING FILES =====
    // Stylesheets and CSS-in-JS
    {
      files: ['*.css', '*.scss', '*.sass', '*.less'],
      options: {
        printWidth: 120,
        tabWidth: 2,
        singleQuote: false, // CSS prefers double quotes
      },
    },

    // ===== TypeScript DECLARATION FILES =====
    // Type definitions
    {
      files: ['*.d.ts'],
      options: {
        printWidth: 120,
        // Type declarations can be more verbose
        trailingComma: 'all',
      },
    },

    // ===== SHELL SCRIPTS =====
    // Automation and deployment scripts
    {
      files: ['*.sh', '*.bash'],
      options: {
        printWidth: 120,
        tabWidth: 4, // Shell scripts often use 4 spaces
        useTabs: false,
      },
    },
  ],

  // ===== PLUGIN CONFIGURATIONS =====
  // Future plugin support
  plugins: [
    // Plugins will be added here as needed
    // '@prettier/plugin-xml',
    // 'prettier-plugin-tailwindcss',
  ],
};
