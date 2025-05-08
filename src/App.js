import React, { useState } from "react";
import "./index.css";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setResponse("");

    try {
      const res = await fetch("https://climate-backend.onrender.com/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ question: query }),
      });

      const data = await res.json();
      const llmReply = data.choices?.[0]?.message?.content || "No response from ClimateGPT.";
      setResponse(llmReply);
    } catch (error) {
      console.error("Error:", error);
      setResponse(" Failed to connect to ClimateGPT API.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative h-screen w-full overflow-hidden">
      {/* Background Image */}
      <img
        src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1950&q=80"
        alt="background"
        className="absolute top-0 left-0 w-full h-full object-cover"
      />

      <div className="absolute inset-0 bg-black bg-opacity-40 z-10" />

      <div className="relative z-20 flex flex-col items-center justify-center h-full px-4 text-white text-center">
        {/* Header */}
        <div className="absolute top-6 left-6 flex items-center space-x-2 text-black font-bold text-xl">
          <span>ClimateGPT 2.0</span>
          <span className="bg-green-500 text-white text-xs font-semibold px-2 py-1 rounded">BETA</span>
          <span className="text-sm font-light ml-2">by StormChasers</span>
        </div>

        <div className="absolute top-6 right-6 flex items-center space-x-6 text-black">
          <a href="#" className="hover:underline">Our Story</a>
          <a href="#" className="hover:underline">Your History</a>
          <div className="bg-teal-400 text-white font-semibold w-10 h-10 flex items-center justify-center rounded-full">AV</div>
        </div>

        {/* Title */}
        <h1 className="text-2xl md:text-3xl lg:text-4xl font-semibold mb-6 max-w-3xl">
          Enhance decision making with robust climate information for researchers, policymakers, and business leaders
        </h1>

        {/* Input Section */}
        <div className="flex w-full max-w-2xl items-center bg-white rounded-full overflow-hidden shadow-md">
          <input
            type="text"
            placeholder="Type a climate related question to start"
            className="flex-grow p-4 text-gray-800 outline-none"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            className="bg-green-500 text-white px-6 py-3 disabled:opacity-50"
            onClick={handleAsk}
            disabled={loading}
          >
            {loading ? "..." : "â–¶ï¸"}
          </button>
        </div>

        {/* Subtext */}
        <p className="mt-4 text-sm text-gray-200">
          or <span className="underline">see what others are asking</span>
        </p>
        <p className="text-xs mt-2 text-gray-400 max-w-md">
          ClimateGPT can make mistakes. Always double-check important information in its answers. <a className="underline" href="#">Learn more</a>
        </p>

        {/* Response Output */}
        {response && (
          <div className="bg-white text-black rounded-lg mt-6 p-4 max-w-xl shadow-lg">
            <p className="text-md font-medium">Response:</p>
            <p className="mt-1 whitespace-pre-line">{response}</p>
          </div>
        )}

        {/* Scroll Down Indicator */}
        <div className="absolute bottom-10 text-white text-sm flex flex-col items-center">
          <span className="animate-bounce text-xl">âŒ„</span>
          <span className="mt-1">scroll for more</span>
        </div>
      </div>
    </div>
  );
}

export default App;
