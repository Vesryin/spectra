# tests/test_emotions.py

import pytest
from core.emotions import EmotionalState, EmotionEngine

class TestEmotionalState:
    """Test cases for EmotionalState class."""
    
    def test_initialization(self):
        """Test emotional state initialization."""
        state = EmotionalState()
        
        # Check that all emotions are initialized
        assert len(state.emotions) > 0
        assert "joy" in state.emotions
        assert "empathy" in state.emotions
        assert "curiosity" in state.emotions
        
        # Check value ranges
        for emotion, value in state.emotions.items():
            assert 0.0 <= value <= 1.0
    
    def test_update_emotion(self):
        """Test updating emotions."""
        state = EmotionalState()
        original_joy = state.emotions["joy"]
        
        # Update emotion
        result = state.update_emotion("joy", 0.2, "test reason")
        assert result is True
        assert state.emotions["joy"] > original_joy
        
        # Test bounds
        state.update_emotion("joy", 2.0)  # Should cap at 1.0
        assert state.emotions["joy"] <= 1.0
        
        state.update_emotion("joy", -2.0)  # Should floor at 0.0
        assert state.emotions["joy"] >= 0.0
    
    def test_update_invalid_emotion(self):
        """Test updating non-existent emotion."""
        state = EmotionalState()
        result = state.update_emotion("nonexistent", 0.1)
        assert result is False
    
    def test_get_dominant_emotions(self):
        """Test getting dominant emotions."""
        state = EmotionalState()
        
        # Set specific emotion high
        state.emotions["joy"] = 0.95
        state.emotions["excitement"] = 0.85
        
        dominant = state.get_dominant_emotions(2)
        assert len(dominant) == 2
        assert dominant[0][0] == "joy"  # Should be highest
        assert dominant[1][0] == "excitement"  # Should be second
    
    def test_get_emotional_tone(self):
        """Test emotional tone detection."""
        state = EmotionalState()
        
        # Test joyful tone
        state.emotions["joy"] = 0.9
        assert state.get_emotional_tone() == "joyful"
        
        # Test curious tone
        state.emotions["joy"] = 0.5
        state.emotions["curiosity"] = 0.9
        assert state.get_emotional_tone() == "curious"
    
    def test_decay_emotions(self):
        """Test emotional decay."""
        state = EmotionalState()
        
        # Set emotion very high
        state.emotions["excitement"] = 1.0
        original_excitement = state.emotions["excitement"]
        
        # Apply decay
        state.decay_emotions(0.1)
        
        # Should move toward baseline
        assert state.emotions["excitement"] < original_excitement

class TestEmotionEngine:
    """Test cases for EmotionEngine class."""
    
    def test_initialization(self):
        """Test emotion engine initialization."""
        engine = EmotionEngine()
        
        assert engine.state is not None
        assert len(engine.emotion_triggers) > 0
    
    def test_process_positive_input(self):
        """Test processing positive emotional input."""
        engine = EmotionEngine()
        original_joy = engine.state.emotions["joy"]
        
        result = engine.process_input("I'm so grateful and happy!")
        
        # Should increase positive emotions
        assert engine.state.emotions["joy"] > original_joy
        assert result["emotional_response"] is not None
        assert result["tone"] is not None
    
    def test_process_sad_input(self):
        """Test processing sad emotional input."""
        engine = EmotionEngine()
        original_empathy = engine.state.emotions["empathy"]
        
        result = engine.process_input("I'm feeling really sad today")
        
        # Should increase empathy and concern
        assert engine.state.emotions["empathy"] >= original_empathy
        assert "empathy" in result["emotional_response"] or "concern" in result["emotional_response"]
    
    def test_process_curious_input(self):
        """Test processing curious input."""
        engine = EmotionEngine()
        original_curiosity = engine.state.emotions["curiosity"]
        
        result = engine.process_input("I wonder how this works? What do you think?")
        
        # Should increase curiosity
        assert engine.state.emotions["curiosity"] >= original_curiosity
    
    def test_emotional_modifier(self):
        """Test getting emotional modifiers for AI responses."""
        engine = EmotionEngine()
        
        # Set engine to joyful state
        engine.state.emotions["joy"] = 0.9
        
        modifier = engine.get_emotional_modifier()
        assert isinstance(modifier, str)
        assert len(modifier) > 0
    
    def test_state_summary(self):
        """Test getting state summary."""
        engine = EmotionEngine()
        
        summary = engine.get_state_summary()
        
        assert "dominant_emotions" in summary
        assert "emotional_tone" in summary
        assert "intensity" in summary
        assert "stability" in summary
