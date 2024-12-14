import React from 'react';

const QueryResult = ({ result, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="w-full max-w-2xl p-6 bg-gray-50 rounded-lg animate-pulse">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-full max-w-2xl p-6 bg-red-50 rounded-lg text-red-600">
        Error: {error}
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="w-full max-w-2xl p-6 bg-white rounded-lg shadow-sm border border-gray-100">
      <h3 className="text-lg font-medium mb-2">Result:</h3>
      <div className="whitespace-pre-wrap">{result}</div>
    </div>
  );
};

export default QueryResult;