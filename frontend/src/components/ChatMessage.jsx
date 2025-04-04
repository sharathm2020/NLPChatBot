import React from "react";

export default function ChatMessage({ message, sender, timestamp }) {
  return (
    <div
      className={`my-2 p-3 rounded-md max-w-[75%] break-words ${
        sender === "user"
          ? "bg-blue-100 ml-auto text-right"
          : "bg-gray-100 mr-auto text-left"
      }`}
    >
      <p className="text-sm">{message}</p>
      {timestamp && (
        <p className="text-xs text-gray-400 mt-1">
          {sender === "user" ? "You" : "Bot"} • {timestamp}
        </p>
      )}
    </div>
  );
}
