import React from "react";

export default function HistoryPanel({ history }) {
  if (!history || history.length === 0) return null;
  return (
    <div className="bg-white rounded shadow p-4 mt-4">
      <h2 className="font-semibold mb-2">Query History</h2>
      <ul className="space-y-2">
        {history.map((item, i) => (
          <li key={i} className="border-b pb-2">
            <div className="font-mono text-xs">{item.query}</div>
            <div className="text-xs text-gray-600">{item.sql}</div>
          </li>
        ))}
      </ul>
    </div>
  );
} 