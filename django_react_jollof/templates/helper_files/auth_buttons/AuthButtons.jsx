import React, { Suspense, lazy } from "react";

// Dynamically import the login buttons based on socialLogin
const GoogleLoginButton = lazy(() => import("./GoogleLoginButton"));

const AuthButtons = () => {
    // Get socialLogin value from environment variables
    const socialLogin = import.meta.env.VITE_SOCIAL_LOGIN;

    return (
        socialLogin !== "none" && (
            <div className="auth-buttons">
                <h3>Or login with</h3>
                <Suspense fallback={<div>Loading...</div>}>
                    <GoogleLoginButton />
                </Suspense>
            </div>
        )
    );
};

export default AuthButtons;
