import asyncio
import json
from typing import Dict, List, Any, Optional
import httpx
from tavily import TavilyClient
from config import settings

class WebSearchMCP:
    """Model Context Protocol implementation for web search"""
    
    def __init__(self):
        self.tavily_client = TavilyClient(api_key=settings.tavily_api_key)
        self.mcp_server_url = settings.mcp_server_url
        self.session = httpx.AsyncClient(timeout=30.0)
    
    async def search_math_content(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for mathematical content using Tavily API"""
        try:
            # Enhance query for mathematical content
            enhanced_query = self._enhance_math_query(query)
            
            # Perform search
            search_results = self.tavily_client.search(
                query=enhanced_query,
                search_depth="advanced",
                max_results=max_results,
                include_domains=["khanacademy.org", "mathworld.wolfram.com", "brilliant.org", 
                               "math.stackexchange.com", "purplemath.com", "mathisfun.com"]
            )
            
            # Process and filter results
            processed_results = []
            for result in search_results.get("results", []):
                if self._is_math_related(result.get("content", "")):
                    processed_results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", ""),
                        "score": result.get("score", 0.0),
                        "source": "tavily"
                    })
            
            return processed_results
            
        except Exception as e:
            print(f"Error in Tavily search: {e}")
            return await self._fallback_search(query, max_results)
    
    def _enhance_math_query(self, query: str) -> str:
        """Enhance query for better mathematical search results"""
        math_keywords = [
            "mathematics", "math", "algebra", "calculus", "geometry", 
            "trigonometry", "statistics", "step by step", "solution"
        ]
        
        # Check if query already contains math keywords
        query_lower = query.lower()
        has_math_keywords = any(keyword in query_lower for keyword in math_keywords)
        
        if not has_math_keywords:
            return f"{query} mathematics step by step solution"
        
        return query
    
    def _is_math_related(self, content: str) -> bool:
        """Check if content is mathematically relevant"""
        math_indicators = [
            "equation", "formula", "solve", "calculate", "derivative", 
            "integral", "algebra", "geometry", "trigonometry", "statistics",
            "step", "solution", "answer", "mathematical", "math"
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in math_indicators)
    
    async def _fallback_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Fallback search using MCP server"""
        try:
            # Try to connect to MCP server
            response = await self.session.post(
                f"{self.mcp_server_url}/search",
                json={"query": query, "max_results": max_results}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            else:
                print(f"MCP server error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error in MCP fallback search: {e}")
            return []
    
    async def get_math_explanation(self, topic: str, difficulty: str = "intermediate") -> Optional[Dict[str, Any]]:
        """Get detailed mathematical explanation for a topic"""
        try:
            # Search for comprehensive explanations
            query = f"{topic} mathematics explanation tutorial {difficulty} level"
            results = await self.search_math_content(query, max_results=3)
            
            if not results:
                return None
            
            # Combine and process results
            combined_content = []
            sources = []
            
            for result in results:
                combined_content.append(result["content"])
                sources.append({
                    "title": result["title"],
                    "url": result["url"]
                })
            
            return {
                "topic": topic,
                "difficulty": difficulty,
                "explanation": " ".join(combined_content),
                "sources": sources,
                "confidence": min(1.0, len(results) * 0.3)
            }
            
        except Exception as e:
            print(f"Error getting math explanation: {e}")
            return None
    
    async def verify_math_solution(self, problem: str, solution: str) -> Dict[str, Any]:
        """Verify mathematical solution using web search"""
        try:
            # Search for similar problems and solutions
            query = f"{problem} solution step by step"
            results = await self.search_math_content(query, max_results=3)
            
            verification_score = 0.0
            similar_solutions = []
            
            for result in results:
                content = result["content"].lower()
                if any(keyword in content for keyword in ["step", "solution", "answer"]):
                    verification_score += 0.3
                    similar_solutions.append({
                        "source": result["title"],
                        "url": result["url"],
                        "content": result["content"][:200] + "..."
                    })
            
            return {
                "verified": verification_score > 0.5,
                "confidence": min(verification_score, 1.0),
                "similar_solutions": similar_solutions
            }
            
        except Exception as e:
            print(f"Error verifying solution: {e}")
            return {
                "verified": False,
                "confidence": 0.0,
                "similar_solutions": []
            }
    
    async def close(self):
        """Close the HTTP session"""
        await self.session.aclose()

