// frontend/src/pages/AuthPage.jsx
import { useState } from "react";
// REMOVED: import { supabase } from "../supabaseClient";
import { useNavigate } from "react-router-dom";
import { apiSignIn, apiSignUp } from "../lib/apiClient"; // NEW Import

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState(""); // Only for signup
  const [loading, setLoading] = useState(false); // NEW Loading state
  const [message, setMessage] = useState(""); // NEW Message state for success/info
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setMessage(""); // Clear previous messages
    setLoading(true); // Set loading true

    // Basic frontend validation (optional, backend validates too)
    if (!email || !password || (!isLogin && !fullName)) {
      setError("Please fill in all required fields.");
      setLoading(false);
      return;
    }

    try {
      if (isLogin) {
        // Call backend API for signin
        const data = await apiSignIn(email, password);
        console.log("Sign in successful:", data);
        // Store the token (e.g., in localStorage)
        // IMPORTANT: Consider more secure storage (HttpOnly cookies managed by backend is best)
        if (data.access_token) {
            localStorage.setItem("authToken", data.access_token);
            localStorage.setItem("userId", data.user_id);
            // Optionally store refresh token if implementing token refresh
            // localStorage.setItem("refreshToken", data.refresh_token);
            navigate("/"); // Navigate to chat page or dashboard
        } else {
             throw new Error("Sign in response did not include access token.");
        }
      } else {
        // Call backend API for signup
        const data = await apiSignUp(email, password, fullName);
        console.log("Sign up successful:", data);
        // Display success message (e.g., check email for verification)
        setMessage(data.message || "Signup successful! Check your email for verification.");
        // Optionally switch to login view or clear form
        setIsLogin(true); // Switch to login view after successful signup
        setEmail(""); // Clear form
        setPassword("");
        setFullName("");
      }
    } catch (err) {
      console.error("Auth Error:", err);
      // Display error message from backend or a generic one
      setError(err.message || "An error occurred. Please try again.");
    } finally {
      setLoading(false); // Set loading false
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gray-100">
      <h2 className="text-2xl font-bold mb-4">{isLogin ? "Login" : "Sign Up"}</h2>
      <form onSubmit={handleSubmit} className="w-full max-w-sm bg-white p-6 rounded shadow space-y-4">
        {!isLogin && (
          <input
            type="text"
            placeholder="Full Name"
            className="w-full border p-2 rounded"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            disabled={loading} // Disable during loading
          />
        )}
        <input
          type="email"
          placeholder="Email"
          className="w-full border p-2 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={loading} // Disable during loading
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full border p-2 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={loading} // Disable during loading
        />
        {/* Display Messages/Errors */}
        {message && <p className="text-green-500">{message}</p>}
        {error && <p className="text-red-500">{error}</p>}
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:opacity-50" disabled={loading}>
          {loading ? "Processing..." : (isLogin ? "Login" : "Create Account")}
        </button>
      </form>
      <button
        onClick={() => { setIsLogin(!isLogin); setError(""); setMessage(""); }} // Clear errors/messages on switch
        className="mt-4 text-blue-600 underline"
        disabled={loading} // Disable during loading
      >
        {isLogin ? "Need an account? Sign up" : "Have an account? Login"}
      </button>
    </div>
  );
}
