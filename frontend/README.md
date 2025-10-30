# Math Routing Agent Frontend

## Deploying on Render

To configure your frontend to connect to your backend (e.g., FastAPI hosted on Render), set the backend URL using an environment variable:

Create a `.env` file in this directory with this content (replace the URL with your backend's Render URL):

```
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
```

If no environment variable is set, it defaults to `http://localhost:8000` for local development.

No other changes are required.
