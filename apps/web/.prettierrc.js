/**
 * Prettier Configuration for SpectraAI Frontend
 * Modern formatting rules following 2025 best practices
 *
 * Features:
 * - Consistent code formatting across the project
 * - Optimized for readability and maintainability
 * - Compatible with ESLint and team workflows
 * - File-specific overrides for different formats
 */

module.exports = {
  // Core formatting rules
  semi: true,
  trailingComma: 'es5',
  singleQuote: true,
  printWidth: 80,
  tabWidth: 2,
  useTabs: false,
  endOfLine: 'lf',

  // JSX and React specific
  jsxSingleQuote: true,
  bracketSpacing: true,
  bracketSameLine: false,
  arrowParens: 'avoid',

  // Advanced formatting
  embeddedLanguageFormatting: 'auto',
  htmlWhitespaceSensitivity: 'css',
  insertPragma: false,
  proseWrap: 'preserve',
  quoteProps: 'as-needed',
  requirePragma: false,
  vueIndentScriptAndStyle: false,

  // File-specific overrides for optimal formatting
  overrides: [
    // Markdown files - optimized for documentation
    {
      files: '*.md',
      options: {
        printWidth: 100,
        proseWrap: 'always',
        tabWidth: 2,
      },
    },

    // JSON files - compact but readable
    {
      files: ['*.json', '*.jsonc'],
      options: {
        printWidth: 100,
        tabWidth: 2,
      },
    },

    // YAML files - standard indentation
    {
      files: ['*.yml', '*.yaml'],
      options: {
        tabWidth: 2,
        singleQuote: false,
      },
    },

    // Configuration files - more lenient line length
    {
      files: [
        '*.config.js',
        '*.config.ts',
        '*.config.mjs',
        '.eslintrc.js',
        'tailwind.config.js',
      ],
      options: {
        printWidth: 100,
      },
    },

    // Package.json - maintain standard formatting
    {
      files: 'package.json',
      options: {
        printWidth: 120,
        tabWidth: 2,
      },
    },
  ],
};
