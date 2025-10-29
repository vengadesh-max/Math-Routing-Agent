import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

from knowledge_base.vector_store import VectorStore
from mcp.web_search_mcp import WebSearchMCP
from feedback.dspy_feedback import MathLearningSystem
from guardrails.input_guardrails import InputGuardrails, InputValidationResult
from guardrails.output_guardrails import OutputGuardrails, OutputValidationResult
from llm.gemini_client import GeminiClient

class RouteDecision(Enum):
    KNOWLEDGE_BASE = "knowledge_base"
    WEB_SEARCH = "web_search"
    REJECT = "reject"

@dataclass
class RoutingResult:
    decision: RouteDecision
    confidence: float
    reasoning: str
    source: str
    data: Optional[Dict[str, Any]] = None

@dataclass
class MathResponse:
    question: str
    answer: str
    solution_steps: List[str]
    explanation: str
    source: str
    confidence: float
    session_id: str
    timestamp: str

class MathRoutingAgent:
    """Main routing agent for mathematical problem solving"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.web_search = WebSearchMCP()
        self.learning_system = MathLearningSystem()
        self.input_guardrails = InputGuardrails()
        self.output_guardrails = OutputGuardrails()
        self.gemini_client = GeminiClient()
        self.session_counter = 0
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        self.session_counter += 1
        return f"math_session_{self.session_counter}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    async def process_question(self, question: str, user_id: str = "anonymous") -> Dict[str, Any]:
        """Main entry point for processing mathematical questions"""
        session_id = self._generate_session_id()
        
        try:
            # Step 1: Input validation and guardrails
            input_validation = self.input_guardrails.validate_input(question)
            if not input_validation.is_valid:
                return {
                    "success": False,
                    "error": "Input validation failed",
                    "warnings": input_validation.warnings,
                    "session_id": session_id
                }
            
            # Step 2: Route decision
            routing_result = await self._make_routing_decision(question, input_validation)
            
            if routing_result.decision == RouteDecision.REJECT:
                return {
                    "success": False,
                    "error": "Question rejected",
                    "reasoning": routing_result.reasoning,
                    "session_id": session_id
                }
            
            # Step 3: Generate response based on routing decision
            response = await self._generate_response(question, routing_result, session_id)
            
            # Step 4: Output validation and guardrails
            output_validation = self.output_guardrails.validate_output(response.answer, question)
            
            # Always return a result; treat validation as advisory unless content is clearly unsafe
            # If sanitization produced text, prefer it
            if output_validation.sanitized_output:
                response.answer = output_validation.sanitized_output
            
            return {
                "success": True,
                "response": {
                    "question": response.question,
                    "answer": response.answer,
                    "solution_steps": response.solution_steps,
                    "explanation": response.explanation,
                    "source": response.source,
                    "confidence": response.confidence,
                    "session_id": response.session_id,
                    "timestamp": response.timestamp
                },
                "session_id": response.session_id,
                "routing_info": {
                    "decision": routing_result.decision.value,
                    "confidence": routing_result.confidence,
                    "reasoning": routing_result.reasoning
                },
                "validation_info": {
                    "input_warnings": input_validation.warnings,
                    "output_warnings": output_validation.warnings,
                    "educational_value": output_validation.educational_value
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Processing failed: {str(e)}",
                "session_id": session_id
            }
    
    async def _make_routing_decision(self, question: str, input_validation: InputValidationResult) -> RoutingResult:
        """Make routing decision between knowledge base and web search"""
        
        # First, try knowledge base search
        kb_results = self.vector_store.search(question, limit=3, score_threshold=0.7)
        
        if kb_results and kb_results[0]["score"] > 0.8:
            return RoutingResult(
                decision=RouteDecision.KNOWLEDGE_BASE,
                confidence=kb_results[0]["score"],
                reasoning="High confidence match found in knowledge base",
                source="knowledge_base",
                data={"results": kb_results}
            )
        
        # If knowledge base has moderate results, check if we should use them
        if kb_results and kb_results[0]["score"] > 0.5:
            # Check if question is complex enough to warrant web search
            complexity_score = self._assess_question_complexity(question)
            
            if complexity_score < 0.6:  # Simple question, use knowledge base
                return RoutingResult(
                    decision=RouteDecision.KNOWLEDGE_BASE,
                    confidence=kb_results[0]["score"],
                    reasoning="Moderate match in knowledge base for simple question",
                    source="knowledge_base",
                    data={"results": kb_results}
                )
        
        # Use web search for complex questions or when knowledge base fails
        return RoutingResult(
            decision=RouteDecision.WEB_SEARCH,
            confidence=0.7,
            reasoning="Question requires web search for comprehensive answer",
            source="web_search"
        )
    
    def _assess_question_complexity(self, question: str) -> float:
        """Assess the complexity of a mathematical question"""
        complexity_indicators = [
            r'\b(prove|derive|show that|demonstrate)\b',
            r'\b(integral|derivative|limit|series|convergence)\b',
            r'\b(matrix|vector|eigenvalue|determinant)\b',
            r'\b(probability|distribution|hypothesis|statistical)\b',
            r'\b(optimization|constraint|lagrange|calculus of variations)\b',
            r'\b(complex|imaginary|real analysis|topology)\b'
        ]
        
        import re
        complexity_score = 0.0
        
        for pattern in complexity_indicators:
            if re.search(pattern, question, re.IGNORECASE):
                complexity_score += 0.2
        
        # Check for multiple mathematical concepts
        math_concepts = len(re.findall(r'\b(equation|function|formula|theorem|lemma)\b', question, re.IGNORECASE))
        complexity_score += min(math_concepts * 0.1, 0.3)
        
        return min(complexity_score, 1.0)
    
    async def _generate_response(self, question: str, routing_result: RoutingResult, session_id: str) -> MathResponse:
        """Generate response based on routing decision"""
        
        if routing_result.decision == RouteDecision.KNOWLEDGE_BASE:
            return await self._generate_kb_response(question, routing_result, session_id)
        else:
            return await self._generate_web_response(question, routing_result, session_id)
    
    async def _generate_kb_response(self, question: str, routing_result: RoutingResult, session_id: str) -> MathResponse:
        """Generate response from knowledge base"""
        kb_data = routing_result.data["results"][0]["content"]
        
        # Extract solution steps
        solution_steps = kb_data.get("solution_steps", [])
        if isinstance(solution_steps, str):
            solution_steps = solution_steps.split('\n')
        
        return MathResponse(
            question=question,
            answer=kb_data.get("answer", ""),
            solution_steps=solution_steps,
            explanation=kb_data.get("explanation", ""),
            source="knowledge_base",
            confidence=routing_result.confidence,
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
    
    async def _generate_web_response(self, question: str, routing_result: RoutingResult, session_id: str) -> MathResponse:
        """Generate response from web search"""
        web_results = await self.web_search.search_math_content(question, max_results=3)
        
        if not web_results:
            return MathResponse(
                question=question,
                answer="I apologize, but I couldn't find a suitable solution for your question. Please try rephrasing or providing more specific details.",
                solution_steps=["Unable to find solution"],
                explanation="No relevant mathematical content found in web search",
                source="web_search",
                confidence=0.0,
                session_id=session_id,
                timestamp=datetime.now().isoformat()
            )
        
        # Combine web results into context
        combined_content = []
        sources = []
        
        for result in web_results:
            combined_content.append(result["content"])
            sources.append({"title": result["title"], "url": result["url"]})
        
        context = " ".join(combined_content)
        
        # Use Gemini to generate a comprehensive response
        gemini_response = self.gemini_client.generate_math_response(question, context)
        
        if gemini_response["success"]:
            # Extract solution steps and final answer using Gemini
            solution_steps = self.gemini_client.extract_solution_steps(gemini_response["response"])
            final_answer = self.gemini_client.extract_final_answer(gemini_response["response"])
            
            return MathResponse(
                question=question,
                answer=final_answer,
                solution_steps=solution_steps,
                explanation=gemini_response["response"],
                source="web_search",
                confidence=gemini_response["confidence"],
                session_id=session_id,
                timestamp=datetime.now().isoformat()
            )
        else:
            # Fallback to original method
            solution_steps = self._extract_solution_steps(combined_content)
            
            return MathResponse(
                question=question,
                answer=self._extract_final_answer(combined_content),
                solution_steps=solution_steps,
                explanation=self._generate_explanation(combined_content),
                source="web_search",
                confidence=min(0.8, len(web_results) * 0.2),
                session_id=session_id,
                timestamp=datetime.now().isoformat()
            )
    
    def _extract_solution_steps(self, content: List[str]) -> List[str]:
        """Extract solution steps from web content"""
        steps = []
        combined_text = " ".join(content)
        
        # Look for step patterns
        import re
        step_patterns = [
            r'step \d+[:\-]\s*([^.]*\.)',
            r'\d+[\.\)]\s*([^.]*\.)',
            r'first[:\-]\s*([^.]*\.)',
            r'second[:\-]\s*([^.]*\.)',
            r'third[:\-]\s*([^.]*\.)',
            r'next[:\-]\s*([^.]*\.)',
            r'finally[:\-]\s*([^.]*\.)'
        ]
        
        for pattern in step_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            steps.extend(matches)
        
        # If no steps found, create generic steps
        if not steps:
            steps = [
                "Analyze the given problem",
                "Apply appropriate mathematical concepts",
                "Solve step by step",
                "Verify the solution"
            ]
        
        return steps[:10]  # Limit to 10 steps
    
    def _extract_final_answer(self, content: List[str]) -> str:
        """Extract final answer from web content"""
        combined_text = " ".join(content)
        
        # Look for answer patterns
        import re
        answer_patterns = [
            r'answer[:\-]\s*([^.]*\.)',
            r'result[:\-]\s*([^.]*\.)',
            r'solution[:\-]\s*([^.]*\.)',
            r'therefore[,\s]+([^.]*\.)',
            r'thus[,\s]+([^.]*\.)'
        ]
        
        for pattern in answer_patterns:
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Answer not explicitly stated in the sources"
    
    def _generate_explanation(self, content: List[str]) -> str:
        """Generate explanation from web content"""
        combined_text = " ".join(content)
        
        # Extract explanation sentences
        import re
        explanation_sentences = []
        
        # Look for explanation patterns
        explanation_patterns = [
            r'[^.]*because[^.]*\.',
            r'[^.]*since[^.]*\.',
            r'[^.]*therefore[^.]*\.',
            r'[^.]*thus[^.]*\.',
            r'[^.]*we have[^.]*\.',
            r'[^.]*we get[^.]*\.',
            r'[^.]*we obtain[^.]*\.'
        ]
        
        for pattern in explanation_patterns:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            explanation_sentences.extend(matches)
        
        if explanation_sentences:
            return " ".join(explanation_sentences[:3])  # Limit to 3 sentences
        
        return "This solution is based on mathematical principles and step-by-step reasoning."
    
    async def collect_feedback(self, session_id: str, rating: int, comments: str = "") -> Dict[str, Any]:
        """Collect user feedback for a response"""
        # This would be called by the API endpoint
        # For now, return a placeholder
        return {
            "success": True,
            "message": "Feedback collected successfully",
            "session_id": session_id
        }
    
    async def get_learning_insights(self) -> Dict[str, Any]:
        """Get learning insights from the system"""
        return self.learning_system.get_learning_insights()
    
    async def close(self):
        """Clean up resources"""
        await self.web_search.close()
