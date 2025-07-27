/**
 * AI-related type definitions
 */

export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface AIResponse {
  id: string;
  content: string;
  emotions: Record<string, number>;
  confidence: number;
  processingTime: number;
  modelUsed: string;
  metadata?: Record<string, any>;
}

export interface Conversation {
  id: string;
  title: string;
  messages: ChatMessage[];
  userId: string;
  createdAt: Date;
  updatedAt: Date;
  metadata?: Record<string, any>;
}

export interface AIProvider {
  name: string;
  version: string;
  capabilities: AICapability[];
  isAvailable: boolean;
}

export type AICapability = 
  | 'text-generation'
  | 'text-completion'
  | 'conversation'
  | 'code-generation'
  | 'image-analysis'
  | 'voice-synthesis'
  | 'emotion-analysis';

export interface ChatRequest {
  message: string;
  conversationId?: string;
  stream?: boolean;
  temperature?: number;
  maxTokens?: number;
  provider?: string;
}

export interface StreamChunk {
  type: 'chunk' | 'complete' | 'error';
  content?: string;
  chunkId?: number;
  isFinal?: boolean;
  emotions?: Record<string, number>;
  confidence?: number;
  error?: string;
}

export interface EmotionState {
  primary: string;
  confidence: number;
  emotions: Record<string, number>;
  timestamp: Date;
}
