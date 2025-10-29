import json
import pandas as pd
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class MathProblem:
    id: str
    question: str
    topic: str
    difficulty: str
    solution_steps: List[str]
    final_answer: str
    explanation: str
    related_concepts: List[str]

class MathDataset:
    """Mathematical knowledge base dataset"""
    
    def __init__(self):
        self.problems = []
        self._create_sample_dataset()
    
    def _create_sample_dataset(self):
        """Create a comprehensive mathematical dataset"""
        sample_problems = [
            {
                "id": "alg_001",
                "question": "Solve the equation: 2x + 5 = 13",
                "topic": "algebra",
                "difficulty": "beginner",
                "solution_steps": [
                    "Start with the equation: 2x + 5 = 13",
                    "Subtract 5 from both sides: 2x = 13 - 5",
                    "Simplify: 2x = 8",
                    "Divide both sides by 2: x = 8/2",
                    "Final answer: x = 4"
                ],
                "final_answer": "x = 4",
                "explanation": "This is a linear equation in one variable. We solve it by isolating the variable using inverse operations.",
                "related_concepts": ["linear equations", "algebraic manipulation", "solving equations"]
            },
            {
                "id": "calc_001",
                "question": "Find the derivative of f(x) = x² + 3x + 2",
                "topic": "calculus",
                "difficulty": "intermediate",
                "solution_steps": [
                    "Given function: f(x) = x² + 3x + 2",
                    "Apply power rule to x²: d/dx(x²) = 2x",
                    "Apply power rule to 3x: d/dx(3x) = 3",
                    "Derivative of constant 2: d/dx(2) = 0",
                    "Combine results: f'(x) = 2x + 3 + 0",
                    "Final answer: f'(x) = 2x + 3"
                ],
                "final_answer": "f'(x) = 2x + 3",
                "explanation": "We use the power rule for differentiation: d/dx(x^n) = nx^(n-1). For each term, we apply this rule and sum the results.",
                "related_concepts": ["derivatives", "power rule", "polynomial functions"]
            },
            {
                "id": "geom_001",
                "question": "Find the area of a triangle with base 6 cm and height 8 cm",
                "topic": "geometry",
                "difficulty": "beginner",
                "solution_steps": [
                    "Given: base = 6 cm, height = 8 cm",
                    "Use the formula: Area = (1/2) × base × height",
                    "Substitute values: Area = (1/2) × 6 × 8",
                    "Calculate: Area = (1/2) × 48",
                    "Final answer: Area = 24 cm²"
                ],
                "final_answer": "24 cm²",
                "explanation": "The area of a triangle is half the product of its base and height. This formula works for any triangle.",
                "related_concepts": ["area", "triangle", "geometry formulas"]
            },
            {
                "id": "trig_001",
                "question": "Find the value of sin(30°)",
                "topic": "trigonometry",
                "difficulty": "beginner",
                "solution_steps": [
                    "Recall the special angle: sin(30°) = 1/2",
                    "This is a standard trigonometric value",
                    "We can verify using the unit circle",
                    "At 30°, the y-coordinate is 1/2",
                    "Final answer: sin(30°) = 1/2"
                ],
                "final_answer": "1/2",
                "explanation": "30° is a special angle in trigonometry. The sine of 30° is always 1/2, which can be derived from a 30-60-90 triangle.",
                "related_concepts": ["trigonometric functions", "special angles", "unit circle"]
            },
            {
                "id": "stat_001",
                "question": "Find the mean of the numbers: 2, 4, 6, 8, 10",
                "topic": "statistics",
                "difficulty": "beginner",
                "solution_steps": [
                    "Given numbers: 2, 4, 6, 8, 10",
                    "Add all numbers: 2 + 4 + 6 + 8 + 10 = 30",
                    "Count the numbers: n = 5",
                    "Apply formula: Mean = Sum / n = 30 / 5",
                    "Final answer: Mean = 6"
                ],
                "final_answer": "6",
                "explanation": "The mean (average) is calculated by adding all values and dividing by the count of values.",
                "related_concepts": ["mean", "average", "descriptive statistics"]
            },
            {
                "id": "calc_002",
                "question": "Evaluate the integral: ∫(2x + 3)dx",
                "topic": "calculus",
                "difficulty": "intermediate",
                "solution_steps": [
                    "Given integral: ∫(2x + 3)dx",
                    "Apply power rule: ∫(2x)dx = 2(x²/2) = x²",
                    "Apply constant rule: ∫(3)dx = 3x",
                    "Combine results: x² + 3x",
                    "Add constant of integration: + C",
                    "Final answer: x² + 3x + C"
                ],
                "final_answer": "x² + 3x + C",
                "explanation": "We use the power rule for integration: ∫(x^n)dx = x^(n+1)/(n+1) + C. We integrate each term separately and add the constant of integration.",
                "related_concepts": ["integration", "power rule", "indefinite integral"]
            },
            {
                "id": "alg_002",
                "question": "Factor the quadratic: x² - 5x + 6",
                "topic": "algebra",
                "difficulty": "intermediate",
                "solution_steps": [
                    "Given quadratic: x² - 5x + 6",
                    "Find two numbers that multiply to 6 and add to -5",
                    "The numbers are -2 and -3: (-2) × (-3) = 6, (-2) + (-3) = -5",
                    "Write as product: (x - 2)(x - 3)",
                    "Verify: (x - 2)(x - 3) = x² - 3x - 2x + 6 = x² - 5x + 6",
                    "Final answer: (x - 2)(x - 3)"
                ],
                "final_answer": "(x - 2)(x - 3)",
                "explanation": "To factor a quadratic, we find two numbers that multiply to the constant term and add to the coefficient of the linear term.",
                "related_concepts": ["factoring", "quadratic equations", "polynomials"]
            },
            {
                "id": "geom_002",
                "question": "Find the circumference of a circle with radius 5 cm",
                "topic": "geometry",
                "difficulty": "beginner",
                "solution_steps": [
                    "Given: radius = 5 cm",
                    "Use formula: C = 2πr",
                    "Substitute: C = 2π(5)",
                    "Calculate: C = 10π",
                    "Approximate: C ≈ 10 × 3.14159 ≈ 31.42 cm",
                    "Final answer: C = 10π cm or approximately 31.42 cm"
                ],
                "final_answer": "10π cm (approximately 31.42 cm)",
                "explanation": "The circumference of a circle is calculated using the formula C = 2πr, where r is the radius.",
                "related_concepts": ["circumference", "circle", "pi", "radius"]
            }
        ]
        
        for problem_data in sample_problems:
            problem = MathProblem(**problem_data)
            self.problems.append(problem)
    
    def get_problems_by_topic(self, topic: str) -> List[MathProblem]:
        """Get problems filtered by topic"""
        return [p for p in self.problems if p.topic == topic]
    
    def get_problems_by_difficulty(self, difficulty: str) -> List[MathProblem]:
        """Get problems filtered by difficulty"""
        return [p for p in self.problems if p.difficulty == difficulty]
    
    def search_problems(self, query: str) -> List[MathProblem]:
        """Search problems by query string"""
        query_lower = query.lower()
        results = []
        
        for problem in self.problems:
            # Check if query matches question, topic, or related concepts
            if (query_lower in problem.question.lower() or
                query_lower in problem.topic.lower() or
                any(query_lower in concept.lower() for concept in problem.related_concepts)):
                results.append(problem)
        
        return results
    
    def get_all_problems(self) -> List[MathProblem]:
        """Get all problems in the dataset"""
        return self.problems
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """Convert dataset to dictionary format for vectorization"""
        return [
            {
                "id": problem.id,
                "question": problem.question,
                "topic": problem.topic,
                "difficulty": problem.difficulty,
                "solution": " ".join(problem.solution_steps),
                "answer": problem.final_answer,
                "explanation": problem.explanation,
                "concepts": " ".join(problem.related_concepts),
                "content": f"{problem.question} {problem.explanation} {' '.join(problem.solution_steps)}"
            }
            for problem in self.problems
        ]

