// src/pages/Login.jsx
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUser, faLock } from "@fortawesome/free-solid-svg-icons";
import { login as loginApi } from "../actions/authActions";
import { useSnackbar } from "notistack";
import AuthButtons from "../components/auth_buttons/AuthButtons";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false); // Loading state
    const [errorMessage, setErrorMessage] = useState(""); // Error message state
    const { login } = useAuth();
    const { enqueueSnackbar } = useSnackbar();

    // Handle form submission
    const handleLogin = async (e) => {
        e.preventDefault();

        // Simple form validation
        if (!username || !password) {
            setErrorMessage("Please enter both username and password.");
            return;
        }

        setIsLoading(true); // Set loading state

        const result = await loginApi(username, password, login);

        setIsLoading(false); // Reset loading state

        // Handle login result
        if (result.success) {
            enqueueSnackbar(result.message, { variant: "success" });
            navigate("/profile");
        } else {
            enqueueSnackbar(result.message, { variant: "error" });
            setErrorMessage(result.message); // Display the error message
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2 className="login-title">Login</h2>
                <form onSubmit={handleLogin} className="login-form">
                    <div className="input-group">
                        <FontAwesomeIcon icon={faUser} className="input-icon" />
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            aria-label="Username"
                            required
                            className="login-input"
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
                            className="login-input"
                        />
                    </div>
                    {errorMessage && (
                        <p className="error-message">{errorMessage}</p>
                    )}{" "}
                    {/* Display error */}
                    <div className="button-group">
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="login-button"
                        >
                            {isLoading ? (
                                <div className="spinner"></div>
                            ) : (
                                "Login"
                            )}
                        </button>
                    </div>
                </form>
                <div className="divider">
                    <span>OR</span>
                </div>
                <AuthButtons />
            </div>
        </div>
    );
};

export default Login;
