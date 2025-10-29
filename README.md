# Math Routing Agent - AI-Powered Mathematical Problem Solving

An advanced AI system that replicates a mathematical professor's capabilities through an Agentic-RAG (Retrieval-Augmented Generation) architecture. The system intelligently routes between a curated knowledge base and web search to provide comprehensive, step-by-step mathematical solutions while incorporating human feedback for continuous learning.

## 🚀 Features

- **Intelligent Routing**: Automatically chooses between knowledge base and web search
- **Comprehensive Knowledge Base**: Curated mathematical problems with step-by-step solutions
- **Web Search Integration**: MCP (Model Context Protocol) for external content
- **Human-in-the-Loop Learning**: DSPy-powered feedback system for continuous improvement
- **AI Gateway Guardrails**: Input/output validation and content safety
- **Modern UI**: React frontend with real-time interaction
- **JEE Benchmarking**: Comprehensive performance evaluation

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React UI      │    │   FastAPI        │    │   Vector DB     │
│   (Frontend)    │◄──►│   (Backend)      │◄──►│   (Qdrant)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Routing Agent   │
                       │  (LangGraph)     │
                       └──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            ┌─────────────┐    ┌─────────────┐
            │ Knowledge   │    │ Web Search  │
            │ Base        │    │ (MCP)       │
            └─────────────┘    └─────────────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
                       ┌──────────────────┐
                       │ Feedback System  │
                       │ (DSPy)           │
                       └──────────────────┘
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker (for Qdrant)
- API Keys: OpenAI, Tavily

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd math-routing-agent
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Update environment variables**
   ```bash
   # Edit .env file with your API keys
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

4. **Start the services**
   ```bash
   # Terminal 1: Start backend
   python main.py
   
   # Terminal 2: Start frontend
   cd frontend
   npm start
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Qdrant: http://localhost:6333

## 📚 Usage

### Asking Math Questions

1. Navigate to the "Ask Question" section
2. Enter your mathematical question
3. The system will automatically route to the best source
4. Receive a comprehensive step-by-step solution
5. Provide feedback to help the system learn

### Example Questions

- **Algebra**: "Solve the equation: 2x + 5 = 13"
- **Calculus**: "Find the derivative of f(x) = x² + 3x + 2"
- **Geometry**: "Find the area of a triangle with base 6 cm and height 8 cm"
- **Trigonometry**: "What is the value of sin(30°)?"
- **Statistics**: "Find the mean of the numbers: 2, 4, 6, 8, 10"

### Viewing Learning Insights

1. Navigate to the "Insights" section
2. View system performance metrics
3. Analyze learning trends
4. Monitor feedback patterns

## 🧪 Benchmarking

Run the JEE benchmark to evaluate system performance:

```bash
python run_benchmark.py
```

The benchmark tests the system with JEE-level mathematical problems and provides detailed performance metrics.

## 🔧 API Endpoints

### Core Endpoints

- `POST /ask` - Ask a mathematical question
- `POST /feedback` - Submit feedback for a response
- `GET /insights` - Get learning insights
- `GET /health` - Health check

### Knowledge Base Endpoints

- `GET /knowledge-base/info` - Get knowledge base information
- `POST /knowledge-base/search` - Search knowledge base directly

### Example API Usage

```python
import requests

# Ask a question
response = requests.post('http://localhost:8000/ask', json={
    'question': 'Solve the equation: 2x + 5 = 13'
})

# Submit feedback
feedback = requests.post('http://localhost:8000/feedback', json={
    'session_id': 'session_123',
    'rating': 5,
    'comments': 'Great explanation!'
})
```

## 🏛️ Project Structure

```
math-routing-agent/
├── agents/                 # Routing agent implementation
│   └── routing_agent.py
├── benchmark/              # JEE benchmark testing
│   ├── jee_benchmark.py
│   └── results/
├── docs/                   # Documentation
│   └── FINAL_PROPOSAL.md
├── feedback/               # DSPy feedback system
│   └── dspy_feedback.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   └── App.js
│   └── package.json
├── guardrails/             # Input/output validation
│   ├── input_guardrails.py
│   └── output_guardrails.py
├── knowledge_base/         # Vector database and dataset
│   ├── math_dataset.py
│   └── vector_store.py
├── mcp/                    # Model Context Protocol
│   └── web_search_mcp.py
├── main.py                 # FastAPI application
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── setup.py               # Setup script
└── README.md              # This file
```

## 🔒 Security Features

### Input Guardrails
- Content validation and sanitization
- Mathematical content detection
- Length and format validation
- Harmful content filtering

### Output Guardrails
- Educational value assessment
- Mathematical content validation
- Step-by-step structure verification
- Content safety checks

## 📊 Performance Metrics

The system tracks various performance metrics:

- **Accuracy**: Mathematical correctness of responses
- **Completeness**: How well responses address the question
- **Clarity**: Quality of explanations and formatting
- **Confidence**: System's confidence in responses
- **Response Time**: Time to generate responses
- **Source Performance**: Knowledge base vs web search effectiveness

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain** for agent framework
- **DSPy** for feedback and learning
- **Qdrant** for vector database
- **Tavily** for web search
- **React** for frontend framework
- **FastAPI** for backend framework

## 🔮 Future Enhancements

- [ ] Advanced mathematical parsing with symbolic libraries
- [ ] Multi-language support
- [ ] Visual mathematical diagrams
- [ ] Collaborative learning features
- [ ] Performance optimization and caching
- [ ] Mobile application
- [ ] Integration with learning management systems

---


