import { useState, useRef, useEffect } from "react";
import ChatMessage from "./components/ChatMessage";
import Sidebar from "./components/Sidebar";
import { useNavigate } from "react-router-dom";
import { sendMessage as apiSendMessage } from "./lib/apiClient";

const FILE_UPLOAD_URL = "http://localhost:8000/chat/upload";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [authToken, setAuthToken] = useState(() => localStorage.getItem("authToken"));
  const [userId, setUserId] = useState(() => localStorage.getItem("userId"));
  const [error, setError] = useState("");
  const chatContainerRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!authToken) {
      navigate("/auth");
    }
  }, [authToken, navigate]);

  const logout = async () => {
    localStorage.removeItem("authToken");
    localStorage.removeItem("userId");
    setAuthToken(null);
    setUserId(null);
    setMessages([]);
    setError("");
    navigate("/auth");
  };

  const sendMessage = async () => {
    const messageToSend = userInput.trim();
    if (!messageToSend) return;

    const localAuthToken = localStorage.getItem("authToken");
    if (!localAuthToken) {
      setError("You must be logged in to send messages.");
      logout();
      return;
    }

    const timestamp = new Date().toLocaleTimeString();
    const newMessages = [...messages, { sender: "user", message: messageToSend, timestamp }];
    setMessages(newMessages);
    setUserInput("");
    setLoading(true);
    setError("");

    try {
      const data = await apiSendMessage(messageToSend, localAuthToken);
      setMessages([...newMessages, { sender: "bot", message: data.response, timestamp }]);
    } catch (error) {
       console.error("Error sending message:", error);
       if (error.message.includes("401") || error.message.toLowerCase().includes("unauthorized")) {
            setError("Session expired. Please log in again.");
            logout();
       } else {
            setError(`Error sending message: ${error.message}`);
       }
    } finally {
      setLoading(false);
    }
  };

  const sendFile = async () => {
    if (!file) return;

    const localAuthToken = localStorage.getItem("authToken");
    if (!localAuthToken) {
        setError("You must be logged in to upload files.");
        logout();
        return;
    }

    const timestamp = new Date().toLocaleTimeString();
    const newMessages = [...messages, {
      sender: "user",
      message: `📎 Sending file: ${file.name}...`,
      timestamp,
    }];
    setMessages(newMessages);
    setFile(null);
    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(FILE_UPLOAD_URL, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${localAuthToken}`,
        },
        body: formData,
      });
      if (!res.ok) {
           const errorData = await res.json().catch(() => ({ detail: res.statusText }));
           throw new Error(errorData.detail || `HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      setMessages([...newMessages, {
        sender: "bot",
        message: data.response || "File uploaded successfully.",
        timestamp,
      }]);
    } catch (error) {
        console.error("Error uploading file:", error);
        if (error.message.includes("401") || error.message.toLowerCase().includes("unauthorized")) {
            setError("Session expired. Please log in again.");
            logout();
        } else {
            setError(`File upload failed: ${error.message}`);
        }
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !loading && authToken) sendMessage();
  };

  useEffect(() => {
    chatContainerRef.current?.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages]);

  if (!authToken) {
      return null;
  }

  return (
    <div className="flex h-screen bg-white">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <div className="w-full flex justify-between items-center p-4 border-b border-gray-200 bg-gray-50">
          <h1 className="text-xl font-semibold">Chat</h1>
          <div className="flex items-center gap-3">
            <button className="text-sm text-red-500 hover:underline" onClick={logout}>
              Logout
            </button>
          </div>
        </div>

        <div
          ref={chatContainerRef}
          className="flex-1 p-4 overflow-y-auto space-y-4"
        >
          {messages.map((msg, idx) => (
            <ChatMessage key={idx} {...msg} />
          ))}
          {loading && (
             <div className="flex justify-center">
                 <ChatMessage sender="bot" message="Typing..." isloading />
             </div>
           )}
            {error && <p className="text-red-500 text-center text-sm mt-2">{error}</p>}
        </div>

        <div className="p-4 border-t border-gray-200 bg-gray-50">
            <div className="flex gap-2 mb-2">
              <input
                type="text"
                className="flex-1 border rounded p-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
                placeholder={authToken ? "Type your message..." : "Please sign in to chat"}
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyDown={handleKeyPress}
                disabled={!authToken || loading}
              />
              <button
                className="bg-blue-600 text-white px-4 py-2 rounded font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={sendMessage}
                disabled={!authToken || loading || !userInput.trim()}
              >
                Send
              </button>
            </div>
            <div className="flex gap-2 items-center text-sm">
              <label className="flex items-center gap-2 cursor-pointer text-gray-600 hover:text-blue-600">
                 <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="m18.375 12.739-7.693 7.693a4.5 4.5 0 0 1-6.364-6.364l10.94-10.94A3 3 0 1 1 19.5 7.372L8.552 18.32m.009-.01-.01.01m5.699-9.941-7.81 7.81a1.5 1.5 0 0 0 2.122 2.122l7.81-7.81" />
                 </svg>
                 Attach File
                 <input
                    type="file"
                    className="hidden"
                    onChange={(e) => setFile(e.target.files[0])}
                    disabled={!authToken || loading}
                 />
              </label>
              {file && <span className="text-gray-500 truncate max-w-xs">{file.name}</span>}
              {file && (
                <button
                  className="bg-green-600 text-white px-3 py-1 rounded text-xs font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  onClick={sendFile}
                  disabled={!authToken || loading}
                >
                  Upload
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
  );
}
