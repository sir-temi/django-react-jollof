# Project Name

Welcome to **Project Name**! This project is a full-stack web application built with **Django** for the backend and **React** for the frontend.

## Tech Stack

-   **Backend:** Django, Django REST Framework
-   **Frontend:** React, Redux, Axios
-   **Database:** SQLite
-   **Others:** ESLint, etc

## Getting Started

### Prerequisites

-   **Backend:**

    -   Python 3.8+
    -   pip
    -   virtualenv

-   **Frontend:**
    -   Node.js 20+
    -   npm or Yarn

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/project-name.git
    cd project-name
    ```

2. **Backend Setup**

    ```bash
    cd backend
    python -m venv env
    source env/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    # Update .env with your configurations
    python manage.py runserver
    ```

3. **Frontend Setup**

    Open a new terminal window/tab and navigate to the frontend directory:

    ```bash
    cd frontend
    npm install
    # Update .env with your configurations
    npm run dev
    ```

## Running the Application

1. **Start the Backend Server**

    Ensure you're in the `backend/` directory and your virtual environment is activated:

    ```bash
    python manage.py runserver
    ```

2. **Start the Frontend Development Server**

    In the `frontend/` directory:

    ```bash
    npm run dev
    ```

    The React app will typically be available at `http://localhost:5173`, and the Django backend at `http://localhost:8000`.
