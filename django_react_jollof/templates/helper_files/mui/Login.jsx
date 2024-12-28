// src/pages/Login.jsx
import { useState } from "react";
import PersonIcon from "@mui/icons-material/Person";
import LockIcon from "@mui/icons-material/Lock";
import { login as loginApi } from "../actions/authActions";
import { useSnackbar } from "notistack";
import AuthButtons from "../components/auth_buttons/AuthButtons";
import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";

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
                        <TextField
                            placeholder="Username"
                            type="text"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            aria-label="Username"
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <PersonIcon />
                                    </InputAdornment>
                                ),
                            }}
                        />
                    </div>
                    <div className="input-group">
                        <TextField
                            placeholder="Password"
                            type="password"
                            variant="outlined"
                            fullWidth
                            margin="normal"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            aria-label="Password"
                            InputProps={{
                                startAdornment: (
                                    <InputAdornment position="start">
                                        <LockIcon />
                                    </InputAdornment>
                                ),
                            }}
                            sx={{ marginTop: 0 }}
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
