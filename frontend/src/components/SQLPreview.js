import React from "react";

export default function SQLPreview({ sql, examples }) {
  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="font-semibold mb-2">SQL Preview</h2>
      <pre className="bg-gray-100 p-2 rounded text-sm">{sql || "No SQL generated yet."}</pre>
      {examples && examples.length > 0 && (
        <div className="mt-2">
          <h3 className="font-medium">Grounded Examples:</h3>
          <ul className="list-disc ml-6">
            {examples.map((ex, i) => (
              <li key={i}>
                <span className="font-mono text-xs">{ex.question}</span>
                <br />
                <span className="text-xs text-gray-600">{ex.sql}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
} 