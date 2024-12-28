import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import { ThemeContext } from "../context/ThemeContext";
import { useAuth } from "../context/AuthContext";
import { logout as logoutUser } from "../actions/authActions";

const NavBar = () => {
    const { logout } = useAuth();
    const { isDarkMode, toggleTheme } = useContext(ThemeContext);
    const { isLoggedIn } = useAuth();

    return (
        <AppBar position="static" color={isDarkMode ? "default" : "primary"}>
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    <Link
                        to="/"
                        style={{
                            textDecoration: "none",
                            color: "inherit",
                        }}
                    >
                        Jesjay
                    </Link>
                </Typography>
                {!isLoggedIn && (
                    <>
                        <Button color="inherit" component={Link} to="/login">
                            Login
                        </Button>
                        <Button color="inherit" component={Link} to="/register">
                            Register
                        </Button>
                    </>
                )}
                {isLoggedIn && (
                    <>
                        <Button color="inherit" component={Link} to="/profile">
                            Profile
                        </Button>
                        <Button
                            color="inherit"
                            to="/login"
                            component={Link}
                            onClick={() => {
                                logoutUser(logout);
                            }}
                        >
                            Log Out
                        </Button>
                    </>
                )}
                <Button
                    variant="contained"
                    onClick={toggleTheme}
                    style={{
                        backgroundColor: isDarkMode ? "#fff" : "#000",
                        color: isDarkMode ? "#000" : "#fff",
                        marginLeft: "10px",
                    }}
                >
                    {isDarkMode ? "Light Mode" : "Dark Mode"}
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default NavBar;
