import google.generativeai as genai
from typing import Optional, Dict, Any
from config import settings

class GeminiClient:
    """Google Gemini AI client for mathematical problem solving"""
    
    def __init__(self):
        self.api_key = settings.gemini_api_key
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_math_response(self, question: str, context: str = "") -> Dict[str, Any]:
        """Generate a mathematical response using Gemini"""
        try:
            prompt = self._create_math_prompt(question, context)
            response = self.model.generate_content(prompt)
            
            return {
                "success": True,
                "response": response.text,
                "model": "gemini-pro",
                "confidence": 0.8  # Gemini doesn't provide confidence scores
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": "gemini-pro"
            }
    
    def _create_math_prompt(self, question: str, context: str = "") -> str:
        """Create a specialized prompt for mathematical problem solving"""
        base_prompt = f"""
You are an expert mathematics professor. Please solve the following mathematical question step by step.

Question: {question}

Instructions:
1. Provide a clear, step-by-step solution
2. Explain each step in detail
3. Use proper mathematical notation
4. Include the final answer clearly marked
5. If the problem involves multiple concepts, explain how they relate
6. Be educational and help the student understand the process

{context if context else ""}

Please provide your solution:
"""
        return base_prompt
    
    def evaluate_response_quality(self, question: str, response: str) -> Dict[str, Any]:
        """Evaluate the quality of a mathematical response"""
        try:
            prompt = f"""
Evaluate the quality of this mathematical response:

Question: {question}
Response: {response}

Rate the following aspects on a scale of 0-1:
1. Accuracy: Is the mathematical solution correct?
2. Clarity: Is the explanation clear and easy to follow?
3. Completeness: Does it address all parts of the question?
4. Educational Value: Does it help the student learn?

Provide your evaluation in this format:
Accuracy: [score]
Clarity: [score]
Completeness: [score]
Educational Value: [score]
Overall: [score]

Explanation: [brief explanation of your evaluation]
"""
            
            evaluation_response = self.model.generate_content(prompt)
            return self._parse_evaluation(evaluation_response.text)
            
        except Exception as e:
            return {
                "accuracy": 0.5,
                "clarity": 0.5,
                "completeness": 0.5,
                "educational_value": 0.5,
                "overall": 0.5,
                "explanation": f"Evaluation failed: {str(e)}"
            }
    
    def _parse_evaluation(self, evaluation_text: str) -> Dict[str, Any]:
        """Parse the evaluation response from Gemini"""
        import re
        
        scores = {
            "accuracy": 0.5,
            "clarity": 0.5,
            "completeness": 0.5,
            "educational_value": 0.5,
            "overall": 0.5,
            "explanation": "Evaluation parsing failed"
        }
        
        try:
            # Extract scores using regex
            for metric in ["accuracy", "clarity", "completeness", "educational_value", "overall"]:
                pattern = rf"{metric}:\s*([0-9.]+)"
                match = re.search(pattern, evaluation_text, re.IGNORECASE)
                if match:
                    scores[metric] = float(match.group(1))
            
            # Extract explanation
            explanation_match = re.search(r"explanation:\s*(.+)", evaluation_text, re.IGNORECASE | re.DOTALL)
            if explanation_match:
                scores["explanation"] = explanation_match.group(1).strip()
            
        except Exception as e:
            scores["explanation"] = f"Error parsing evaluation: {str(e)}"
        
        return scores
    
    def generate_web_search_query(self, question: str) -> str:
        """Generate an optimized search query for web search"""
        try:
            prompt = f"""
Convert this mathematical question into an optimized web search query:

Question: {question}

Requirements:
1. Include key mathematical terms
2. Add "step by step solution" or "tutorial"
3. Include the mathematical topic (algebra, calculus, etc.)
4. Keep it concise but comprehensive
5. Use terms that would appear in educational math websites

Search query:
"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            # Fallback to simple enhancement
            return f"{question} mathematics step by step solution"
    
    def extract_solution_steps(self, response: str) -> list:
        """Extract solution steps from a mathematical response"""
        import re
        
        try:
            prompt = f"""
Extract the step-by-step solution from this mathematical response:

Response: {response}

Please extract each step and format them as a numbered list. Each step should be clear and concise.

Steps:
"""
            
            steps_response = self.model.generate_content(prompt)
            steps_text = steps_response.text.strip()
            
            # Parse steps from the response
            steps = []
            for line in steps_text.split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('Step') or line.startswith('-')):
                    # Clean up the step
                    step = re.sub(r'^\d+\.?\s*', '', line)
                    step = re.sub(r'^Step\s+\d+[:\-]?\s*', '', step)
                    step = re.sub(r'^-\s*', '', step)
                    if step:
                        steps.append(step)
            
            return steps if steps else ["Solution steps not clearly identified"]
            
        except Exception as e:
            return ["Error extracting steps: " + str(e)]
    
    def extract_final_answer(self, response: str) -> str:
        """Extract the final answer from a mathematical response"""
        try:
            prompt = f"""
Extract the final answer from this mathematical response:

Response: {response}

Look for:
- "Answer:", "Final answer:", "Solution:", "Result:"
- The final numerical or algebraic result
- The conclusion of the problem

Final answer:
"""
            
            answer_response = self.model.generate_content(prompt)
            return answer_response.text.strip()
            
        except Exception as e:
            return "Final answer not clearly identified"
