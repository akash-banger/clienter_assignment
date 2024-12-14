import React, { useState } from 'react';
import QueryForm from './components/QueryForm';
import QueryResult from './components/QueryResult';

function App() {
  const [result, setResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [model, setModel] = useState('');

  const handleSubmit = async (query, model) => {
    setIsLoading(true);
    setError('');
    setModel(model);
    
    try {
      const endpoint = model === 'pandasai' ? '/query/pandasai' : '/query/ownmodel';
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: query }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch response');
      }

      const data = await response.json();
      setResult(data.result);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
            Sales Data Query Interface
          </h1>
          <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
            <QueryForm onSubmit={handleSubmit} />
          </div>
          <QueryResult 
            result={result}
            isLoading={isLoading}
            error={error}
            model={model}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
