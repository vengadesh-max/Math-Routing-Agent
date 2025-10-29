import re
from typing import Dict, List, Optional, Tuple
from pydantic import BaseModel, validator
from config import settings

class InputValidationResult(BaseModel):
    is_valid: bool
    sanitized_input: str
    confidence_score: float
    detected_topic: str
    warnings: List[str]

class InputGuardrails:
    """AI Gateway Input Guardrails for Math Routing Agent"""
    
    def __init__(self):
        self.allowed_topics = settings.allowed_topics
        self.max_length = settings.max_input_length
        self.math_patterns = [
            r'\b(solve|calculate|find|compute|evaluate|integrate|differentiate|derive)\b',
            r'\b(equation|formula|function|matrix|vector|limit|derivative|integral)\b',
            r'\b(algebra|calculus|geometry|trigonometry|statistics|probability)\b',
            r'[+\-*/=<>(){}[\]^]',  # Math operators
            r'\d+',  # Numbers
            r'\b(x|y|z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w)\b',  # Variables
        ]
        
        self.potentially_harmful_patterns = [
            r'\b(hack|exploit|bypass|cheat|illegal|harmful|dangerous)\b',
            r'<script.*?>.*?</script>',  # Script injection
            r'javascript:',  # JavaScript injection
            r'data:text/html',  # Data URI injection
        ]
    
    def validate_input(self, user_input: str) -> InputValidationResult:
        """Validate and sanitize user input"""
        warnings = []
        confidence_score = 0.0
        detected_topic = "general"
        
        # Length validation
        if len(user_input) > self.max_length:
            return InputValidationResult(
                is_valid=False,
                sanitized_input="",
                confidence_score=0.0,
                detected_topic="",
                warnings=[f"Input too long. Maximum {self.max_length} characters allowed."]
            )
        
        # Check for potentially harmful content
        for pattern in self.potentially_harmful_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return InputValidationResult(
                    is_valid=False,
                    sanitized_input="",
                    confidence_score=0.0,
                    detected_topic="",
                    warnings=["Potentially harmful content detected."]
                )
        
        # Sanitize input
        sanitized_input = self._sanitize_input(user_input)
        
        # Detect mathematical content
        math_score = self._calculate_math_score(sanitized_input)
        if math_score > 0.3:
            confidence_score = math_score
            detected_topic = self._detect_math_topic(sanitized_input)
        else:
            warnings.append("Input may not be mathematical in nature.")
            confidence_score = 0.1
        
        # Check if topic is allowed
        if detected_topic not in self.allowed_topics and detected_topic != "general":
            warnings.append(f"Topic '{detected_topic}' may not be supported.")
        
        return InputValidationResult(
            is_valid=True,
            sanitized_input=sanitized_input,
            confidence_score=confidence_score,
            detected_topic=detected_topic,
            warnings=warnings
        )
    
    def _sanitize_input(self, input_text: str) -> str:
        """Sanitize input text"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', input_text)
        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        return sanitized
    
    def _calculate_math_score(self, text: str) -> float:
        """Calculate confidence score for mathematical content"""
        score = 0.0
        total_patterns = len(self.math_patterns)
        
        for pattern in self.math_patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                score += min(matches / 10, 1.0)  # Normalize to 0-1
        
        return min(score / total_patterns, 1.0)
    
    def _detect_math_topic(self, text: str) -> str:
        """Detect specific mathematical topic"""
        text_lower = text.lower()
        
        topic_keywords = {
            "algebra": ["equation", "variable", "solve", "factor", "polynomial"],
            "calculus": ["derivative", "integral", "limit", "differentiate", "integrate"],
            "geometry": ["triangle", "circle", "angle", "area", "perimeter", "volume"],
            "trigonometry": ["sin", "cos", "tan", "angle", "trigonometric"],
            "statistics": ["mean", "median", "mode", "probability", "distribution"],
            "linear_algebra": ["matrix", "vector", "determinant", "eigenvalue"]
        }
        
        topic_scores = {}
        for topic, keywords in topic_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores, key=topic_scores.get)
        
        return "general"

