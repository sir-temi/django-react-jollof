// src/pages/Register.jsx

import React, { useState } from "react";
import { register } from "../actions/authActions";
import { useSnackbar } from "notistack";
import { Link, useNavigate } from "react-router-dom";
import AuthButtons from "../components/auth_buttons/AuthButtons";
import { useAuth } from "../context/AuthContext";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEnvelope, faLock, faUser } from "@fortawesome/free-solid-svg-icons";

const Register = () => {
    const navigate = useNavigate();
    const { enqueueSnackbar } = useSnackbar();
    const { login } = useAuth(); // If you need to log in the user immediately after registration

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false); // Loading state
    const [errorMessage, setErrorMessage] = useState(""); // Error message state

    // Handle form submission
    const handleRegister = async (e) => {
        e.preventDefault();

        // Basic form validation
        if (!username || !email || !password || !confirmPassword) {
            setErrorMessage("Please fill in all fields.");
            enqueueSnackbar("Please fill in all fields.", { variant: "error" });
            return;
        }

        if (password !== confirmPassword) {
            setErrorMessage("Passwords do not match.");
            enqueueSnackbar("Passwords do not match.", { variant: "error" });
            return;
        }

        if (password.length < 6) {
            setErrorMessage("Password must be at least 6 characters.");
            enqueueSnackbar("Password must be at least 6 characters.", {
                variant: "error",
            });
            return;
        }

        setIsLoading(true); // Set loading state

        try {
            const result = await register(username, email, password); // Ensure this is your real registration function
            enqueueSnackbar(result.message, {
                variant: result.success ? "success" : "error",
            });

            if (result.success) {
                navigate("/login"); // Redirect to login on success
            } else {
                setErrorMessage(result.message); // Display the error message
            }
        } catch (error) {
            enqueueSnackbar("An unexpected error occurred. Please try again.", {
                variant: "error",
            });
            setErrorMessage("An unexpected error occurred. Please try again.");
        } finally {
            setIsLoading(false); // Reset loading state
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h2 className="auth-title">Register</h2>
                <form onSubmit={handleRegister} className="auth-form">
                    <div className="input-group">
                        <FontAwesomeIcon icon={faUser} className="input-icon" />
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            aria-label="Username"
                            required
                            className="auth-input"
                        />
                    </div>
                    <div className="input-group">
                        <FontAwesomeIcon
                            icon={faEnvelope}
                            className="input-icon"
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            aria-label="Email"
                            required
                            className="auth-input"
                        />
                    </div>
                    <div className="input-group">
                        <FontAwesomeIcon icon={faLock} className="input-icon" />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            aria-label="Password"
                            required
                            className="auth-input"
                        />
                    </div>
                    <div className="input-group">
                        <FontAwesomeIcon icon={faLock} className="input-icon" />
                        <input
                            type="password"
                            placeholder="Confirm Password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            aria-label="Confirm Password"
                            required
                            className="auth-input"
                        />
                    </div>
                    {errorMessage && (
                        <p className="error-message">{errorMessage}</p>
                    )}
                    <div className="button-group">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="submit-button"
                        >
                            {isLoading ? (
                                <div className="spinner"></div>
                            ) : (
                                "Register"
                            )}
                        </button>
                    </div>
                </form>
                <div className="divider">
                    <span>OR</span>
                </div>
                <AuthButtons />
                <p className="redirect-text">
                    Already have an account? <Link to="/login">Login here</Link>
                </p>
            </div>
        </div>
    );
};

export default Register;
