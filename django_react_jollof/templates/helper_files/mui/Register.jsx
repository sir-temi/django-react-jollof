// src/pages/Register.jsx

import { useState } from "react";
import { register } from "../actions/authActions";
import { useSnackbar } from "notistack";
import { Link, useNavigate } from "react-router-dom";
import AuthButtons from "../components/auth_buttons/AuthButtons";
import { useAuth } from "../context/AuthContext";
import LockIcon from "@mui/icons-material/Lock";
import PersonIcon from "@mui/icons-material/Person";
import EmailIcon from "@mui/icons-material/Email";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";

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
                        sx={{ marginY: 0 }}
                    />
                    <TextField
                        placeholder="Email"
                        type="text"
                        variant="outlined"
                        fullWidth
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        aria-label="Email"
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <EmailIcon />
                                </InputAdornment>
                            ),
                        }}
                        sx={{ marginY: 0 }}
                    />
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
                                    <PersonIcon />
                                </InputAdornment>
                            ),
                        }}
                        sx={{ marginY: 0 }}
                    />
                    <TextField
                        placeholder="Confirm Password"
                        type="password"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                        aria-label="Confirm Password"
                        InputProps={{
                            startAdornment: (
                                <InputAdornment position="start">
                                    <LockIcon />
                                </InputAdornment>
                            ),
                        }}
                        sx={{ marginY: 0 }}
                    />
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
