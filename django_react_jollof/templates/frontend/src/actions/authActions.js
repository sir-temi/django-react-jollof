import API from "../services/api";

/**
 * Log in the user and store the access token.
 * @param {string} username
 * @param {string} password
 * @param {Function} login Function to update the auth state.
 * @returns {Promise<Object>} Response data or error.
 */
export const login = async (username, password, login) => {
    try {
        const { data } = await API.post("login/", { username, password });
        const { access } = data;

        // Save token to localStorage
        localStorage.setItem("drjToken", access);

        // Call login function to update auth state
        login();

        return { success: true, message: "Login successful!" };
    } catch (error) {
        return { success: false, message: "Invalid credentials" };
    }
};

export const logout = async (logout) => {
    localStorage.removeItem("drjToken");
    logout();
};

/**
 * Register a new user.
 * @param {string} username
 * @param {string} email
 * @param {string} password
 * @returns {Promise<Object>} Response data or error.
 */
export const register = async (username, email, password) => {
    try {
        await API.post("register/", { username, email, password });
        return { success: true, message: "Registration successful!" };
    } catch (error) {
        console.log(error);
        return { success: false, message: "Error during registration" };
    }
};

/**
 * Fetch the user's profile.
 * @returns {Promise<Object>} User profile data or error.
 */
export const fetchProfile = async () => {
    try {
        const { data } = await API.get("profile/");
        return { success: true, profile: data };
    } catch (error) {
        return {
            success: false,
            message: "Error fetching profile. Please log in.",
        };
    }
};

/**
 * Fetch admin-only data.
 * @returns {Promise<Object>} Admin data or error.
 */
export const fetchAdminData = async () => {
    try {
        const { data } = await API.get("admin/");
        return {
            success: true,
            message: data.message,
            adminDetails: data.adminDetails,
        };
    } catch (error) {
        return { success: false, message: "Access denied. Admins only." };
    }
};
