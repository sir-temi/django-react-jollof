import React from "react";
import { GoogleLogin as OAuthGoogleLoginButton } from "@react-oauth/google";

const GoogleLoginButton = () => {
    const handleSuccess = (response) => {
        console.log("Google Login Success:", response);
        // Send the ID token to your backend
    };

    const handleError = (error) => {
        console.error("Google Login Failed:", error);
    };

    return (
        <OAuthGoogleLoginButton
            onSuccess={handleSuccess}
            onError={handleError}
        />
    );
};

export default GoogleLoginButton;
