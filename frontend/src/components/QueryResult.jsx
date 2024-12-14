import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const QueryResult = ({ result, isLoading, error, model }) => {
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
      {
        model === 'ownmodel' ? (
          <div className="prose max-w-none">
            {model === 'ownmodel' ? (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{result}</ReactMarkdown>
            ) : (
              result
            )}
          </div>
        ) : <><h3 className="text-lg font-medium mb-2">Result:</h3><div className="whitespace-pre-wrap">{result}</div></>
      }
    </div>
  );
};

export default QueryResult;