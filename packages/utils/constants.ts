/**
 * Application constants
 */

// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000';

// Authentication
export const TOKEN_KEY = 'spectra_auth_token';
export const REFRESH_TOKEN_KEY = 'spectra_refresh_token';
export const USER_KEY = 'spectra_user';

// Local Storage Keys
export const STORAGE_KEYS = {
  THEME: 'spectra_theme',
  LANGUAGE: 'spectra_language',
  SETTINGS: 'spectra_settings',
  CONVERSATION_DRAFTS: 'spectra_conversation_drafts',
  RECENT_SEARCHES: 'spectra_recent_searches',
} as const;

// Application Limits
export const LIMITS = {
  MESSAGE_MAX_LENGTH: 4000,
  MEMORY_MAX_LENGTH: 2000,
  FILE_MAX_SIZE: 10 * 1024 * 1024, // 10MB
  CONVERSATION_TITLE_MAX_LENGTH: 100,
  TAG_MAX_LENGTH: 50,
  TAGS_MAX_COUNT: 10,
} as const;

// Pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
  CONVERSATIONS_PAGE_SIZE: 10,
  MEMORIES_PAGE_SIZE: 25,
} as const;

// Timeouts and Intervals
export const TIMEOUTS = {
  API_REQUEST: 30000, // 30 seconds
  WEBSOCKET_RECONNECT: 5000, // 5 seconds
  DEBOUNCE_SEARCH: 300, // 300ms
  TOAST_DURATION: 5000, // 5 seconds
  SESSION_CHECK: 60000, // 1 minute
} as const;

// AI Configuration
export const AI_CONFIG = {
  DEFAULT_TEMPERATURE: 0.8,
  DEFAULT_MAX_TOKENS: 500,
  MIN_TEMPERATURE: 0.0,
  MAX_TEMPERATURE: 2.0,
  MIN_TOKENS: 1,
  MAX_TOKENS: 4000,
} as const;

// Supported File Types
export const SUPPORTED_FILE_TYPES = {
  IMAGES: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
  DOCUMENTS: ['application/pdf', 'text/plain', 'text/markdown'],
  AUDIO: ['audio/mpeg', 'audio/wav', 'audio/ogg'],
} as const;

// Emotion Categories
export const EMOTIONS = {
  POSITIVE: ['joy', 'excitement', 'love', 'gratitude', 'hope', 'pride'],
  NEGATIVE: ['sadness', 'anger', 'fear', 'disgust', 'shame', 'guilt'],
  NEUTRAL: ['curiosity', 'surprise', 'confusion', 'contemplation'],
} as const;

// Color Themes
export const THEME_COLORS = {
  PRIMARY: {
    50: '#f0f9ff',
    100: '#e0f2fe',
    500: '#0ea5e9',
    600: '#0284c7',
    700: '#0369a1',
    900: '#0c4a6e',
  },
  GRAY: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    500: '#6b7280',
    700: '#374151',
    900: '#111827',
  },
} as const;

// Route Paths
export const ROUTES = {
  HOME: '/',
  CHAT: '/chat',
  CONVERSATIONS: '/conversations',
  MEMORY: '/memory',
  SETTINGS: '/settings',
  PROFILE: '/profile',
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  RESET_PASSWORD: '/auth/reset-password',
} as const;

// API Endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/auth/login',
    REGISTER: '/auth/register',
    REFRESH: '/auth/refresh',
    LOGOUT: '/auth/logout',
    ME: '/auth/me',
  },
  CHAT: {
    SEND: '/chat/send',
    CONVERSATIONS: '/chat/conversations',
    HISTORY: (id: string) => `/chat/conversations/${id}`,
    DELETE: (id: string) => `/chat/conversations/${id}`,
    STREAM: (id: string) => `/chat/stream/${id}`,
  },
  MEMORY: {
    CREATE: '/memory',
    LIST: '/memory',
    GET: (id: string) => `/memory/${id}`,
    UPDATE: (id: string) => `/memory/${id}`,
    DELETE: (id: string) => `/memory/${id}`,
    SEARCH: '/memory/search',
    STATS: '/memory/stats/overview',
    CLEANUP: '/memory/cleanup',
  },
  HEALTH: {
    CHECK: '/health',
    LIVE: '/health/live',
    READY: '/health/ready',
  },
} as const;

// WebSocket Events
export const WS_EVENTS = {
  CONNECT: 'connect',
  DISCONNECT: 'disconnect',
  MESSAGE: 'message',
  CHAT_MESSAGE: 'chat_message',
  CHAT_RESPONSE: 'chat_response',
  TYPING_START: 'typing_start',
  TYPING_STOP: 'typing_stop',
  ERROR: 'error',
} as const;

// Error Codes
export const ERROR_CODES = {
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  RATE_LIMIT: 'RATE_LIMIT',
  SERVER_ERROR: 'SERVER_ERROR',
  NETWORK_ERROR: 'NETWORK_ERROR',
  TIMEOUT: 'TIMEOUT',
} as const;

// Feature Flags
export const FEATURES = {
  VOICE_INPUT: process.env.NEXT_PUBLIC_FEATURE_VOICE === 'true',
  IMAGE_UPLOAD: process.env.NEXT_PUBLIC_FEATURE_IMAGES === 'true',
  MEMORY_EXPORT: process.env.NEXT_PUBLIC_FEATURE_EXPORT === 'true',
  ANALYTICS: process.env.NEXT_PUBLIC_FEATURE_ANALYTICS === 'true',
} as const;

// Regular Expressions
export const REGEX = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PASSWORD: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
  URL: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_+.~#?&//=]*)$/,
  PHONE: /^\+?[\d\s\-()]+$/,
  UUID: /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i,
} as const;
