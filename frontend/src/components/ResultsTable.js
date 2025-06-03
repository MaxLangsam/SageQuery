import React from "react";

export default function ResultsTable({ results }) {
  if (!results || results.length === 0) return null;
  const columns = Object.keys(results[0]);
  return (
    <div className="overflow-x-auto bg-white rounded shadow p-4">
      <h2 className="font-semibold mb-2">Results</h2>
      <table className="min-w-full text-sm">
        <thead>
          <tr>
            {columns.map(col => (
              <th key={col} className="px-2 py-1 border-b">{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {results.map((row, i) => (
            <tr key={i}>
              {columns.map(col => (
                <td key={col} className="px-2 py-1 border-b">{row[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
} 