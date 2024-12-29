import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
});

// Request interceptor
API.interceptors.request.use(
    (config) => {
        // Check if the request is for an endpoint that doesn't require a token
        const noAuthEndpoints = ["register/", "login/"];
        const isNoAuthEndpoint = noAuthEndpoints.some((endpoint) =>
            config.url?.includes(endpoint)
        );

        // Skip attaching the token for these endpoints
        if (!isNoAuthEndpoint) {
            const token = localStorage.getItem("drjToken");
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }

        return config;
    },
    (error) => {
        // Handle request errors
        return Promise.reject(error);
    }
);

// Response interceptor
API.interceptors.response.use(
    (response) => response, // Pass successful responses
    (error) => {
        const status = error.response?.status;

        if (status === 401 || status === 403) {
            // Remove token from localStorage if it exists
            localStorage.removeItem("drjToken");

            // Redirect the user to the login page
            window.location.href = "/login"; // Update this if your login page is different
        }

        // Reject the error to handle it elsewhere if needed
        return Promise.reject(error);
    }
);

export default API;
