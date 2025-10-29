from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import asyncio
from contextlib import asynccontextmanager

from agents.routing_agent import MathRoutingAgent
from knowledge_base.vector_store import VectorStore
from feedback.dspy_feedback import MathLearningSystem

# Global variables for dependency injection
routing_agent = None
vector_store = None
learning_system = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global routing_agent, vector_store, learning_system
    
    # Startup
    print("Starting Math Routing Agent...")
    routing_agent = MathRoutingAgent()
    vector_store = VectorStore()
    learning_system = MathLearningSystem()
    
    # Populate knowledge base
    print("Populating knowledge base...")
    vector_store.populate_knowledge_base()
    
    yield
    
    # Shutdown
    print("Shutting down...")
    if routing_agent:
        await routing_agent.close()

app = FastAPI(
    title="Math Routing Agent API",
    description="AI-powered mathematical problem solving with Agentic-RAG architecture",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class MathQuestionRequest(BaseModel):
    question: str
    user_id: Optional[str] = "anonymous"

class FeedbackRequest(BaseModel):
    session_id: str
    rating: int
    comments: Optional[str] = ""

class MathQuestionResponse(BaseModel):
    success: bool
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    routing_info: Optional[Dict[str, Any]] = None
    validation_info: Optional[Dict[str, Any]] = None
    session_id: str

class FeedbackResponse(BaseModel):
    success: bool
    message: str
    session_id: str

class LearningInsightsResponse(BaseModel):
    insights: Dict[str, Any]

# Dependency functions
def get_routing_agent() -> MathRoutingAgent:
    if routing_agent is None:
        raise HTTPException(status_code=503, detail="Routing agent not initialized")
    return routing_agent

def get_vector_store() -> VectorStore:
    if vector_store is None:
        raise HTTPException(status_code=503, detail="Vector store not initialized")
    return vector_store

def get_learning_system() -> MathLearningSystem:
    if learning_system is None:
        raise HTTPException(status_code=503, detail="Learning system not initialized")
    return learning_system

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Math Routing Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "routing_agent": routing_agent is not None,
            "vector_store": vector_store is not None,
            "learning_system": learning_system is not None
        }
    }

@app.post("/ask", response_model=MathQuestionResponse)
async def ask_math_question(
    request: MathQuestionRequest,
    agent: MathRoutingAgent = Depends(get_routing_agent)
):
    """Ask a mathematical question"""
    try:
        result = await agent.process_question(request.question, request.user_id)
        return MathQuestionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    agent: MathRoutingAgent = Depends(get_routing_agent)
):
    """Submit feedback for a response"""
    try:
        result = await agent.collect_feedback(
            request.session_id,
            request.rating,
            request.comments
        )
        return FeedbackResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing feedback: {str(e)}")

@app.get("/insights", response_model=LearningInsightsResponse)
async def get_learning_insights(
    agent: MathRoutingAgent = Depends(get_routing_agent)
):
    """Get learning insights from the system"""
    try:
        insights = await agent.get_learning_insights()
        return LearningInsightsResponse(insights=insights)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting insights: {str(e)}")

@app.get("/knowledge-base/info")
async def get_knowledge_base_info(
    vector_store: VectorStore = Depends(get_vector_store)
):
    """Get information about the knowledge base"""
    try:
        info = vector_store.get_collection_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting knowledge base info: {str(e)}")

@app.post("/knowledge-base/search")
async def search_knowledge_base(
    query: str,
    limit: int = 5,
    vector_store: VectorStore = Depends(get_vector_store)
):
    """Search the knowledge base directly"""
    try:
        results = vector_store.search(query, limit=limit)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching knowledge base: {str(e)}")

@app.get("/feedback/summary")
async def get_feedback_summary(
    learning_system: MathLearningSystem = Depends(get_learning_system)
):
    """Get feedback summary"""
    try:
        summary = learning_system.feedback_collector.get_feedback_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting feedback summary: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "success": False}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "success": False}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

