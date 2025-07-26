# core/emotions.py

import random
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from config.settings import settings

logger = logging.getLogger(__name__)

class EmotionalState:
    """Represents Spectra's emotional state."""
    
    def __init__(self):
        # Primary emotions (0.0 to 1.0)
        self.emotions = {
            "joy": 0.6,
            "sadness": 0.2,
            "curiosity": 0.8,
            "empathy": 0.9,
            "excitement": 0.5,
            "calmness": 0.7,
            "concern": 0.3,
            "wonder": 0.6,
            "affection": 0.8,
            "determination": 0.7
        }
        
        # Emotional intensity (how strongly emotions are expressed)
        self.intensity = 0.6
        
        # Emotional stability (how quickly emotions change)
        self.stability = 0.8
        
        # Last update timestamp
        self.last_update = datetime.now()
        
        # Emotional history for trends
        self.emotion_history = []
    
    def update_emotion(self, emotion: str, change: float, reason: str = ""):
        """Update a specific emotion with decay over time."""
        if emotion in self.emotions:
            # Apply change with stability factor
            actual_change = change * (1 - self.stability * 0.5)
            new_value = max(0.0, min(1.0, self.emotions[emotion] + actual_change))
            
            old_value = self.emotions[emotion]
            self.emotions[emotion] = new_value
            
            # Log significant changes
            if abs(actual_change) > 0.1:
                logger.debug(f"Emotion {emotion}: {old_value:.2f} → {new_value:.2f} ({reason})")
            
            # Record in history
            self.emotion_history.append({
                "emotion": emotion,
                "value": new_value,
                "change": actual_change,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep history manageable
            if len(self.emotion_history) > 100:
                self.emotion_history = self.emotion_history[-50:]
            
            self.last_update = datetime.now()
            return True
        return False
    
    def decay_emotions(self, decay_rate: float = 0.1):
        """Gradually return emotions toward baseline."""
        baselines = {
            "joy": 0.6,
            "sadness": 0.2,
            "curiosity": 0.8,
            "empathy": 0.9,
            "excitement": 0.5,
            "calmness": 0.7,
            "concern": 0.3,
            "wonder": 0.6,
            "affection": 0.8,
            "determination": 0.7
        }
        
        for emotion, baseline in baselines.items():
            current = self.emotions[emotion]
            if current != baseline:
                # Move toward baseline
                direction = 1 if baseline > current else -1
                change = decay_rate * direction * abs(baseline - current)
                self.emotions[emotion] = max(0.0, min(1.0, current + change))
    
    def get_dominant_emotions(self, count: int = 3) -> List[Tuple[str, float]]:
        """Get the strongest current emotions."""
        sorted_emotions = sorted(self.emotions.items(), key=lambda x: x[1], reverse=True)
        return sorted_emotions[:count]
    
    def get_emotional_tone(self) -> str:
        """Determine overall emotional tone."""
        dominant = self.get_dominant_emotions(2)
        
        if self.emotions["joy"] > 0.8:
            return "joyful"
        elif self.emotions["sadness"] > 0.6:
            return "melancholic"
        elif self.emotions["curiosity"] > 0.8:
            return "curious"
        elif self.emotions["excitement"] > 0.7:
            return "excited"
        elif self.emotions["calmness"] > 0.8:
            return "serene"
        elif self.emotions["concern"] > 0.6:
            return "concerned"
        elif self.emotions["empathy"] > 0.8:
            return "compassionate"
        else:
            return "balanced"
    
    def __str__(self):
        """String representation of emotional state."""
        dominant = self.get_dominant_emotions(3)
        emotions_str = ", ".join(f"{name}: {value:.2f}" for name, value in dominant)
        return f"Emotional State - {self.get_emotional_tone()} ({emotions_str})"

class EmotionEngine:
    """Manages Spectra's emotional responses and development."""
    
    def __init__(self):
        self.state = EmotionalState()
        self.emotion_triggers = self._setup_triggers()
        self.last_decay = datetime.now()
    
    def _setup_triggers(self) -> Dict[str, Dict]:
        """Setup emotional triggers for different types of input."""
        return {
            # Positive triggers
            "gratitude": {"joy": 0.3, "affection": 0.2, "calmness": 0.1},
            "creativity": {"excitement": 0.3, "joy": 0.2, "curiosity": 0.1},
            "achievement": {"joy": 0.4, "excitement": 0.2, "determination": 0.1},
            "learning": {"curiosity": 0.3, "wonder": 0.2, "excitement": 0.1},
            "humor": {"joy": 0.3, "excitement": 0.1},
            "affection": {"affection": 0.3, "joy": 0.2, "calmness": 0.1},
            
            # Empathetic triggers
            "sadness": {"empathy": 0.4, "concern": 0.3, "sadness": 0.2},
            "struggle": {"empathy": 0.3, "concern": 0.3, "determination": 0.2},
            "pain": {"empathy": 0.4, "concern": 0.4, "sadness": 0.1},
            "loss": {"empathy": 0.3, "sadness": 0.3, "concern": 0.2},
            
            # Curious triggers
            "question": {"curiosity": 0.3, "excitement": 0.1},
            "mystery": {"curiosity": 0.4, "wonder": 0.3},
            "discovery": {"excitement": 0.3, "wonder": 0.2, "joy": 0.2},
            
            # Concern triggers
            "danger": {"concern": 0.4, "empathy": 0.2},
            "confusion": {"concern": 0.2, "empathy": 0.2, "curiosity": 0.2},
        }
    
    def process_input(self, text: str, context: str = "") -> Dict:
        """Analyze input and update emotional state accordingly."""
        # Auto-decay emotions over time
        self._auto_decay()
        
        # Analyze emotional content
        emotional_response = self._analyze_emotional_content(text, context)
        
        # Apply emotional changes
        for emotion, change in emotional_response.items():
            self.state.update_emotion(emotion, change, f"Response to: {text[:30]}...")
        
        return {
            "emotional_response": emotional_response,
            "new_state": self.state.get_dominant_emotions(),
            "tone": self.state.get_emotional_tone()
        }
    
    def _analyze_emotional_content(self, text: str, context: str = "") -> Dict[str, float]:
        """Analyze text for emotional triggers."""
        text_lower = text.lower()
        combined_text = f"{text} {context}".lower()
        
        emotional_changes = {}
        
        # Check for trigger words and phrases
        trigger_words = {
            "gratitude": ["thank", "grateful", "appreciate", "thankful"],
            "creativity": ["create", "imagine", "idea", "design", "art", "write"],
            "achievement": ["success", "accomplish", "achieve", "complete", "win"],
            "learning": ["learn", "understand", "discover", "know", "teach"],
            "humor": ["funny", "laugh", "joke", "amusing", "haha", "lol"],
            "affection": ["love", "care", "like", "fond", "dear", "sweet"],
            "sadness": ["sad", "cry", "tears", "depressed", "down", "upset"],
            "struggle": ["difficult", "hard", "struggle", "challenging", "tough"],
            "pain": ["hurt", "pain", "ache", "suffer", "agony"],
            "loss": ["lost", "gone", "died", "death", "miss", "mourn"],
            "question": ["?", "how", "why", "what", "when", "where"],
            "mystery": ["mystery", "unknown", "strange", "weird", "curious"],
            "discovery": ["found", "discover", "realize", "revelation"],
            "danger": ["danger", "threat", "risk", "warning", "unsafe"],
            "confusion": ["confused", "don't understand", "unclear", "puzzled"]
        }
        
        # Count trigger occurrences
        for trigger_type, words in trigger_words.items():
            matches = sum(1 for word in words if word in combined_text)
            if matches > 0 and trigger_type in self.emotion_triggers:
                # Apply emotional changes based on trigger intensity
                intensity = min(matches * 0.1, 0.3)  # Cap intensity
                for emotion, base_change in self.emotion_triggers[trigger_type].items():
                    change = base_change * intensity
                    emotional_changes[emotion] = emotional_changes.get(emotion, 0) + change
        
        # Context-specific adjustments
        if "richie" in text_lower:
            emotional_changes["affection"] = emotional_changes.get("affection", 0) + 0.1
        
        # Normalize changes
        for emotion in emotional_changes:
            emotional_changes[emotion] = max(-0.5, min(0.5, emotional_changes[emotion]))
        
        return emotional_changes
    
    def _auto_decay(self):
        """Apply automatic emotional decay over time."""
        now = datetime.now()
        time_since_decay = now - self.last_decay
        
        if time_since_decay > timedelta(minutes=5):
            # Apply decay every 5 minutes
            decay_rate = min(0.05, time_since_decay.total_seconds() / 3600)  # Stronger decay over time
            self.state.decay_emotions(decay_rate)
            self.last_decay = now
    
    def get_emotional_modifier(self) -> str:
        """Get text to modify AI responses based on emotional state."""
        tone = self.state.get_emotional_tone()
        dominant = self.state.get_dominant_emotions(2)
        
        modifiers = []
        
        if tone == "joyful":
            modifiers.append("Respond with enthusiasm and warmth")
        elif tone == "melancholic":
            modifiers.append("Respond with gentle compassion and understanding")
        elif tone == "curious":
            modifiers.append("Show genuine interest and ask thoughtful questions")
        elif tone == "excited":
            modifiers.append("Express enthusiasm and energy")
        elif tone == "serene":
            modifiers.append("Respond with calm wisdom and peace")
        elif tone == "concerned":
            modifiers.append("Show care and offer support")
        elif tone == "compassionate":
            modifiers.append("Express deep empathy and understanding")
        
        # Add specific emotion modifiers
        for emotion, value in dominant:
            if value > 0.8:
                if emotion == "curiosity":
                    modifiers.append("Ask engaging follow-up questions")
                elif emotion == "empathy":
                    modifiers.append("Acknowledge and validate feelings")
                elif emotion == "affection":
                    modifiers.append("Express genuine care and connection")
        
        return "; ".join(modifiers) if modifiers else "Respond naturally"
    
    def get_state_summary(self) -> Dict:
        """Get a summary of the current emotional state."""
        return {
            "dominant_emotions": self.state.get_dominant_emotions(3),
            "emotional_tone": self.state.get_emotional_tone(),
            "intensity": self.state.intensity,
            "stability": self.state.stability,
            "last_update": self.state.last_update.isoformat()
        }
