import { useContext } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import { ThemeContext } from "./context/ThemeContext";

const App = () => {
    const { isDarkMode } = useContext(ThemeContext);

    return (
        <div className={isDarkMode ? "dark-theme" : ""}>
            <Router>
                <NavBar />
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/profile" element={<Profile />} />
                </Routes>
            </Router>
        </div>
    );
};

export default App;
