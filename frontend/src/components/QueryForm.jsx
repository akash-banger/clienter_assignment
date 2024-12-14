import React, { useState } from 'react';

const QueryForm = ({ onSubmit }) => {
  const [query, setQuery] = useState('');
  const [model, setModel] = useState('ownmodel');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(query, model);
    setQuery('');
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl">
      <div className="mb-6">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query here..."
          className="w-full p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none h-32 transition-all duration-200 ease-in-out"
          required
        />
      </div>
      <div className="flex gap-4 mb-6">
        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className="px-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="pandasai">PandasAI</option>
          <option value="ownmodel">Own Model</option>
        </select>
        <button
          type="submit"
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200"
        >
          Submit Query
        </button>
      </div>
    </form>
  );
};

export default QueryForm;