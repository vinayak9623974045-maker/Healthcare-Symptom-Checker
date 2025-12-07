import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

export default function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("history") || "[]");
    } catch {
      return [];
    }
  });

  const inputRef = useRef(null);

  useEffect(() => {
    localStorage.setItem("history", JSON.stringify(history));
  }, [history]);

  const submit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const resp = await axios.post(
        "http://127.0.0.1:8000/api/symptoms",
        { text },
        { headers: { "Content-Type": "application/json" } }
      );

      setResult(resp.data);
      setHistory((prev) =>
        [{ text, when: new Date().toISOString(), resp: resp.data }, ...prev].slice(0, 20)
      );
    } catch (err) {
      console.error(err);
      setResult({
        conditions: [
          {
            name: "Service unavailable",
            likelihood: 0,
            rationale: "Could not contact backend",
          },
        ],
        recommendations: [],
        disclaimer: ".",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f2f7fb] flex justify-center px-4 py-8">
      <div className="w-full max-w-6xl grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* LEFT PANEL — SYMPTOM INPUT */}
        <div className="md:col-span-1 bg-white rounded-2xl shadow-md p-6 border border-blue-50">
          <h1 className="text-2xl font-bold text-blue-700 mb-2">Symptom Checker</h1>
          <p className="text-gray-500 text-sm mb-4">
            Enter your symptoms below.
          </p>

          <form onSubmit={submit} className="space-y-4">
            <textarea
              ref={inputRef}
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="e.g., Fever, cough, sore throat..."
              className="w-full p-4 border border-blue-200 rounded-xl h-40 resize-none text-gray-700 focus:ring-2 focus:ring-blue-300"
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold shadow-md transition disabled:opacity-60"
            >
              {loading ? "Analyzing..." : "Analyze Symptoms"}
            </button>
          </form>

          {/* History */}
          <h2 className="mt-8 font-semibold text-blue-700">History</h2>
          <div className="mt-3 max-h-60 overflow-y-auto space-y-2">
            {history.length === 0 && (
              <p className="text-gray-500 text-sm">No history yet.</p>
            )}

            {history.map((h, i) => (
              <div
                key={i}
                onClick={() => {
                  setText(h.text);
                  setResult(h.resp);
                }}
                className="p-3 bg-blue-50 rounded-lg hover:bg-blue-100 cursor-pointer border border-blue-100"
              >
                <p className="font-medium text-blue-700">{h.text}</p>
                <p className="text-xs text-gray-500">{new Date(h.when).toLocaleString()}</p>
              </div>
            ))}
          </div>

          <button
            onClick={() => setHistory([])}
            className="mt-3 w-full py-2 border rounded-lg text-gray-600 hover:bg-gray-100"
          >
            Clear History
          </button>
        </div>

        {/* RIGHT PANEL — RESULTS */}
        <div className="md:col-span-2 bg-white rounded-2xl shadow-md p-6 border border-blue-50">
          <h2 className="text-xl font-bold text-blue-700 mb-4">Analysis Results</h2>

          {!result && (
            <p className="text-gray-400 text-center py-20">
              Results will appear here after analysis.
            </p>
          )}

          {result && (
            <div className="space-y-6">

              {/* Conditions */}
              <div>
                <h3 className="text-lg font-semibold text-blue-600">Possible Conditions</h3>
                <div className="mt-3 grid gap-4">
                  {result.conditions.map((c, index) => (
                    <div
                      key={index}
                      className="p-4 bg-blue-50 rounded-xl border border-blue-100 shadow-sm"
                    >
                      <div className="flex justify-between items-center">
                        <p className="text-blue-800 font-bold">{c.name}</p>
                        <span className="text-blue-600 font-semibold">
                          {Math.round(c.likelihood * 100)}%
                        </span>
                      </div>
                      <p className="text-gray-600 mt-1">{c.rationale}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div>
                <h3 className="text-lg font-semibold text-blue-600">Recommendations</h3>
                <ul className="list-disc ml-5 text-gray-700 space-y-1 mt-2">
                  {result.recommendations.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>

              {/* Disclaimer */}
              <p className="text-xs text-gray-500 mt-6 border-t pt-3">
                {result.disclaimer}
              </p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
