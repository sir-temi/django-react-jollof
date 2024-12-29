# Django-React-Jollof

Welcome to **Django-React-Jollof**! This package scaffolds a full-stack web application with **Django** for the backend and **React** for the frontend. It simplifies the setup process by automating the configuration, migration, and installation of necessary dependencies.

## Tech Stack

-   **Backend:** Django, Django REST Framework
-   **Frontend:** React, Axios, Redux (optional)
-   **Database:** SQLite (default, configurable)
-   **Authentication:** Google login integration (optional)
-   **Others:** ESLint, Prettier, Vite (for fast React development)

## Getting Started

### Prerequisites

Ensure you have the following installed:

-   **Backend:**

    -   Python 3.8+
    -   pip
    -   virtualenv

-   **Frontend:**
    -   Node.js 20+ (recommended version)
    -   npm or Yarn

### Installation

1. **Install the Package**

    Install the package via `pip`:

    ```bash
    pip install django-react-jollof
    ```

2. **Run the Setup Command**

    After installation, use the `django-react-jollof cook` command to scaffold the project. This will:

    - Set up the Django backend.
    - Install frontend dependencies.
    - Run database migrations.
    - Set up social login configurations (if selected).

    ```bash
    django-react-jollof cook
    ```

    Follow the prompts to choose the frontend framework (Bootstrap or Material) and select social login providers (Google or none).

### Environment Configuration

-   **Backend**: Configure environment variables by creating a `.env` file in the `backend` directory, optional, but recommended. For example:

    ```plaintext
    DEBUG=True
    SECRET_KEY=<your_secret_key>
    ```

-   **Frontend**: Update the `.env` file in the `frontend` directory to configure the API URL and any social login keys.

    Example:

    ```plaintext
    VITE_API_URL=http://localhost:8000/api
    VITE_GOOGLE_CLIENT_ID=<your_google_client_id>
    ```

---

## Running the Application

1. **Start the Backend Server**

    Ensure you're in the `backend/` directory and your virtual environment is activated:

    ```bash
    cd backend
    source env/bin/activate  # For Linux/macOS
    # venv\Scripts\activate  # For Windows
    python manage.py runserver
    ```

    The backend will be available at `http://localhost:8000`.

2. **Start the Frontend Development Server**

    In the `frontend/` directory:

    ```bash
    cd frontend
    npm run dev
    ```

    The React app will be available at `http://localhost:5173`.

---

## Authentication Setup

### Social Login (Google, GitHub)

**To enable social login functionality (Google), ensure you've configured the following in your `.env` files:**

-   For **Google**:
    -   Google Client ID and Client Secret from the Google Developer Console.

### Optional: Using Social Login Providers

You can choose to enable Google or no social login methods during setup via environment variables. Modify the configuration in your `.env` files for both the backend and frontend to integrate them.

Example:

-   Backend `.env`:

    ```plaintext
    GOOGLE_CLIENT_ID=<google_client_id>
    GOOGLE_CLIENT_SECRET=<google_client_secret>
    ```

-   Frontend `.env`:

    ```plaintext
    VITE_GOOGLE_CLIENT_ID=<google_client_id>
    VITE_GITHUB_CLIENT_ID=<github_client_id>
    ```

---

## Additional Features

-   **Admin Dashboard**: Django’s default admin panel for managing users and data.
-   **Frontend Customization**: Choose between **Bootstrap** or **Material UI** for the frontend.
-   **API Integration**: Django REST Framework is used for seamless API integration between the backend and frontend.
-   **Cross-Origin Resource Sharing (CORS)**: Configured to allow the frontend to make requests to the backend from different domains.

---

## Development Workflow

-   **Backend**:

    -   Make changes to the backend code and use Django’s built-in features to manage migrations, users, and data.
    -   Use the Django REST Framework for building and managing your APIs.

-   **Frontend**:
    -   Make changes in the React components located in `frontend/src/`.
    -   Use Vite for fast, hot-reload development in the React frontend.

---

## Contribution

1. **Fork the Repository**: Fork the repo to your GitHub account.
2. **Clone Your Fork**: Clone the forked repository to your local machine.
3. **Create a Branch**: Create a feature branch for your changes.
4. **Make Your Changes**: Implement your feature or fix a bug.
5. **Commit Your Changes**: Commit your changes with meaningful messages.
6. **Push Your Changes**: Push your branch to your fork.
7. **Submit a Pull Request**: Open a pull request to the main repository.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Conclusion

This `README.md` provides an easy-to-follow guide for setting up **Django-React-Jollof** as a package, including detailed steps for installation, running the backend and frontend, and configuring social login. The `django-react-jollof cook` command automates much of the setup process for you.

Let me know if you need further changes or additions!
