try:
    import dspy
    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False
    print("Warning: DSPy not available, using fallback implementation")

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import os
from datetime import datetime

@dataclass
class FeedbackData:
    question: str
    response: str
    user_rating: int  # 1-5 scale
    user_comments: str
    timestamp: str
    session_id: str

class MathFeedbackCollector:
    """DSPy module for collecting and processing feedback"""
    
    def __init__(self):
        self.feedback_history = []
        self.feedback_file = "feedback/feedback_history.json"
        self._load_feedback_history()
    
    def collect_feedback(self, question: str, response: str, 
                        rating: int, comments: str = "", 
                        session_id: str = "") -> Dict[str, Any]:
        """Collect user feedback for a math response"""
        feedback = FeedbackData(
            question=question,
            response=response,
            user_rating=rating,
            user_comments=comments,
            timestamp=datetime.now().isoformat(),
            session_id=session_id
        )
        
        self.feedback_history.append(feedback)
        self._save_feedback_history()
        
        return {
            "feedback_id": len(self.feedback_history),
            "status": "collected",
            "rating": rating,
            "timestamp": feedback.timestamp
        }
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get summary of all feedback collected"""
        if not self.feedback_history:
            return {"total_feedback": 0, "average_rating": 0.0}
        
        ratings = [f.user_rating for f in self.feedback_history]
        return {
            "total_feedback": len(self.feedback_history),
            "average_rating": sum(ratings) / len(ratings),
            "rating_distribution": {
                "1": ratings.count(1),
                "2": ratings.count(2),
                "3": ratings.count(3),
                "4": ratings.count(4),
                "5": ratings.count(5)
            },
            "recent_feedback": self.feedback_history[-5:] if len(self.feedback_history) >= 5 else self.feedback_history
        }
    
    def _load_feedback_history(self):
        """Load feedback history from file"""
        try:
            if not os.path.exists(self.feedback_file):
                # Initialize file with an empty array so future reads are valid JSON
                os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
                with open(self.feedback_file, 'w') as f:
                    json.dump([], f)
                self.feedback_history = []
                return

            # File exists — handle empty or malformed JSON gracefully
            with open(self.feedback_file, 'r') as f:
                raw = f.read().strip()
                if not raw:
                    # Empty file: treat as no history and reinitialize
                    self.feedback_history = []
                    with open(self.feedback_file, 'w') as wf:
                        json.dump([], wf)
                    return
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    # Malformed JSON: reset to empty history instead of crashing
                    data = []
                    with open(self.feedback_file, 'w') as wf:
                        json.dump([], wf)

                self.feedback_history = [FeedbackData(**item) for item in data]
        except Exception as e:
            print(f"Error loading feedback history: {e}")
            self.feedback_history = []
    
    def _save_feedback_history(self):
        """Save feedback history to file"""
        try:
            os.makedirs(os.path.dirname(self.feedback_file), exist_ok=True)
            with open(self.feedback_file, 'w') as f:
                json.dump([
                    {
                        "question": f.question,
                        "response": f.response,
                        "user_rating": f.user_rating,
                        "user_comments": f.user_comments,
                        "timestamp": f.timestamp,
                        "session_id": f.session_id
                    }
                    for f in self.feedback_history
                ], f, indent=2)
        except Exception as e:
            print(f"Error saving feedback history: {e}")

class MathResponseEvaluator:
    """DSPy module for evaluating math responses"""
    
    def __init__(self):
        if DSPY_AVAILABLE:
            self.evaluator = dspy.Predict("question, response -> evaluation")
        else:
            self.evaluator = None
    
    def evaluate_response(self, question: str, response: str) -> Dict[str, Any]:
        """Evaluate the quality of a math response"""
        try:
            if self.evaluator:
                # Use DSPy to evaluate the response
                evaluation = self.evaluator(question=question, response=response)
            else:
                # Fallback evaluation
                evaluation = type('obj', (object,), {'evaluation': 'Fallback evaluation: Response appears to be mathematical content.'})
            
            # Parse evaluation results
            evaluation_text = evaluation.evaluation
            
            # Extract scores (assuming evaluation contains numerical scores)
            accuracy_score = self._extract_score(evaluation_text, "accuracy")
            clarity_score = self._extract_score(evaluation_text, "clarity")
            completeness_score = self._extract_score(evaluation_text, "completeness")
            
            return {
                "accuracy": accuracy_score,
                "clarity": clarity_score,
                "completeness": completeness_score,
                "overall_score": (accuracy_score + clarity_score + completeness_score) / 3,
                "evaluation_text": evaluation_text,
                "needs_improvement": self._identify_improvements(evaluation_text)
            }
            
        except Exception as e:
            print(f"Error evaluating response: {e}")
            return {
                "accuracy": 0.5,
                "clarity": 0.5,
                "completeness": 0.5,
                "overall_score": 0.5,
                "evaluation_text": "Evaluation failed",
                "needs_improvement": ["evaluation_error"]
            }
    
    def _extract_score(self, text: str, metric: str) -> float:
        """Extract numerical score for a specific metric"""
        try:
            # Look for patterns like "accuracy: 0.8" or "accuracy score: 8/10"
            import re
            patterns = [
                rf"{metric}:\s*(\d+\.?\d*)",
                rf"{metric}\s*score:\s*(\d+\.?\d*)",
                rf"{metric}\s*=\s*(\d+\.?\d*)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    score = float(match.group(1))
                    # Normalize to 0-1 range if needed
                    if score > 1:
                        score = score / 10
                    return min(max(score, 0), 1)
            
            return 0.5  # Default score if not found
            
        except Exception:
            return 0.5
    
    def _identify_improvements(self, evaluation_text: str) -> List[str]:
        """Identify areas for improvement from evaluation text"""
        improvements = []
        
        if "step" in evaluation_text.lower() and "missing" in evaluation_text.lower():
            improvements.append("add_more_steps")
        
        if "explanation" in evaluation_text.lower() and "unclear" in evaluation_text.lower():
            improvements.append("improve_explanation")
        
        if "answer" in evaluation_text.lower() and "incorrect" in evaluation_text.lower():
            improvements.append("fix_answer")
        
        if "format" in evaluation_text.lower() and "poor" in evaluation_text.lower():
            improvements.append("improve_formatting")
        
        return improvements

class MathLearningSystem:
    """DSPy module for continuous learning from feedback"""
    
    def __init__(self):
        self.feedback_collector = MathFeedbackCollector()
        self.evaluator = MathResponseEvaluator()
        self.learning_data = []
    
    def process_feedback(self, question: str, response: str, 
                        user_rating: int, user_comments: str = "",
                        session_id: str = "") -> Dict[str, Any]:
        """Process user feedback and update learning system"""
        
        # Collect feedback
        feedback_result = self.feedback_collector.collect_feedback(
            question, response, user_rating, user_comments, session_id
        )
        
        # Evaluate response quality
        evaluation = self.evaluator.evaluate_response(question, response)
        
        # Update learning data
        learning_entry = {
            "question": question,
            "response": response,
            "user_rating": user_rating,
            "user_comments": user_comments,
            "evaluation": evaluation,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id
        }
        self.learning_data.append(learning_entry)
        
        # Generate improvement suggestions
        improvements = self._generate_improvements(learning_entry)
        
        return {
            "feedback_collected": feedback_result,
            "evaluation": evaluation,
            "improvements": improvements,
            "learning_updated": True
        }
    
    def _generate_improvements(self, learning_entry: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions based on feedback and evaluation"""
        improvements = []
        
        user_rating = learning_entry["user_rating"]
        evaluation = learning_entry["evaluation"]
        user_comments = learning_entry["user_comments"].lower()
        
        # Based on user rating
        if user_rating <= 2:
            improvements.append("improve_accuracy")
            improvements.append("add_more_explanations")
        
        # Based on evaluation scores
        if evaluation["accuracy"] < 0.7:
            improvements.append("verify_mathematical_correctness")
        
        if evaluation["clarity"] < 0.7:
            improvements.append("simplify_explanations")
        
        if evaluation["completeness"] < 0.7:
            improvements.append("add_more_steps")
        
        # Based on user comments
        if "confusing" in user_comments:
            improvements.append("improve_clarity")
        
        if "incomplete" in user_comments:
            improvements.append("add_more_details")
        
        if "wrong" in user_comments:
            improvements.append("verify_solution")
        
        return list(set(improvements))  # Remove duplicates
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from the learning system"""
        if not self.learning_data:
            return {"insights": "No learning data available"}
        
        # Calculate average scores
        avg_user_rating = sum(entry["user_rating"] for entry in self.learning_data) / len(self.learning_data)
        avg_accuracy = sum(entry["evaluation"]["accuracy"] for entry in self.learning_data) / len(self.learning_data)
        avg_clarity = sum(entry["evaluation"]["clarity"] for entry in self.learning_data) / len(self.learning_data)
        avg_completeness = sum(entry["evaluation"]["completeness"] for entry in self.learning_data) / len(self.learning_data)
        
        # Find common improvement areas
        all_improvements = []
        for entry in self.learning_data:
            all_improvements.extend(entry.get("improvements", []))
        
        improvement_counts = {}
        for improvement in all_improvements:
            improvement_counts[improvement] = improvement_counts.get(improvement, 0) + 1
        
        return {
            "total_interactions": len(self.learning_data),
            "average_user_rating": avg_user_rating,
            "average_accuracy": avg_accuracy,
            "average_clarity": avg_clarity,
            "average_completeness": avg_completeness,
            "common_improvements": sorted(improvement_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "recent_trends": self._analyze_recent_trends()
        }
    
    def _analyze_recent_trends(self) -> Dict[str, Any]:
        """Analyze recent trends in feedback"""
        if len(self.learning_data) < 5:
            return {"trend": "insufficient_data"}
        
        recent_entries = self.learning_data[-5:]
        older_entries = self.learning_data[:-5] if len(self.learning_data) > 5 else []
        
        if not older_entries:
            return {"trend": "insufficient_data"}
        
        recent_avg_rating = sum(entry["user_rating"] for entry in recent_entries) / len(recent_entries)
        older_avg_rating = sum(entry["user_rating"] for entry in older_entries) / len(older_entries)
        
        trend = "improving" if recent_avg_rating > older_avg_rating else "declining"
        
        return {
            "trend": trend,
            "recent_avg_rating": recent_avg_rating,
            "previous_avg_rating": older_avg_rating,
            "change": recent_avg_rating - older_avg_rating
        }
