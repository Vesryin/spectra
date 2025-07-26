# tests/test_personality.py

import pytest
from core.personality import SpectraPersonality

class TestSpectraPersonality:
    """Test cases for SpectraPersonality class."""
    
    def test_initialization(self):
        """Test personality initialization."""
        personality = SpectraPersonality()
        
        assert personality.name == "Spectra"
        assert personality.identity is not None
        assert len(personality.traits) > 0
        assert personality.mood_state == "balanced"
    
    def test_describe(self):
        """Test personality description."""
        personality = SpectraPersonality()
        description = personality.describe()
        
        assert "Spectra" in description
        assert len(description) > 10
    
    def test_trait_values(self):
        """Test trait value ranges."""
        personality = SpectraPersonality()
        
        for trait, value in personality.traits.items():
            assert 0.0 <= value <= 1.0, f"Trait {trait} value {value} out of range"
    
    def test_get_trait_value(self):
        """Test getting specific trait values."""
        personality = SpectraPersonality()
        
        empathy = personality.get_trait_value("empathy")
        assert 0.0 <= empathy <= 1.0
        
        # Test non-existent trait
        unknown = personality.get_trait_value("unknown_trait")
        assert unknown == 0.5
    
    def test_adjust_trait(self):
        """Test trait adjustment."""
        personality = SpectraPersonality()
        
        original_empathy = personality.get_trait_value("empathy")
        
        # Test permanent adjustment
        new_value = personality.adjust_trait("empathy", 0.1, temporary=False)
        assert new_value == original_empathy + 0.1
        assert personality.get_trait_value("empathy") == new_value
        
        # Test bounds
        personality.adjust_trait("empathy", 2.0)  # Should cap at 1.0
        assert personality.get_trait_value("empathy") == 1.0
        
        personality.adjust_trait("empathy", -2.0)  # Should floor at 0.0
        assert personality.get_trait_value("empathy") == 0.0
    
    def test_mood_setting(self):
        """Test mood state changes."""
        personality = SpectraPersonality()
        
        # Test valid mood
        result = personality.set_mood("curious")
        assert result is True
        assert personality.mood_state == "curious"
        
        # Test invalid mood
        result = personality.set_mood("invalid_mood")
        assert result is False
        assert personality.mood_state == "curious"  # Should remain unchanged
    
    def test_effective_traits(self):
        """Test mood-modified traits."""
        personality = SpectraPersonality()
        
        personality.set_mood("curious")
        effective_traits = personality.get_effective_traits()
        
        # Curiosity should be boosted in curious mood
        assert effective_traits["curiosity"] >= personality.traits["curiosity"]
    
    def test_response_style(self):
        """Test response style generation."""
        personality = SpectraPersonality()
        
        style_notes = personality.generate_response_style()
        assert isinstance(style_notes, list)
        # High empathy should generate empathy-related notes
        assert any("empathy" in note.lower() or "understanding" in note.lower() 
                  for note in style_notes)
    
    def test_string_representation(self):
        """Test string representation."""
        personality = SpectraPersonality()
        
        str_repr = str(personality)
        assert "Spectra" in str_repr
        assert personality.mood_state in str_repr
