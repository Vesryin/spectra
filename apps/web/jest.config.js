/**
 * Jest Configuration for SpectraAI Frontend
 * Modern testing setup with Next.js 14 and ESM support
 *
 * Features:
 * - Next.js App Router compatibility
 * - TypeScript support
 * - ESM modules handling
 * - React Testing Library integration
 * - Coverage reporting
 * - Optimized for CI/CD
 */

const nextJest = require('next/jest');

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files
  dir: './',
});

const customJestConfig = {
  // Test environment
  testEnvironment: 'jsdom',

  // Setup files
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

  // Module paths and aliases
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/$1',
    '^@/components/(.*)$': '<rootDir>/components/$1',
    '^@/pages/(.*)$': '<rootDir>/pages/$1',
    '^@/lib/(.*)$': '<rootDir>/lib/$1',
    '^@/utils/(.*)$': '<rootDir>/utils/$1',
    '^@/hooks/(.*)$': '<rootDir>/hooks/$1',
    '^@/types/(.*)$': '<rootDir>/types/$1',
    '^@/styles/(.*)$': '<rootDir>/styles/$1',
  },

  // Test file patterns
  testMatch: ['**/__tests__/**/*.(js|jsx|ts|tsx)', '**/*.(test|spec).(js|jsx|ts|tsx)'],

  // Transform configuration
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { presets: ['next/babel'] }],
  },

  // Module file extensions
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],

  // Coverage configuration
  collectCoverageFrom: [
    'app/**/*.{js,jsx,ts,tsx}',
    'components/**/*.{js,jsx,ts,tsx}',
    'lib/**/*.{js,jsx,ts,tsx}',
    'utils/**/*.{js,jsx,ts,tsx}',
    'hooks/**/*.{js,jsx,ts,tsx}',
    '!**/*.d.ts',
    '!**/node_modules/**',
    '!**/.next/**',
    '!**/coverage/**',
    '!**/dist/**',
    '!**/build/**',
  ],

  // Coverage thresholds for quality assurance
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },

  // Coverage reporters
  coverageReporters: ['text', 'html', 'lcov', 'json-summary'],

  // Test environment options
  testEnvironmentOptions: {
    customExportConditions: [''],
  },

  // Files to ignore
  testPathIgnorePatterns: [
    '<rootDir>/.next/',
    '<rootDir>/node_modules/',
    '<rootDir>/dist/',
    '<rootDir>/build/',
    '<rootDir>/coverage/',
  ],

  // Globals available in tests
  globals: {
    'ts-jest': {
      tsconfig: {
        jsx: 'react-jsx',
      },
    },
  },

  // Clear mocks between tests
  clearMocks: true,

  // Restore mocks after each test
  restoreMocks: true,

  // Verbose output for debugging
  verbose: false,

  // Maximum worker processes for parallel testing
  maxWorkers: '50%',
};

// Create and export the Jest configuration
module.exports = createJestConfig(customJestConfig);
