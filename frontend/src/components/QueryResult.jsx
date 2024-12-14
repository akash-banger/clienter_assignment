import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const QueryResult = ({ result, isLoading, error, model }) => {
  if (isLoading) {
    return (
      <div className="w-full max-w-2xl p-6 bg-gray-50 rounded-lg flex flex-col items-center justify-center">
        <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent border-solid rounded-full animate-spin"></div>
        <p className="mt-4 text-gray-600 text-sm">Processing your query...</p>
        <p className="mt-1 text-gray-400 text-xs">This might take a few moments. Hang tight!</p>
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