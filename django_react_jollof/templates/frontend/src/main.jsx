import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";
import "./styles/main.css";
import ReactDOM from "react-dom/client";
import { GoogleOAuthProvider } from "@react-oauth/google";
import App from "./App";
import ThemeProvider from "./context/ThemeContext";
import { SnackbarProvider } from "notistack";
import { AuthProvider } from "./context/AuthContext";

const googleClentId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

ReactDOM.createRoot(document.getElementById("root")).render(
    <SnackbarProvider
        maxSnack={3} // Maximum number of snackbars displayed at once
        anchorOrigin={{ vertical: "top", horizontal: "right" }} // Position of the notifications
    >
        <ThemeProvider>
            <AuthProvider>
                <GoogleOAuthProvider clientId={googleClentId}>
                    <App />
                </GoogleOAuthProvider>
            </AuthProvider>
        </ThemeProvider>
    </SnackbarProvider>
);
