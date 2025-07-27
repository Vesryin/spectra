/**
 * Validation utilities and schemas using Zod
 */

import { z } from 'zod';

// User validation schemas
export const emailSchema = z.string().email('Invalid email address');

export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
  .regex(/[a-z]/, 'Password must contain at least one lowercase letter')
  .regex(/[0-9]/, 'Password must contain at least one number')
  .regex(/[^A-Za-z0-9]/, 'Password must contain at least one special character');

export const userRegistrationSchema = z.object({
  email: emailSchema,
  password: passwordSchema,
  fullName: z.string().min(2, 'Full name must be at least 2 characters').optional(),
});

export const userLoginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, 'Password is required'),
});

// Chat validation schemas
export const chatMessageSchema = z.object({
  message: z.string().min(1, 'Message cannot be empty').max(4000, 'Message too long'),
  conversationId: z.string().uuid().optional(),
  stream: z.boolean().default(false),
  temperature: z.number().min(0).max(2).default(0.8).optional(),
  maxTokens: z.number().min(1).max(4000).default(500).optional(),
});

// Memory validation schemas
export const memoryTypeSchema = z.enum(['conversation', 'fact', 'preference', 'emotion', 'context']);

export const memoryImportanceSchema = z.enum(['low', 'medium', 'high', 'critical']);

export const memoryCreateSchema = z.object({
  content: z.string().min(1, 'Content cannot be empty').max(2000, 'Content too long'),
  type: memoryTypeSchema,
  importance: memoryImportanceSchema.default('medium'),
  tags: z.array(z.string()).default([]),
  metadata: z.record(z.any()).default({}),
});

export const memorySearchSchema = z.object({
  query: z.string().min(1, 'Search query cannot be empty').max(500, 'Query too long'),
  types: z.array(memoryTypeSchema).optional(),
  importance: z.array(memoryImportanceSchema).optional(),
  tags: z.array(z.string()).optional(),
  limit: z.number().min(1).max(100).default(10),
});

// Common validation schemas
export const uuidSchema = z.string().uuid('Invalid UUID format');

export const paginationSchema = z.object({
  page: z.number().min(1).default(1),
  limit: z.number().min(1).max(100).default(20),
  sort: z.string().optional(),
  order: z.enum(['asc', 'desc']).default('desc'),
});

// File upload validation
export const fileUploadSchema = z.object({
  filename: z.string().min(1, 'Filename is required'),
  mimetype: z.string().min(1, 'MIME type is required'),
  size: z.number().max(10 * 1024 * 1024, 'File size cannot exceed 10MB'), // 10MB limit
});

// Settings validation
export const userPreferencesSchema = z.object({
  theme: z.enum(['light', 'dark', 'system']).default('system'),
  language: z.string().min(2).max(5).default('en'),
  timezone: z.string().default('UTC'),
  notifications: z.object({
    email: z.boolean().default(true),
    push: z.boolean().default(true),
    aiResponses: z.boolean().default(true),
    systemUpdates: z.boolean().default(false),
  }).default({}),
});

// Validation utility functions
export const validateEmail = (email: string): boolean => {
  return emailSchema.safeParse(email).success;
};

export const validatePassword = (password: string): boolean => {
  return passwordSchema.safeParse(password).success;
};

export const validateUuid = (id: string): boolean => {
  return uuidSchema.safeParse(id).success;
};

export const sanitizeHtml = (input: string): string => {
  // Basic HTML sanitization (in production, use a proper library like DOMPurify)
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
};

export const validateAndSanitize = <T>(schema: z.ZodSchema<T>, data: unknown): T => {
  const result = schema.safeParse(data);
  if (!result.success) {
    throw new Error(`Validation failed: ${result.error.message}`);
  }
  return result.data;
};
