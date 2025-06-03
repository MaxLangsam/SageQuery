import React from "react";

export default function QueryInput({ query, setQuery, onSubmit, loading }) {
  return (
    <form
      className="flex gap-2"
      onSubmit={e => {
        e.preventDefault();
        onSubmit(query, false);
      }}
    >
      <input
        className="flex-1 border rounded px-3 py-2"
        type="text"
        placeholder="Ask a question (e.g., List all users)..."
        value={query}
        onChange={e => setQuery(e.target.value)}
        disabled={loading}
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        type="submit"
        disabled={loading || !query}
      >
        {loading ? "Loading..." : "Run"}
      </button>
      <button
        className="bg-gray-300 px-3 py-2 rounded"
        type="button"
        onClick={() => onSubmit(query, true)}
        disabled={loading || !query}
      >
        Preview SQL
      </button>
    </form>
  );
} 