import React, { createContext, useState, useEffect } from "react";
import { useSnackbar } from "notistack";

export const ThemeContext = createContext({
    isDarkMode: false,
    toggleTheme: () => {},
});

const ThemeProvider = ({ children }) => {
    const [isDarkMode, setIsDarkMode] = useState(false);
    const { enqueueSnackbar } = useSnackbar();

    useEffect(() => {
        // Check localStorage or default to system preference
        const savedTheme = localStorage.getItem("theme");
        if (savedTheme === "dark") {
            setIsDarkMode(true);
            document.body.classList.add("dark-theme");
        } else if (savedTheme === "light") {
            setIsDarkMode(false);
            document.body.classList.remove("dark-theme");
        } else {
            const prefersDark = window.matchMedia(
                "(prefers-color-scheme: dark)"
            ).matches;
            setIsDarkMode(prefersDark);
            document.body.classList.toggle("dark-theme", prefersDark);
        }
    }, []);

    const toggleTheme = () => {
        const newIsDarkMode = !isDarkMode;
        setIsDarkMode(newIsDarkMode);

        // Update the <body> class
        document.body.classList.toggle("dark-theme", newIsDarkMode);

        // Save preference in localStorage
        localStorage.setItem("theme", newIsDarkMode ? "dark" : "light");
    };

    return (
        <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

export default ThemeProvider;
