# TODO API - MongoDB & Flask

A modern, full-stack TODO application built with Flask and MongoDB. This API allows for complete CRUD operations on tasks and serves a clean frontend to interact with them.

## Features
- **Full CRUD**: Create, Read, Update, and Delete tasks.
- **MongoDB Backend**: Persistent storage using MongoDB.
- **Global Error Handling**: Standardized JSON error responses for all API failures.
- **Frontend UI**: Simple and intuitive interface to manage your TODO list.
- **Validation**: Robust input validation to ensure data integrity.

## Prerequisites
- Python 3.x
- MongoDB (running locally or a connection string)
- `.env` file with `MONGO_URI`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SeanShmilov/TODO_API.git
   cd TODO_API
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory:
   ```env
   MONGO_URI=mongodb://localhost:27017/
   ```

## Running the App
```bash
python app.py
```
The application will be available at `http://127.0.0.1:5001`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the frontend application |
| GET | `/tasks` | Retrieves all tasks |
| GET | `/tasks/<id>` | Retrieves a specific task |
| POST | `/tasks` | Creates a new task |
| PUT | `/tasks/<id>` | Updates an existing task |
| DELETE | `/tasks/<id>` | Deletes a task |

## Testing
Run the test suite using `pytest`:
```bash
pytest
```
