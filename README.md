# Todo Project

## Setup

1. Create credentials
    * Go to https://console.cloud.google.com/
    * Select your project or create a new one.
    * Go to Credentials
    * Create OAuth 2.0 credentials for desktop

2. Clone the repository:
    ```bash
    git clone git@github.com:d1mmm/ToDoList.git
    cd ToDoList
    ```

3. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
   
4. Change CLIENT_ID and SECRET

    **In todo_list/settings.py change CLIENT_ID and SECRET**

5. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

6. Run the migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

8. Run the development server:
    ```bash
    python manage.py runserver
    ```

9. Access the API at `http://127.0.0.1:8000/api/`.

## API Endpoints

- List all todos: `GET /api/todos/`
- Retrieve a todo by ID: `GET /api/todos/{id}/`
- Create a new todo: `POST /api/todos/`
- Update a todo: `PUT /api/todos/{id}/`
- Delete a todo: `DELETE /api/todos/{id}/`

## Filtering and Pagination

- Filter by due date: `GET /api/todos/?due_date_after=YYYY-MM-DD&due_date_before=YYYY-MM-DD`
- Filter by completion status: `GET /api/todos/?completed=true`
- Pagination: The list endpoint supports pagination with `page` and `page_size` query parameters.

## Testing

Run the tests:
```bash
python manage.py test
```
