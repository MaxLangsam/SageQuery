import React, { useState } from "react";

export default function FeedbackForm({ query, sql, onSubmit }) {
  const [feedback, setFeedback] = useState("");
  const [correct, setCorrect] = useState(true);

  const handleSubmit = async e => {
    e.preventDefault();
    await onSubmit({ question: query, sql, feedback, correct });
    setFeedback("");
  };

  return (
    <form className="bg-white rounded shadow p-4 mt-4" onSubmit={handleSubmit}>
      <h2 className="font-semibold mb-2">Feedback</h2>
      <div className="flex items-center gap-2 mb-2">
        <label>
          <input
            type="checkbox"
            checked={correct}
            onChange={e => setCorrect(e.target.checked)}
          />{" "}
          SQL is correct
        </label>
      </div>
      <textarea
        className="w-full border rounded p-2 mb-2"
        placeholder="Additional feedback (optional)..."
        value={feedback}
        onChange={e => setFeedback(e.target.value)}
      />
      <button className="bg-green-600 text-white px-4 py-2 rounded" type="submit">
        Submit Feedback
      </button>
    </form>
  );
} 