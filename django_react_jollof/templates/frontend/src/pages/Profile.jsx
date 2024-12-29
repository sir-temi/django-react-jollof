// src/pages/Profile.jsx

import { useEffect, useState } from "react";
import { fetchProfile, logout as logoutApi } from "../actions/authActions";
import { useSnackbar } from "notistack";
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
    faUserCircle,
    faSignOutAlt,
    faEdit,
    faSpinner,
} from "@fortawesome/free-solid-svg-icons";
import AuthButtons from "../components/auth_buttons/AuthButtons";

const Profile = () => {
    const navigate = useNavigate();
    const { enqueueSnackbar } = useSnackbar();

    const [profile, setProfile] = useState({});
    const [isLoading, setIsLoading] = useState(true); // Loading state
    const [errorMessage, setErrorMessage] = useState(""); // Error message state

    useEffect(() => {
        const getProfile = async () => {
            try {
                const result = await fetchProfile(); // Ensure this is your real fetchProfile function
                if (result.success) {
                    setProfile(result.profile);
                } else {
                    // Show an error message with notistack
                    enqueueSnackbar(result.message, { variant: "error" });

                    // Redirect to the login page
                    navigate("/login");
                }
            } catch (error) {
                enqueueSnackbar("Failed to fetch profile. Please try again.", {
                    variant: "error",
                });
                setErrorMessage("Failed to fetch profile. Please try again.");
                navigate("/login");
            } finally {
                setIsLoading(false); // Reset loading state
            }
        };

        getProfile();
    }, [navigate, enqueueSnackbar]);

    /**
     * Handles editing profile (Optional).
     */
    const handleEditProfile = () => {
        // Implement navigation to edit profile page or open a modal
        navigate("/edit-profile"); // Ensure this route exists
    };

    if (isLoading) {
        return (
            <div className="profile-container">
                <div className="profile-card">
                    <FontAwesomeIcon
                        icon={faSpinner}
                        spin
                        size="3x"
                        className="spinner-icon"
                    />
                </div>
            </div>
        );
    }

    if (errorMessage) {
        return (
            <div className="profile-container">
                <div className="profile-card">
                    <p className="error-message">{errorMessage}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="profile-container">
            <div className="profile-card">
                {/* User Avatar */}
                <div className="avatar">
                    <FontAwesomeIcon icon={faUserCircle} size="6x" />
                </div>

                {/* User Information */}
                <div className="profile-info">
                    <h2 className="profile-name">{profile.username}</h2>
                    <p className="profile-email">
                        <strong>Email:</strong> {profile.email}
                    </p>
                    <p className="profile-role">
                        <strong>Role:</strong> {profile.role || "None"}
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Profile;
