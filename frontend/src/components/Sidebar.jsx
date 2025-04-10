import React, { useState, useEffect } from 'react';
import { getTodos, getChatHistory } from '../lib/apiClient';
import { CalendarDaysIcon, CheckCircleIcon, PlusIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'; // Using heroicons for icons

// Helper function to group chat history (implementation details TBD)
const groupChatHistory = (history) => {
    // For now, just return the history ungrouped
    // TODO: Implement grouping logic based on timestamps (week, month, older)
    if (!history || history.length === 0) return [];

    // Assuming history items have a timestamp field
    // Format timestamp for display
    return history.map(item => ({
        ...item,
        displayTimestamp: item.timestamp ? new Date(item.timestamp).toLocaleString() : 'No date'
    })).sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Sort newest first
};


export default function Sidebar() {
    const [todos, setTodos] = useState([]);
    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showTodos, setShowTodos] = useState(false);
    const [showHistory, setShowHistory] = useState(true); // Show history by default

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("authToken");
            if (!token) {
                setError("Not logged in"); // Should ideally not happen if sidebar is shown only when logged in
                return;
            }

            setIsLoading(true);
            setError(null);

            try {
                // Fetch in parallel
                const [todosData, historyData] = await Promise.all([
                    getTodos(token),
                    getChatHistory(token)
                ]);

                // Ensure todosData is an array
                setTodos(Array.isArray(todosData) ? todosData : []);

                // Process and set history
                const groupedHistory = groupChatHistory(historyData);
                setHistory(groupedHistory);

            } catch (err) {
                console.error("Failed to fetch sidebar data:", err);
                setError(err.message || "Failed to load data.");
                // Handle specific errors like 401 Unauthorized (token expired)
                if (err.message.includes('401')) {
                    // Consider triggering logout from here or notifying App.jsx
                    setError("Session expired. Please log in again.");
                    localStorage.removeItem('authToken');
                    localStorage.removeItem('userId');
                    // Force refresh or navigate might be needed depending on app structure
                    window.location.reload();
                }
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();

        // Optional: Set up polling or WebSocket for real-time updates

    }, []); // Fetch data on component mount

    // Placeholder function for creating a new chat
    const handleNewChat = () => {
        console.log("New Chat clicked - implement functionality");
        // Likely involves clearing current chat state in App.jsx
    };

    return (
        <div className="w-64 bg-gray-50 h-full flex flex-col border-r border-gray-200">
            {/* Header / New Chat Button */}
            <div className="p-4 border-b border-gray-200 flex justify-between items-center">
                <h2 className="font-semibold text-lg">History</h2>
                <button
                    onClick={handleNewChat}
                    className="p-1 text-gray-600 hover:text-gray-900 hover:bg-gray-200 rounded"
                    title="New Chat"
                >
                    <PlusIcon className="h-5 w-5" />
                </button>
            </div>

            {/* Navigation Icons/Buttons */}
            <div className="p-2 flex justify-around border-b border-gray-200 bg-white">
                <button
                    onClick={() => { setShowHistory(true); setShowTodos(false); }}
                    className={`p-2 rounded hover:bg-gray-100 ${showHistory ? 'text-blue-600' : 'text-gray-500'}`}
                    title="Chat History"
                >
                    <ChatBubbleLeftRightIcon className="h-6 w-6" />
                </button>
                <button
                    onClick={() => { setShowTodos(true); setShowHistory(false); }}
                    className={`p-2 rounded hover:bg-gray-100 ${showTodos ? 'text-blue-600' : 'text-gray-500'}`}
                    title="To-Do List"
                >
                    <CheckCircleIcon className="h-6 w-6" />
                </button>
            </div>

            {/* Content Area (History or Todos) */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {isLoading && <p className="text-gray-500">Loading...</p>}
                {error && <p className="text-red-500 text-sm">Error: {error}</p>}

                {!isLoading && !error && (
                    <>
                        {/* Chat History Section */}
                        {showHistory && (
                            <div className="space-y-2">
                                <h3 className="text-sm font-semibold text-gray-500 uppercase">Recent Chats</h3>
                                {history.length > 0 ? (
                                    history.map((chat, index) => (
                                        <div key={index} className="text-sm p-2 hover:bg-gray-100 rounded cursor-pointer group">
                                            <p className="truncate text-gray-700 group-hover:text-gray-900">{chat.user_message || 'Chat entry'}</p>
                                            <p className="text-xs text-gray-400">{chat.displayTimestamp}</p>
                                            {/* TODO: Add onClick to load this chat */}
                                        </div>
                                    ))
                                ) : (
                                    <p className="text-sm text-gray-400">No chat history found.</p>
                                )}
                                {/* TODO: Add grouping headers (This Week, Last Month, etc.) */}
                            </div>
                        )}

                        {/* Todos Section */}
                        {showTodos && (
                            <div className="space-y-2">
                                 <h3 className="text-sm font-semibold text-gray-500 uppercase">To-Do List</h3>
                                {todos.length > 0 ? (
                                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
                                        {todos.map((todo, index) => (
                                            <li key={index}>{todo}</li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p className="text-sm text-gray-400">Your to-do list is empty.</p>
                                )}
                            </div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
} 