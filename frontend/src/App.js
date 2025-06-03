import React, { useState } from "react";
import QueryInput from "./components/QueryInput";
import SQLPreview from "./components/SQLPreview";
import ResultsTable from "./components/ResultsTable";
import HistoryPanel from "./components/HistoryPanel";
import FeedbackForm from "./components/FeedbackForm";
import { sendQuery, sendFeedback } from "./services/api";

function App() {
  const [query, setQuery] = useState("");
  const [sql, setSQL] = useState("");
  const [results, setResults] = useState([]);
  const [history, setHistory] = useState([]);
  const [groundedExamples, setGroundedExamples] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleQuery = async (q, preview = false) => {
    setLoading(true);
    try {
      const response = await sendQuery(q, preview);
      setSQL(response.sql);
      setGroundedExamples(response.grounded_examples || []);
      if (!preview) setResults(response.results || []);
      setHistory([{ query: q, sql: response.sql, results: response.results }, ...history]);
    } catch (e) {
      alert("Error: " + e.message);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold mb-4">SageQuery</h1>
      <div className="w-full max-w-3xl space-y-4">
        <QueryInput
          query={query}
          setQuery={setQuery}
          onSubmit={handleQuery}
          loading={loading}
        />
        <SQLPreview sql={sql} examples={groundedExamples} />
        <ResultsTable results={results} />
        <FeedbackForm query={query} sql={sql} onSubmit={sendFeedback} />
        <HistoryPanel history={history} />
      </div>
    </div>
  );
}

export default App; 