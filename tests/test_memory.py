# tests/test_memory.py

import pytest
import tempfile
from pathlib import Path
from core.memory import SpectraMemory, MemoryEntry

class TestMemoryEntry:
    """Test cases for MemoryEntry class."""
    
    def test_memory_entry_creation(self):
        """Test creating a memory entry."""
        entry = MemoryEntry("Test content", "conversation", 0.8, ["test"])
        
        assert entry.content == "Test content"
        assert entry.memory_type == "conversation"
        assert entry.importance == 0.8
        assert "test" in entry.tags
        assert entry.access_count == 0
    
    def test_memory_entry_serialization(self):
        """Test converting memory entry to/from dict."""
        entry = MemoryEntry("Test content", "reflection", 0.9, ["important"])
        
        # Test to_dict
        data = entry.to_dict()
        assert data["content"] == "Test content"
        assert data["memory_type"] == "reflection"
        assert data["importance"] == 0.9
        assert "important" in data["tags"]
        
        # Test from_dict
        new_entry = MemoryEntry.from_dict(data)
        assert new_entry.content == entry.content
        assert new_entry.memory_type == entry.memory_type

class TestSpectraMemory:
    """Test cases for SpectraMemory class."""
    
    def setup_method(self):
        """Set up test with temporary memory file."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.memory_file = self.temp_dir / "test_memory.json"
        self.memory = SpectraMemory(self.memory_file)
    
    def test_initialization_new_file(self):
        """Test initializing with a new memory file."""
        assert self.memory.memories == []
        assert self.memory.memory_path == self.memory_file
    
    def test_remember_and_recall(self):
        """Test basic remember and recall functionality."""
        # Remember something
        self.memory.remember("Test memory")
        
        # Recall all memories
        memories = self.memory.recall()
        assert len(memories) == 1
        assert "Test memory" in memories[0]
    
    def test_remember_with_metadata(self):
        """Test remembering with metadata."""
        self.memory.remember("Important memory", "reflection", 0.9, ["important"])
        
        # Check that it was stored correctly
        assert len(self.memory.memories) == 1
        memory_entry = self.memory.memories[0]
        assert memory_entry.content == "Important memory"
        assert memory_entry.memory_type == "reflection"
        assert memory_entry.importance == 0.9
        assert "important" in memory_entry.tags
    
    def test_recall_with_keyword(self):
        """Test recalling memories with keyword filter."""
        self.memory.remember("I love programming")
        self.memory.remember("I enjoy reading books")
        self.memory.remember("Programming is fun")
        
        # Recall memories with keyword
        programming_memories = self.memory.recall(keyword="programming")
        assert len(programming_memories) == 2
    
    def test_recall_with_type_filter(self):
        """Test recalling memories with type filter."""
        self.memory.remember("Normal conversation", "conversation")
        self.memory.remember("Important reflection", "reflection")
        self.memory.remember("Another conversation", "conversation")
        
        # Recall only conversations
        conversations = self.memory.recall(memory_type="conversation")
        assert len(conversations) == 2
        
        # Recall only reflections
        reflections = self.memory.recall(memory_type="reflection")
        assert len(reflections) == 1
    
    def test_recall_with_importance_filter(self):
        """Test recalling memories with importance filter."""
        self.memory.remember("Low importance", "conversation", 0.3)
        self.memory.remember("High importance", "conversation", 0.9)
        self.memory.remember("Medium importance", "conversation", 0.6)
        
        # Recall only high importance memories
        important_memories = self.memory.recall(min_importance=0.8)
        assert len(important_memories) == 1
        assert "High importance" in important_memories[0]
    
    def test_recall_with_limit(self):
        """Test recalling with limit."""
        for i in range(10):
            self.memory.remember(f"Memory {i}")
        
        # Recall with limit
        limited_memories = self.memory.recall(limit=5)
        assert len(limited_memories) == 5
    
    def test_get_recent_context(self):
        """Test getting recent conversation context."""
        for i in range(10):
            self.memory.remember(f"Conversation {i}", "conversation")
        
        context = self.memory.get_recent_context(limit=3)
        assert len(context.split('\n')) <= 3
    
    def test_add_reflection(self):
        """Test adding reflection memories."""
        self.memory.add_reflection("This was a meaningful conversation")
        
        reflections = self.memory.recall(memory_type="reflection")
        assert len(reflections) == 1
        assert "meaningful conversation" in reflections[0]
    
    def test_search_memories(self):
        """Test searching memories with detailed results."""
        self.memory.remember("I love artificial intelligence", "conversation", 0.8)
        self.memory.remember("AI is fascinating", "reflection", 0.9)
        
        results = self.memory.search_memories("artificial")
        assert len(results) == 1
        assert results[0]["content"] == "I love artificial intelligence"
        assert results[0]["importance"] == 0.8
    
    def test_memory_persistence(self):
        """Test that memories persist across instances."""
        # Add memory to first instance
        self.memory.remember("Persistent memory")
        
        # Create new instance with same file
        new_memory = SpectraMemory(self.memory_file)
        
        # Check memory persisted
        memories = new_memory.recall()
        assert len(memories) == 1
        assert "Persistent memory" in memories[0]
    
    def test_memory_stats(self):
        """Test memory statistics."""
        # Empty stats
        stats = self.memory.get_stats()
        assert stats["total"] == 0
        
        # Add some memories
        self.memory.remember("Conversation 1", "conversation", 0.5)
        self.memory.remember("Reflection 1", "reflection", 0.8)
        
        stats = self.memory.get_stats()
        assert stats["total"] == 2
        assert "conversation" in stats["by_type"]
        assert "reflection" in stats["by_type"]
        assert stats["by_type"]["conversation"] == 1
        assert stats["by_type"]["reflection"] == 1
    
    def teardown_method(self):
        """Clean up test files."""
        if self.memory_file.exists():
            self.memory_file.unlink()
        self.temp_dir.rmdir()
