import { useContext } from "react";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import Form from "react-bootstrap/Form";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { NavLink } from "react-router-dom";
import { ThemeContext } from "../context/ThemeContext";
import { useAuth } from "../context/AuthContext";
import { logout as logoutUser } from "../actions/authActions";
import { faMoon, faSun } from "@fortawesome/free-solid-svg-icons";

const NavBar = () => {
    const { logout } = useAuth();
    const { isDarkMode, toggleTheme } = useContext(ThemeContext);
    const { isLoggedIn } = useAuth();

    return (
        <Navbar
            expand="lg"
            className="px-5 py-3"
            bg={isDarkMode ? "dark" : "light"}
            data-bs-theme={isDarkMode ? "dark" : "light"}
            sticky="top"
        >
            <Navbar.Brand>
                <NavLink to="/" className="text-decoration-none">
                    Jesjay
                </NavLink>
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ms-auto">
                    {!isLoggedIn && (
                        <>
                            <NavLink to="/login" className="nav-link">
                                Login
                            </NavLink>
                            <NavLink to="/register" className="nav-link">
                                Register
                            </NavLink>
                        </>
                    )}
                    {isLoggedIn && (
                        <>
                            <NavLink to="/profile" className="nav-link">
                                Profile
                            </NavLink>
                            <NavLink
                                to="/login"
                                className="nav-link"
                                onClick={() => {
                                    logoutUser(logout);
                                }}
                            >
                                Log Out
                            </NavLink>
                        </>
                    )}
                    <div className="d-flex align-items-center">
                        <Form.Check
                            type="switch"
                            id="theme-switch"
                            label={
                                <FontAwesomeIcon
                                    icon={isDarkMode ? faMoon : faSun}
                                />
                            }
                            checked={isDarkMode}
                            onChange={toggleTheme}
                            className="mb-0 ms-3"
                            style={{ cursor: "pointer" }}
                            aria-label="Toggle dark and light mode"
                        />
                    </div>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default NavBar;
