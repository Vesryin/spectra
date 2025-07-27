/**
 * Memory and knowledge management types
 */

export type MemoryType = 
  | 'conversation'
  | 'fact'
  | 'preference'
  | 'emotion'
  | 'context';

export type MemoryImportance = 
  | 'low'
  | 'medium'
  | 'high'
  | 'critical';

export interface Memory {
  id: string;
  content: string;
  type: MemoryType;
  importance: MemoryImportance;
  tags: string[];
  userId: string;
  conversationId?: string;
  createdAt: Date;
  updatedAt: Date;
  accessCount: number;
  metadata?: Record<string, any>;
}

export interface MemorySearchQuery {
  query: string;
  types?: MemoryType[];
  importance?: MemoryImportance[];
  tags?: string[];
  userId?: string;
  limit?: number;
  offset?: number;
}

export interface MemorySearchResult {
  memory: Memory;
  relevanceScore: number;
  matchedTerms: string[];
}

export interface MemoryStats {
  totalMemories: number;
  byType: Record<MemoryType, number>;
  byImportance: Record<MemoryImportance, number>;
  recentMemories: number;
  storageSizeMb: number;
  topTags: Array<{ tag: string; count: number }>;
}

export interface MemoryCluster {
  id: string;
  theme: string;
  memories: Memory[];
  relevanceScore: number;
  createdAt: Date;
}

export interface MemoryInsight {
  type: 'pattern' | 'trend' | 'preference' | 'relationship';
  title: string;
  description: string;
  confidence: number;
  relatedMemories: string[];
  metadata?: Record<string, any>;
}

export interface KnowledgeGraph {
  nodes: KnowledgeNode[];
  edges: KnowledgeEdge[];
  metadata: {
    generatedAt: Date;
    nodeCount: number;
    edgeCount: number;
  };
}

export interface KnowledgeNode {
  id: string;
  type: 'person' | 'concept' | 'event' | 'preference' | 'fact';
  label: string;
  properties: Record<string, any>;
  memoryIds: string[];
}

export interface KnowledgeEdge {
  id: string;
  sourceId: string;
  targetId: string;
  relationship: string;
  strength: number;
  metadata?: Record<string, any>;
}
