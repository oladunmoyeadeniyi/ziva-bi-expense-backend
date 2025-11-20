Ziva BI - Expense Module (Backend)
==================================

This is the backend service for the Ziva BI Expense Management Module.
It is FastAPI-based and uses SQLite by default for simple deployment.

To run with Docker:
  docker build -t ziva-expense-backend .
  docker run -p 8000:8000 -v $(pwd)/app/static_uploads:/app/app/static_uploads ziva-expense-backend

Or use docker-compose to run with the frontend.
