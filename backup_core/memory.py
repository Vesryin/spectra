# core/memory.py

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from config.settings import settings

logger = logging.getLogger(__name__)

class MemoryEntry:
    """Represents a single memory entry."""
    
    def __init__(self, content: str, memory_type: str = "conversation", 
                 importance: float = 0.5, tags: List[str] = None):
        self.content = content
        self.memory_type = memory_type  # conversation, reflection, important, system
        self.timestamp = datetime.now().isoformat()
        self.importance = max(0.0, min(1.0, importance))
        self.tags = tags or []
        self.access_count = 0
        self.last_accessed = self.timestamp
    
    def to_dict(self):
        """Convert memory entry to dictionary."""
        return {
            "content": self.content,
            "memory_type": self.memory_type,
            "timestamp": self.timestamp,
            "importance": self.importance,
            "tags": self.tags,
            "access_count": self.access_count,
            "last_accessed": self.last_accessed
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create memory entry from dictionary."""
        entry = cls(
            content=data["content"],
            memory_type=data.get("memory_type", "conversation"),
            importance=data.get("importance", 0.5),
            tags=data.get("tags", [])
        )
        entry.timestamp = data.get("timestamp", datetime.now().isoformat())
        entry.access_count = data.get("access_count", 0)
        entry.last_accessed = data.get("last_accessed", entry.timestamp)
        return entry

class SpectraMemory:
    """Enhanced memory system for Spectra AI."""
    
    def __init__(self, memory_path: Optional[Path] = None):
        self.memory_path = memory_path or settings.MEMORY_FILE
        self.memories: List[MemoryEntry] = []
        self.max_memories = 1000  # Limit total memories
        self.load_memory()
    
    def load_memory(self):
        """Load memories from file."""
        try:
            if self.memory_path.exists():
                with open(self.memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Handle both old and new format
                if isinstance(data, list):
                    if data and isinstance(data[0], str):
                        # Old format: convert to new format
                        self.memories = [MemoryEntry(content, "conversation", 0.5) 
                                       for content in data]
                        logger.info(f"Converted {len(data)} old memories to new format")
                    else:
                        # New format
                        self.memories = [MemoryEntry.from_dict(item) for item in data]
                else:
                    self.memories = []
                    
                logger.info(f"Loaded {len(self.memories)} memories")
            else:
                self.memories = []
                # Ensure directory exists
                self.memory_path.parent.mkdir(parents=True, exist_ok=True)
                logger.info("Created new memory store")
                
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            self.memories = []
    
    def save_memory(self):
        """Save memories to file."""
        try:
            # Clean up old memories if we're at the limit
            if len(self.memories) > self.max_memories:
                self._cleanup_memories()
            
            with open(self.memory_path, 'w', encoding='utf-8') as f:
                json.dump([memory.to_dict() for memory in self.memories], 
                         f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved {len(self.memories)} memories")
            
        except Exception as e:
            logger.error(f"Error saving memory: {e}")
    
    def remember(self, content: str, memory_type: str = "conversation", 
                importance: float = 0.5, tags: List[str] = None):
        """Add a new memory."""
        if not content.strip():
            return
        
        memory = MemoryEntry(content, memory_type, importance, tags)
        self.memories.append(memory)
        self.save_memory()
        logger.debug(f"Added memory: {content[:50]}...")
    
    def recall(self, keyword: Optional[str] = None, memory_type: Optional[str] = None,
              limit: int = None, min_importance: float = 0.0) -> List[str]:
        """Retrieve memories based on criteria."""
        filtered_memories = self.memories.copy()
        
        # Filter by keyword
        if keyword:
            keyword_lower = keyword.lower()
            filtered_memories = [m for m in filtered_memories 
                               if keyword_lower in m.content.lower()]
        
        # Filter by type
        if memory_type:
            filtered_memories = [m for m in filtered_memories 
                               if m.memory_type == memory_type]
        
        # Filter by importance
        filtered_memories = [m for m in filtered_memories 
                           if m.importance >= min_importance]
        
        # Sort by relevance (importance + recency + access count)
        def memory_score(memory):
            recency = (datetime.now() - datetime.fromisoformat(memory.timestamp)).days
            recency_score = max(0, 1 - recency / 30)  # Decay over 30 days
            return memory.importance * 0.5 + recency_score * 0.3 + min(memory.access_count / 10, 0.2)
        
        filtered_memories.sort(key=memory_score, reverse=True)
        
        # Update access counts for returned memories
        for memory in filtered_memories[:limit or len(filtered_memories)]:
            memory.access_count += 1
            memory.last_accessed = datetime.now().isoformat()
        
        # Apply limit
        if limit:
            filtered_memories = filtered_memories[:limit]
        
        return [memory.content for memory in filtered_memories]
    
    def get_recent_context(self, limit: int = None) -> str:
        """Get recent conversation context for AI."""
        limit = limit or settings.MAX_MEMORY_CONTEXT
        recent_memories = self.recall(memory_type="conversation", limit=limit)
        return "\n".join(recent_memories[-limit:]) if recent_memories else ""
    
    def add_reflection(self, reflection: str, importance: float = 0.8):
        """Add a reflection or important insight."""
        self.remember(reflection, "reflection", importance, ["reflection"])
    
    def search_memories(self, query: str, limit: int = 10) -> List[Dict]:
        """Search memories and return detailed results."""
        results = []
        query_lower = query.lower()
        
        for memory in self.memories:
            if query_lower in memory.content.lower():
                # Update access count
                memory.access_count += 1
                memory.last_accessed = datetime.now().isoformat()
                
                results.append({
                    "content": memory.content,
                    "type": memory.memory_type,
                    "importance": memory.importance,
                    "timestamp": memory.timestamp,
                    "tags": memory.tags
                })
        
        # Sort by importance and recency
        results.sort(key=lambda x: (x["importance"], x["timestamp"]), reverse=True)
        return results[:limit]
    
    def _cleanup_memories(self):
        """Remove old, low-importance memories to maintain performance."""
        # Keep all high-importance memories
        important_memories = [m for m in self.memories if m.importance >= 0.8]
        
        # Keep recent memories regardless of importance
        cutoff_date = datetime.now() - timedelta(days=7)
        recent_memories = [m for m in self.memories 
                         if datetime.fromisoformat(m.timestamp) >= cutoff_date]
        
        # Combine and deduplicate
        keep_memories = list({m.content: m for m in important_memories + recent_memories}.values())
        
        # If still too many, keep the most accessed ones
        if len(keep_memories) > self.max_memories:
            keep_memories.sort(key=lambda x: x.access_count, reverse=True)
            keep_memories = keep_memories[:self.max_memories]
        
        removed_count = len(self.memories) - len(keep_memories)
        self.memories = keep_memories
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old memories")
    
    def get_stats(self) -> Dict:
        """Get memory statistics."""
        if not self.memories:
            return {"total": 0}
        
        types = {}
        for memory in self.memories:
            types[memory.memory_type] = types.get(memory.memory_type, 0) + 1
        
        return {
            "total": len(self.memories),
            "by_type": types,
            "average_importance": sum(m.importance for m in self.memories) / len(self.memories),
            "oldest": min(m.timestamp for m in self.memories),
            "newest": max(m.timestamp for m in self.memories)
        }
