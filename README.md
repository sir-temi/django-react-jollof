# 🥘 Django-React-Jollof

![Python Versions](https://img.shields.io/pypi/pyversions/django-react-jollof)
![PyPI](https://img.shields.io/pypi/v/django-react-jollof)
![PyPI - Downloads](https://img.shields.io/pypi/dm/django-react-jollof)
![License](https://img.shields.io/pypi/l/django-react-jollof)
![Build Status](https://github.com/sir-temi/django-react-jollof/actions/workflows/ci.yml/badge.svg)

Welcome to **Django-React-Jollof (DRJ)**! This package scaffolds a fully functional full-stack web application with **Django** for the backend and **React** for the frontend. It simplifies the entire setup process by automating key tasks like configuration, database migrations, API integration, and dependency installation.

With **Django-React-Jollof**, you can quickly set up a robust web app and focus on bringing your ideas to life, leaving the repetitive boilerplate setup to the tool. Whether you're building a simple project or a scalable application, DRJ equips you with the essentials to get started effortlessly.

---

## 📖 Table of Contents

1. [Features](#-features)
2. [Tech Stack](#️-tech-stack)
3. [Getting Started](#-getting-started)
    - [Prerequisites](#-prerequisites)
    - [Installation](#-installation)
4. [Setting Up the Environment](#setting-up-the-environment)
5. [Authentication Setup](#-authentication-setup)
6. [Additional Features](#-additional-features)
7. [Development Workflow](#-development-workflow)
8. [Final Project Structure](#final-project-structure)
9. [Contribution](#-contribution)
10. [License](#-license)
11. [Connect with Us](#-connect-with-us)
12. [Conclusion](#conclusion)

---

## 🌟 Features

-   **🔧 Full-Stack Scaffolding**: Django + React setup in seconds.
-   **⚡ Modern Frontend**: React with Vite for fast development.
-   **🔐 Authentication**: Optional Google login integration.
-   **🎨 Customizable**: Choose Bootstrap or Material UI for styling.
-   **📡 API Ready**: Django REST Framework for seamless backend/frontend communication.

---

## 🛠️ Tech Stack

| **Component** | **Technology**                                      |
| ------------- | --------------------------------------------------- |
| **Backend**   | Django, Django REST Framework                       |
| **Frontend**  | React, Axios                                        |
| **Database**  | SQLite (default, configurable)                      |
| **Styling**   | Bootstrap or Material UI                            |
| **Tools**     | ESLint, Prettier, Vite (for fast React development) |

---

## 🚀 Getting Started

### ✅ Prerequisites

Make sure you have the following installed:

#### **Backend**:

-   Python 3.10+
-   pip
-   virtualenv

#### **Frontend**:

-   Node.js 20+ (recommended version)
-   npm or Yarn

### 🔗 Installation

1. **Create a Virtual Environment**:

    Navigate to your project directory and run the following commands to create and activate a virtual environment:

    ```bash
    python -m venv env
    ```

    **Activate the virtual environment**:

    - On Linux/macOS:
        ```bash
        source env/bin/activate
        ```
    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```

2. **Install the Package**:

    With the virtual environment activated, install the package via pip:

    ```bash
    pip install django-react-jollof
    ```

3. **Run the Setup Command**:

    ```bash
    django-react-jollof cook
    ```

    During the setup, you will be prompted to provide a project name. Choose your desired name, and it will be automatically configured throughout the app, including:

    - App name in the NavBar.
    - The browser tab title for the frontend.

    The command will also:

    - Set up the Django backend and install necessary requirements.
    - Set up the React frontend and install dependencies.
    - Run database migrations.
    - Configure social login (if selected).

---

## Setting Up the Environment

In the `frontend/` directory, create a `.env` file:

```plaintext
VITE_GOOGLE_CLIENT_ID=<your_google_client_id>
```

To start the backend server, navigate to the `backend` directory, activate your virtual environment, and run:

```bash
cd backend
source env/bin/activate  # For Linux/macOS
# venv\Scripts\activate  # For Windows
python manage.py runserver
```

The backend will be available at `http://localhost:8000`.

Next, start the frontend development server. Navigate to the `frontend` directory and run:

```bash
cd frontend
npm run dev
```

The React app will be available at `http://localhost:5173`.

---

## 🔑 Authentication Setup

To enable Google login, configure the following in your `.env` files:

**Backend**:

```plaintext
GOOGLE_CLIENT_ID=<your_google_client_id>
GOOGLE_CLIENT_SECRET=<your_google_client_secret>
```

**Frontend**:

```plaintext
VITE_GOOGLE_CLIENT_ID=<your_google_client_id>
```

Obtain the credentials from the [Google Developer Console](https://console.cloud.google.com/).

---

## 🎁 Additional Features

-   **Styling Frameworks**: Choose between Bootstrap and Material UI for the frontend.
-   **API Integration**: Powered by Django REST Framework.
-   **CORS**: Pre-configured for frontend-backend communication.

---

## 🔄 Development Workflow

Edit backend code in the `backend/` directory and use Django's tools for migrations, testing, and database management. Modify React components in `frontend/src/` and use Vite for hot-reload development.

---

## Final Project Structure

```
backend
│   ├── backend
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── db.sqlite3
│   ├── manage.py
│   ├── requirements.txt
│   └── users
│       ├── models.py
│       ├── permissions.py
│       ├── serializers.py
│       ├── tests
│       │   ├── __init__.py
│       │   ├── test_models.py
│       │   ├── test_permissions.py
│       │   ├── test_serializers.py
│       │   └── test_views.py
│       ├── urls.py
│       └── views.py
frontend
│   ├── env.d.ts
│   ├── index.html
│   ├── jsconfig.json
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   │   └── vite.svg
│   ├── src
│   │   ├── App.jsx
│   │   ├── actions
│   │   │   └── authActions.js
│   │   ├── assets
│   │   │   └── react.svg
│   │   ├── components
│   │   │   ├── Navbar.jsx
│   │   │   └── auth_buttons
│   │   │       ├── AuthButtons.jsx
│   │   │       └── GoogleLoginButton.jsx
│   │   ├── context
│   │   │   ├── AuthContext.jsx
│   │   │   └── ThemeContext.jsx
│   │   ├── main.jsx
│   │   ├── pages
│   │   │   ├── Login.jsx
│   │   │   ├── Profile.jsx
│   │   │   └── Register.jsx
│   │   ├── services
│   │   │   └── api.js
│   │   └── styles
│   │       └── main.css
│   └── vite.config.js
LICENSE
README.md
```

---

## 🤝 Contribution

1. Fork the repository.
2. Clone your fork:

    ```bash
    git clone https://github.com/your-username/django-react-jollof.git
    ```

3. Create a branch:

    ```bash
    git checkout -b feature/your-feature
    ```

4. Make your changes and commit:

    ```bash
    git commit -m "Add your feature"
    ```

5. Push to your fork and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📣 Connect with Us

Feel free to open an issue on GitHub for bugs, feature requests, or questions.

If you find **Django-React-Jollof** helpful, please give the repository a ⭐ on [GitHub](https://github.com/sir-temi/django-react-jollof). Your support helps us grow and improve!

### 🌐 Useful Links

-   **Documentation**: [django-react-jollof Docs](https://github.com/sir-temi/django-react-jollof#readme)
-   **Changelog**: [Releases](https://github.com/sir-temi/django-react-jollof/releases)
-   **Bug Tracker**: [Issues](https://github.com/sir-temi/django-react-jollof/issues)

---

## Conclusion

With **Django-React-Jollof**, building a full-stack app has never been easier! 🍲 Let us know what you create!
