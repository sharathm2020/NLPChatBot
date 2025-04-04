import { useState, useRef, useEffect } from "react";
import ChatMessage from "./components/ChatMessage";

const API_URL = "http://127.0.0.1:8000/chat"; // Will be updated for Vercel
const FILE_UPLOAD_URL = "http://127.0.0.1:8000/chat/upload"; // Backend endpoint (stub for now)

export default function App() {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const chatContainerRef = useRef(null);

  const sendMessage = async () => {
    if (!userInput.trim()) return;
    const timestamp = new Date().toLocaleTimeString();
    const newMessages = [...messages, { sender: "user", message: userInput, timestamp }];
    setMessages(newMessages);
    setUserInput("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput })
      });
      const data = await res.json();
      setMessages([...newMessages, { sender: "bot", message: data.response, timestamp }]);
    } catch {
      setMessages([...newMessages, { sender: "bot", message: "Error contacting backend.", timestamp }]);
    } finally {
      setLoading(false);
    }
  };

  const sendFile = async () => {
    if (!file) return;
    const timestamp = new Date().toLocaleTimeString();
    const newMessages = [...messages, {
      sender: "user",
      message: `📎 Sent file: ${file.name}`,
      timestamp
    }];
    setMessages(newMessages);
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(FILE_UPLOAD_URL, {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      setMessages([...newMessages, {
        sender: "bot",
        message: data.response || "File received. (Processing TBD)",
        timestamp
      }]);
    } catch {
      setMessages([...newMessages, { sender: "bot", message: "File upload failed.", timestamp }]);
    } finally {
      setLoading(false);
      setFile(null);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  useEffect(() => {
    chatContainerRef.current?.scrollTo({
      top: chatContainerRef.current.scrollHeight,
      behavior: "smooth"
    });
  }, [messages]);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center p-4">
      <h1 className="text-2xl font-bold mb-4">🤖 NLP ChatBot</h1>
      <div ref={chatContainerRef} className="w-full max-w-2xl h-[500px] border p-4 overflow-y-auto rounded-lg shadow">
        {messages.map((msg, idx) => (
          <ChatMessage key={idx} {...msg} />
        ))}
        {loading && <ChatMessage sender="bot" message="Typing..." />}
      </div>

      {/* Input Area */}
      <div className="w-full max-w-2xl mt-4 flex flex-col gap-2">
        <div className="flex gap-2">
          <input
            type="text"
            className="flex-1 border rounded p-2"
            placeholder="Type your message..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            onKeyDown={handleKeyPress}
          />
          <button className="bg-blue-500 text-white px-4 rounded" onClick={sendMessage}>
            Send
          </button>
        </div>
        <div className="flex gap-2 items-center">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button
            className="bg-green-500 text-white px-3 py-1 rounded"
            onClick={sendFile}
            disabled={!file}
          >
            Upload File
          </button>
        </div>
      </div>
    </div>
  );
}
