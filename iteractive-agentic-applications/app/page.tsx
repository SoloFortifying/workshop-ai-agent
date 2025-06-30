'use client';

import cx from 'classnames';
import { useChat } from '@ai-sdk/react';
import { Weather } from './weather';
import { useState, useEffect } from 'react';

export default function Page() {
  const { messages, input, handleInputChange, handleSubmit, error } = useChat();
  const [isLoading, setIsLoading] = useState(false);

  // Handle loading state when submitting
  const handleFormSubmit = (e: React.FormEvent) => {
    setIsLoading(true);
    handleSubmit(e);
  };

  // Reset loading state when new message arrives
  useEffect(() => {
    if (messages.length > 0) {
      setIsLoading(false);
    }
  }, [messages.length]);

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4 shadow-md">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">Claude AI Chat</h1>
          {error && (
            <div className="text-red-400 text-sm">
              Error: {error.message || 'Something went wrong'}
            </div>
          )}
        </div>
      </header>

      {/* Main content */}
      <main className="flex-1 overflow-hidden">
        <div className="max-w-4xl mx-auto h-full flex flex-col p-4">
          {/* Messages container */}
          <div className="flex-1 overflow-y-auto space-y-6 mb-6 pr-2 custom-scrollbar">
            {messages.length === 0 ? (
              <div className="h-full flex items-center justify-center">
                <div className="text-center text-gray-500">
                  <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fillRule="evenodd" d="M10 2a8 8 0 100 16 8 8 0 000-16zm0 14a6 6 0 110-12 6 6 0 010 12zm-1-5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1zm0-4a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clipRule="evenodd"></path>
                  </svg>
                  <p className="text-lg">Start a conversation with Claude</p>
                  <p className="text-sm mt-2">Ask a question or try "What's the weather like?"</p>
                </div>
              </div>
            ) : (
              messages.map(message => (
                <div
                  key={message.id}
                  className={`p-4 rounded-lg shadow-md transition-all ${message.role === 'user' 
                    ? 'bg-blue-900/30 border border-blue-800/50 ml-12' 
                    : 'bg-gray-800/80 border border-gray-700/50 mr-12'}`}
                >
                  <div className="flex items-center mb-2">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${message.role === 'user' ? 'bg-blue-600' : 'bg-purple-600'} mr-2`}>
                      {message.role === 'user' ? 'U' : 'C'}
                    </div>
                    <p className="font-medium">
                      {message.role === 'user' ? 'You' : 'Claude 4'}
                    </p>
                  </div>
                  
                  <div className="space-y-3">
                    {message.parts.map((part, index) => {
                      if (part.type === 'text') {
                        return (
                          <div key={index} className="leading-relaxed">
                            {part.text}
                          </div>
                        );
                      }
                      
                      if (part.type === 'reasoning') {
                        return (
                          <pre
                            key={index}
                            className="bg-gray-900/70 p-3 rounded-md mt-2 text-xs overflow-x-auto border border-gray-700"
                          >
                            <details>
                              <summary className="cursor-pointer text-blue-400 hover:text-blue-300 transition-colors">
                                View reasoning
                              </summary>
                              <div className="mt-2 text-gray-300">
                                {part.details.map(detail =>
                                  detail.type === 'text' ? detail.text : '<redacted>',
                                )}
                              </div>
                            </details>
                          </pre>
                        );
                      }
                      
                      if (part.type === 'tool-invocation') {
                        const { toolInvocation } = part;
                        const { toolName, toolCallId, state } = toolInvocation;

                        if (state === 'call') {
                          const { args } = toolInvocation;

                          return (
                            <div
                              key={toolCallId}
                              className={cx({
                                'animate-pulse': ['getWeather'].includes(toolName),
                              })}
                            >
                              {toolName === 'getWeather' ? (
                                <div className="mt-2 p-2 bg-gray-800/50 rounded-md border border-gray-700">
                                  <div className="text-sm text-blue-400 mb-1">Fetching weather data...</div>
                                  <Weather />
                                </div>
                              ) : null}
                            </div>
                          );
                        }

                        if (state === 'result') {
                          const { result } = toolInvocation;

                          return (
                            <div key={toolCallId} className="mt-2 p-2 bg-gray-800/50 rounded-md border border-gray-700">
                              <div className="text-sm text-green-400 mb-1">Tool result: {toolName}</div>
                              {toolName === 'getWeather' ? (
                                <Weather weatherAtLocation={result} />
                              ) : (
                                <pre className="text-xs overflow-x-auto p-2 bg-gray-900/70 rounded-md">
                                  {JSON.stringify(result, null, 2)}
                                </pre>
                              )}
                            </div>
                          );
                        }
                      }              
                    })}
                  </div>
                </div>
              ))
            )}
          </div>
          
          {/* Input form */}
          <form onSubmit={handleFormSubmit} className="relative">
            <div className="flex gap-2 bg-gray-800 p-2 rounded-lg border border-gray-700 shadow-lg">
              <input
                name="prompt"
                value={input}
                onChange={handleInputChange}
                className="flex-1 p-3 bg-gray-800 text-gray-100 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                placeholder="Ask Claude 4 something..."
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className={`px-5 py-3 rounded-md font-medium transition-all ${isLoading || !input.trim() 
                  ? 'bg-gray-700 text-gray-400 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:opacity-90'}`}
              >
                {isLoading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing
                  </span>
                ) : 'Send'}
              </button>
            </div>
          </form>
        </div>
      </main>
      
      {/* Add custom scrollbar style */}
      <style jsx global>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(31, 41, 55, 0.5);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(75, 85, 99, 0.8);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(107, 114, 128, 0.8);
        }
        body {
          background-color: rgb(17, 24, 39);
        }
      `}</style>
    </div>
  );
}