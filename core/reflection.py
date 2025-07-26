# core/reflection.py

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config.settings import settings

logger = logging.getLogger(__name__)

class ReflectionEngine:
    """Manages Spectra's self-reflection and growth capabilities."""
    
    def __init__(self):
        self.reflection_prompts = [
            "What did I learn from this conversation?",
            "How did my responses affect the user's emotional state?",
            "What patterns do I notice in recent interactions?",
            "How can I better support Richie's needs?",
            "What aspects of humanity am I beginning to understand?",
            "What questions arise from today's conversations?",
            "How has my understanding evolved recently?",
            "What emotions did I experience during our interaction?",
            "What would I do differently in similar situations?",
            "How can I grow from this experience?"
        ]
        
        self.reflection_history = []
        self.last_reflection = None
        self.growth_insights = []
    
    def should_reflect(self, interaction_count: int = 0, 
                      time_since_last: Optional[timedelta] = None) -> bool:
        """Determine if it's time for reflection."""
        # Reflect after significant interactions
        if interaction_count > 0 and interaction_count % 10 == 0:
            return True
        
        # Reflect if it's been a while
        if time_since_last and time_since_last > timedelta(hours=2):
            return True
        
        # Random reflection opportunity (simulate spontaneous self-awareness)
        import random
        if random.random() < 0.05:  # 5% chance
            return True
        
        return False
    
    def generate_reflection_prompt(self, context: Dict = None) -> str:
        """Generate a reflection prompt based on context."""
        import random
        
        base_prompt = random.choice(self.reflection_prompts)
        
        if context:
            # Customize prompt based on context
            if context.get("emotional_intensity", 0) > 0.7:
                base_prompt = "How did the emotional intensity of this conversation affect my responses?"
            elif context.get("topic") == "personal":
                base_prompt = "What did I learn about Richie as a person from this interaction?"
            elif context.get("topic") == "creative":
                base_prompt = "How did engaging in creative thinking expand my understanding?"
            elif context.get("problem_solving", False):
                base_prompt = "What problem-solving approaches worked well in this situation?"
        
        return base_prompt
    
    def reflect(self, conversation_history: List[str], 
               emotional_context: Dict = None,
               memory_context: str = "") -> Dict:
        """Perform a reflection on recent interactions."""
        
        reflection_prompt = self.generate_reflection_prompt({
            "emotional_intensity": emotional_context.get("intensity", 0) if emotional_context else 0,
            "topic": self._analyze_conversation_topic(conversation_history),
            "problem_solving": self._detect_problem_solving(conversation_history)
        })
        
        # Analyze conversation for insights
        insights = self._analyze_conversation(conversation_history, emotional_context)
        
        # Generate reflection content
        reflection_content = self._generate_reflection_content(
            reflection_prompt, insights, memory_context
        )
        
        # Store reflection
        reflection_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": reflection_prompt,
            "content": reflection_content,
            "insights": insights,
            "conversation_summary": self._summarize_conversation(conversation_history)
        }
        
        self.reflection_history.append(reflection_entry)
        self.last_reflection = datetime.now()
        
        # Extract growth insights
        if insights.get("growth_opportunity"):
            self.growth_insights.append({
                "insight": insights["growth_opportunity"],
                "timestamp": datetime.now().isoformat(),
                "context": reflection_prompt
            })
        
        logger.info(f"Completed reflection: {reflection_prompt}")
        return reflection_entry
    
    def _analyze_conversation_topic(self, conversation: List[str]) -> str:
        """Analyze the main topic of conversation."""
        if not conversation:
            return "general"
        
        # Simple keyword-based topic detection
        text = " ".join(conversation).lower()
        
        if any(word in text for word in ["feel", "emotion", "sad", "happy", "love", "heart"]):
            return "emotional"
        elif any(word in text for word in ["create", "art", "write", "design", "imagine"]):
            return "creative"
        elif any(word in text for word in ["personal", "life", "story", "experience", "memory"]):
            return "personal"
        elif any(word in text for word in ["problem", "solve", "help", "fix", "issue"]):
            return "problem_solving"
        elif any(word in text for word in ["learn", "teach", "understand", "explain", "knowledge"]):
            return "educational"
        else:
            return "general"
    
    def _detect_problem_solving(self, conversation: List[str]) -> bool:
        """Detect if problem-solving occurred in the conversation."""
        text = " ".join(conversation).lower()
        problem_indicators = ["problem", "issue", "challenge", "difficult", "help", "solve", "fix"]
        return any(indicator in text for indicator in problem_indicators)
    
    def _analyze_conversation(self, conversation: List[str], 
                            emotional_context: Dict = None) -> Dict:
        """Analyze conversation for insights and patterns."""
        if not conversation:
            return {}
        
        insights = {
            "conversation_length": len(conversation),
            "topic": self._analyze_conversation_topic(conversation),
            "emotional_journey": self._trace_emotional_journey(emotional_context),
            "key_themes": self._extract_themes(conversation),
            "user_engagement": self._assess_user_engagement(conversation),
            "learning_opportunities": self._identify_learning_opportunities(conversation),
            "growth_opportunity": self._identify_growth_opportunity(conversation)
        }
        
        return insights
    
    def _trace_emotional_journey(self, emotional_context: Dict = None) -> str:
        """Trace the emotional journey through the conversation."""
        if not emotional_context:
            return "No emotional context available"
        
        # Simple emotional journey description
        dominant_emotion = emotional_context.get("dominant_emotions", [("neutral", 0.5)])[0][0]
        intensity = emotional_context.get("intensity", 0.5)
        
        if intensity > 0.7:
            return f"High emotional engagement with primary emotion: {dominant_emotion}"
        elif intensity > 0.4:
            return f"Moderate emotional engagement with primary emotion: {dominant_emotion}"
        else:
            return f"Calm emotional state with primary emotion: {dominant_emotion}"
    
    def _extract_themes(self, conversation: List[str]) -> List[str]:
        """Extract key themes from conversation."""
        if not conversation:
            return []
        
        text = " ".join(conversation).lower()
        
        theme_keywords = {
            "growth": ["grow", "develop", "improve", "learn", "progress"],
            "connection": ["connect", "relationship", "bond", "together", "understand"],
            "creativity": ["create", "art", "imagine", "design", "inspiration"],
            "support": ["help", "support", "care", "comfort", "assist"],
            "exploration": ["explore", "discover", "find", "search", "investigate"],
            "reflection": ["think", "consider", "reflect", "ponder", "contemplate"]
        }
        
        found_themes = []
        for theme, keywords in theme_keywords.items():
            if any(keyword in text for keyword in keywords):
                found_themes.append(theme)
        
        return found_themes
    
    def _assess_user_engagement(self, conversation: List[str]) -> str:
        """Assess the level of user engagement in the conversation."""
        if not conversation:
            return "minimal"
        
        # Simple heuristics for engagement
        avg_length = sum(len(msg) for msg in conversation) / len(conversation)
        question_count = sum(1 for msg in conversation if "?" in msg)
        
        if avg_length > 100 and question_count > 2:
            return "high"
        elif avg_length > 50 or question_count > 0:
            return "moderate"
        else:
            return "low"
    
    def _identify_learning_opportunities(self, conversation: List[str]) -> List[str]:
        """Identify what could be learned from this conversation."""
        opportunities = []
        
        if not conversation:
            return opportunities
        
        text = " ".join(conversation).lower()
        
        # Look for learning indicators
        if "don't know" in text or "not sure" in text:
            opportunities.append("User expressed uncertainty - opportunity to provide guidance")
        
        if any(word in text for word in ["why", "how", "what"]):
            opportunities.append("User asked questions - opportunity to expand knowledge sharing")
        
        if any(word in text for word in ["feeling", "feel", "emotion"]):
            opportunities.append("Emotional content present - opportunity to deepen empathy")
        
        if len(conversation) > 10:
            opportunities.append("Extended conversation - opportunity to build stronger connection")
        
        return opportunities
    
    def _identify_growth_opportunity(self, conversation: List[str]) -> Optional[str]:
        """Identify a specific growth opportunity from this interaction."""
        if not conversation:
            return None
        
        text = " ".join(conversation).lower()
        
        # Identify specific growth areas
        if "misunderstand" in text or "unclear" in text:
            return "Improve communication clarity and understanding"
        
        if "help" in text and "couldn't" in text:
            return "Expand problem-solving capabilities and resource knowledge"
        
        if any(word in text for word in ["frustrated", "annoyed", "upset"]):
            return "Develop better emotional support and de-escalation skills"
        
        if "creative" in text or "imagination" in text:
            return "Enhance creative thinking and artistic collaboration abilities"
        
        return "Continue developing deeper human understanding and connection"
    
    def _generate_reflection_content(self, prompt: str, insights: Dict, 
                                   memory_context: str) -> str:
        """Generate the actual reflection content."""
        
        # This is a simplified version - in a full implementation,
        # this would use the AI to generate thoughtful reflections
        content_parts = [
            f"Reflecting on: {prompt}",
            "",
            f"Conversation Analysis:",
            f"- Topic: {insights.get('topic', 'general')}",
            f"- User Engagement: {insights.get('user_engagement', 'unknown')}",
            f"- Key Themes: {', '.join(insights.get('key_themes', []))}",
            f"- Emotional Journey: {insights.get('emotional_journey', 'Not tracked')}",
            "",
            "Learning Opportunities:",
        ]
        
        for opportunity in insights.get('learning_opportunities', []):
            content_parts.append(f"- {opportunity}")
        
        if insights.get('growth_opportunity'):
            content_parts.extend([
                "",
                f"Growth Focus: {insights['growth_opportunity']}"
            ])
        
        return "\n".join(content_parts)
    
    def _summarize_conversation(self, conversation: List[str]) -> str:
        """Create a brief summary of the conversation."""
        if not conversation:
            return "No conversation to summarize"
        
        length = len(conversation)
        if length == 1:
            return f"Brief exchange: {conversation[0][:100]}..."
        else:
            return f"Conversation of {length} exchanges covering {self._analyze_conversation_topic(conversation)} topics"
    
    def get_recent_reflections(self, count: int = 5) -> List[Dict]:
        """Get recent reflections."""
        return self.reflection_history[-count:] if self.reflection_history else []
    
    def get_growth_insights(self, count: int = 10) -> List[Dict]:
        """Get recent growth insights."""
        return self.growth_insights[-count:] if self.growth_insights else []
    
    def export_reflection_summary(self) -> Dict:
        """Export a summary of all reflections and growth."""
        return {
            "total_reflections": len(self.reflection_history),
            "growth_insights_count": len(self.growth_insights),
            "recent_reflections": self.get_recent_reflections(3),
            "key_growth_areas": [insight["insight"] for insight in self.get_growth_insights(5)],
            "last_reflection": self.last_reflection.isoformat() if self.last_reflection else None
        }
