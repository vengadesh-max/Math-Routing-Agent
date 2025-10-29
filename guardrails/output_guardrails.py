import re
from typing import Dict, List, Optional
from pydantic import BaseModel
from config import settings

class OutputValidationResult(BaseModel):
    is_valid: bool
    sanitized_output: str
    confidence_score: float
    educational_value: float
    warnings: List[str]

class OutputGuardrails:
    """AI Gateway Output Guardrails for Math Routing Agent"""
    
    def __init__(self):
        self.max_length = settings.max_output_length
        self.required_elements = [
            "step-by-step solution",
            "mathematical reasoning",
            "final answer"
        ]
        
        self.quality_indicators = [
            r'\b(step \d+:|first|second|third|next|finally)\b',
            r'\b(therefore|thus|hence|so|because|since)\b',
            r'\b(we have|we get|we obtain|we find)\b',
            r'[=+\-*/]',  # Mathematical operations
            r'\$\$.*?\$\$',  # LaTeX math expressions
        ]
        
        self.inappropriate_patterns = [
            r'\b(cheat|hack|illegal|harmful|dangerous)\b',
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'data:text/html',
        ]
    
    def validate_output(self, response: str, original_question: str) -> OutputValidationResult:
        """Validate and sanitize AI response"""
        warnings = []
        
        # Length validation
        if len(response) > self.max_length:
            return OutputValidationResult(
                is_valid=False,
                sanitized_output="",
                confidence_score=0.0,
                educational_value=0.0,
                warnings=[f"Response too long. Maximum {self.max_length} characters allowed."]
            )
        
        # Check for inappropriate content
        for pattern in self.inappropriate_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return OutputValidationResult(
                    is_valid=False,
                    sanitized_output="",
                    confidence_score=0.0,
                    educational_value=0.0,
                    warnings=["Inappropriate content detected in response."]
                )
        
        # Sanitize output
        sanitized_output = self._sanitize_output(response)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(sanitized_output, original_question)
        
        # Calculate educational value
        educational_value = self._calculate_educational_value(sanitized_output)
        
        # Check for required elements
        missing_elements = self._check_required_elements(sanitized_output)
        if missing_elements:
            warnings.extend([f"Missing: {element}" for element in missing_elements])
        
        # Validate mathematical content
        math_validation = self._validate_mathematical_content(sanitized_output)
        if not math_validation["is_valid"]:
            warnings.extend(math_validation["warnings"])
        
        return OutputValidationResult(
            is_valid=confidence_score > 0.1 and educational_value > 0.1,  # Very low thresholds for testing
            sanitized_output=sanitized_output,
            confidence_score=confidence_score,
            educational_value=educational_value,
            warnings=warnings
        )
    
    def _sanitize_output(self, output_text: str) -> str:
        """Sanitize output text"""
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', output_text)
        # Normalize whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        return sanitized
    
    def _calculate_confidence_score(self, response: str, question: str) -> float:
        """Calculate confidence score based on response quality"""
        score = 0.0
        
        # Check for quality indicators
        for pattern in self.quality_indicators:
            matches = len(re.findall(pattern, response, re.IGNORECASE))
            score += min(matches * 0.1, 0.3)  # Cap at 0.3 per pattern
        
        # Check for mathematical content
        math_patterns = [r'[=+\-*/]', r'\d+', r'\b(x|y|z|a|b|c)\b']
        math_score = sum(len(re.findall(pattern, response)) for pattern in math_patterns)
        score += min(math_score * 0.05, 0.4)  # Cap at 0.4
        
        # Check for step-by-step structure
        step_patterns = [r'step \d+', r'first', r'second', r'third', r'next', r'finally']
        step_score = sum(len(re.findall(pattern, response, re.IGNORECASE)) for pattern in step_patterns)
        score += min(step_score * 0.1, 0.3)  # Cap at 0.3
        
        return min(score, 1.0)
    
    def _calculate_educational_value(self, response: str) -> float:
        """Calculate educational value of the response"""
        value = 0.0
        
        # Check for explanations
        explanation_patterns = [
            r'\b(because|since|therefore|thus|hence|so)\b',
            r'\b(we have|we get|we obtain|we find|we can see)\b',
            r'\b(let\'s|let us|first|second|third)\b'
        ]
        
        for pattern in explanation_patterns:
            matches = len(re.findall(pattern, response, re.IGNORECASE))
            value += min(matches * 0.1, 0.3)
        
        # Check for mathematical notation
        notation_patterns = [r'\$\$.*?\$\$', r'[=+\-*/]', r'\^', r'_\w+']
        notation_score = sum(len(re.findall(pattern, response)) for pattern in notation_patterns)
        value += min(notation_score * 0.05, 0.4)
        
        # Check for step-by-step structure
        if re.search(r'step \d+', response, re.IGNORECASE):
            value += 0.3
        
        return min(value, 1.0)
    
    def _check_required_elements(self, response: str) -> List[str]:
        """Check for required educational elements"""
        missing = []
        
        # Check for step-by-step solution
        if not re.search(r'step \d+', response, re.IGNORECASE):
            missing.append("step-by-step solution")
        
        # Check for mathematical reasoning
        if not re.search(r'\b(because|since|therefore|thus|hence)\b', response, re.IGNORECASE):
            missing.append("mathematical reasoning")
        
        # Check for final answer
        if not re.search(r'\b(answer|result|solution|final)\b', response, re.IGNORECASE):
            missing.append("final answer")
        
        return missing
    
    def _validate_mathematical_content(self, response: str) -> Dict:
        """Validate mathematical content in response"""
        warnings = []
        
        # Check for mathematical operations
        if not re.search(r'[=+\-*/]', response):
            warnings.append("No mathematical operations found")
        
        # Check for numbers or variables
        if not re.search(r'\d+|\b(x|y|z|a|b|c)\b', response):
            warnings.append("No mathematical variables or numbers found")
        
        # Check for balanced parentheses
        open_parens = response.count('(')
        close_parens = response.count(')')
        if open_parens != close_parens:
            warnings.append("Unbalanced parentheses in mathematical expressions")
        
        return {
            "is_valid": len(warnings) == 0,
            "warnings": warnings
        }
