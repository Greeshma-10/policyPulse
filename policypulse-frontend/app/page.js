// app/page.js
"use client";

import { useState } from "react";
import Navbar from "../components/navbar";

export default function Home() {
  const [state, setState] = useState("");
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        `http://localhost:5000/recommend?state=${state}&keyword=${keyword}`
      );
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error("Error fetching:", err);
    }
    setLoading(false);
  };

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-[#f8f4e5] text-[#1F2937] px-6 py-10">
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="text-4xl font-extrabold text-[#006f6a] mb-2">🇮🇳 PolicyPulse</h1>
          <p className="text-lg text-[#444] mb-10">
            Discover personalized government schemes tailored to your needs.
          </p>

          <div className="flex flex-col md:flex-row items-center gap-4 justify-center mb-10">
            <select
              value={state}
              onChange={(e) => setState(e.target.value)}
              className="w-full md:w-1/4 px-4 py-2 border border-[#ccc] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#006f6a]"
            >
              <option value="">Select State</option>
              <option value="Karnataka">Karnataka</option>
              <option value="Andhra Pradesh">Andhra Pradesh</option>
              <option value="Maharashtra">Maharashtra</option>
              <option value="Tamil Nadu">Tamil Nadu</option>
              <option value="Kerala">Kerala</option>
            </select>

            <input
              type="text"
              placeholder="Enter your interest (e.g. education, farmer)"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              className="w-full md:w-1/3 px-4 py-2 border border-[#ccc] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#006f6a]"
            />

            <button
              onClick={handleSearch}
              className="bg-[#006f6a] hover:bg-[#00524f] text-white px-6 py-2 rounded-lg shadow-md transition"
            >
              🔍 Search
            </button>
          </div>

          {loading && <p className="text-center text-[#006f6a]">Loading results...</p>}

          <div className="grid gap-6 md:grid-cols-2">
            {results.map((item, index) => (
              <div
                key={index}
                className="bg-[#d5f5e3] rounded-xl shadow-md p-6 border border-[#aad9cd] hover:shadow-xl transition duration-300 text-left"
              >
                <h3 className="text-xl font-bold text-[#006f6a] mb-2">
                  📌 {item["Scheme Name"]?.slice(0, 80)}
                  {item["Scheme Name"]?.length > 80 ? "..." : ""}
                </h3>
                <p className="text-sm text-gray-600 mb-1">
                  📍 <span className="font-semibold">State:</span> {item.State}
                </p>
                <p className="text-sm text-gray-700 mb-2">
                  🧾 <span className="font-medium">Eligibility:</span> {item.Eligibility || "Not specified"}
                </p>
                <p className="text-sm text-gray-700">
                  🎁 <span className="font-medium">Benefit:</span> {item.Benefit || "Not specified"}
                </p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </>
  );
}
