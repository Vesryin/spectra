/**
 * ESLint Configuration for SpectraAI Frontend
 * Modern, adaptive configuration following 2025 best practices
 */

module.exports = {
  root: true,
  extends: ['next/core-web-vitals', 'prettier'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  plugins: ['@typescript-eslint', 'prettier'],
  rules: {
    'prettier/prettier': 'error',
    'react/react-in-jsx-scope': 'off',
    'react/prop-types': 'off',
    '@typescript-eslint/no-unused-vars': [
      'error',
      {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
      },
    ],
    'prefer-const': 'error',
    'no-var': 'error',
  },
  ignorePatterns: ['node_modules/', '.next/', 'out/', 'build/', 'dist/', 'coverage/'],
};
