
# Set by django-react-jollof

import os

INSTALLED_APPS += [
    "corsheaders",
    "rest_framework",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # React frontend
]

# Set by django-react-jollof

import os

INSTALLED_APPS += [
    "corsheaders",
    "rest_framework",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # React frontend
]

# Set by django-react-jollof

import os

INSTALLED_APPS += [
    "corsheaders",
    "rest_framework",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # React frontend
]

# Set by django-react-jollof

import os

INSTALLED_APPS += [
    "corsheaders",
    "rest_framework",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # React frontend
]
