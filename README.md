# BookLibraryAPI

A modern, OpenAPI-driven Flask web application for managing authors, books, and reviews. Features a beautiful, interactive HTML UI and a fully documented REST API.

## Features

- Modern, responsive UI with navigation, sidebar, and in-place editing
- All endpoints (API + HTML) defined in OpenAPI (Swagger) spec
- Connexion-powered: OpenAPI is the single source of truth for routes
- Robust error handling and user feedback
- Modular, scalable Flask application structure

## How to Run

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd BookLibraryAPI
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```sh
   python app.py
   ```

5. **Access the app:**
   - Home: [http://localhost:5050/home/](http://localhost:5050/home/)
   - Authors: [http://localhost:5050/home/author/](http://localhost:5050/home/author/)
   - Books: [http://localhost:5050/home/books/](http://localhost:5050/home/books/)
   - Reviews: [http://localhost:5050/home/reviews/](http://localhost:5050/home/reviews/)
   - API docs (Swagger UI): [http://localhost:5050/ui/](http://localhost:5050/ui/)

**Note:** The SQLite database will be created in the `instance/` directory automatically.
