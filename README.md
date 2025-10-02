# TaskManagerAPI

A FastAPI backend for managing personal tasks with PostgreSQL. Features user registration, JWT authentication, task CRUD, filtering, and pagination.

---

## Features

* User registration & login with JWT authentication
* Create, read, update, delete tasks
* Task statuses: TODO, IN_PROGRESS, DONE
* Task priorities: LOW, MEDIUM, HIGH, NONE
* Filter tasks by status, priority, and deadline
* Pagination support via limit and offset query parameters
* PostgreSQL database with SQLAlchemy ORM
* Alembic migrations for schema management

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/TaskManagerAPI.git
cd TaskManagerAPI
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up `.env` file (see `.env.example`):

```
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/task_manager
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

5. Run Alembic migrations:

```bash
alembic upgrade head
```

6. Start the server:

```bash
uvicorn main:app --reload
```

---

## API Endpoints

* **Authentication**

  * `POST /auth/register` — register a new user
  * `POST /auth/token` — login and get JWT access token

* **Users**

  * `GET /users/me` — get currently authenticated user info

* **Tasks**

  * `POST /tasks/` — create a new task
  * `GET /tasks/` — retrieve tasks (supports filtering & pagination)
  * `GET /tasks/{id}` — retrieve a task by ID
  * `PUT /tasks/{id}` — update a task
  * `DELETE /tasks/{id}` — delete a task

### Query parameters for filtering tasks:

* `status` — TODO, IN_PROGRESS, DONE
* `priority` — LOW, MEDIUM, HIGH, NONE
* `deadline_before` — return tasks before this date
* `deadline_after` — return tasks after this date
* `limit` — maximum number of tasks returned
* `offset` — number of tasks to skip
