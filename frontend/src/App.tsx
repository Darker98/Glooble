import React, { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { SearchResults } from './components/SearchResults';
import { Search, Sparkles } from 'lucide-react';

// Keep the mock results as fallback
const mockResults = [
  {
    id: '1',
    title: 'Understanding React Hooks',
    description: 'A comprehensive guide to React Hooks and their usage in modern web development.',
    url: 'https://example.com/article1',
  },
  {
    id: '2',
    title: 'The Future of Web Development',
    description: 'Exploring upcoming trends and technologies in web development for 2024 and beyond.',
    url: 'https://example.com/article2',
  },
];

export default function App() {
  const [results, setResults] = useState<string[]>([]);

  const handleSearch = async (query: string) => {
    // Validate that query is not empty or just whitespace
    if (!query || query.trim() === '') {
      console.log('Please enter a search query');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data.urls || []);
    } catch (error) {
      console.error('Error:', error);
      setResults([]); 
    }
  };

  const handleUpload = async (file: File) => {
    console.log('Uploading file:', file.name);
  };

  return (
    <div className="min-h-screen bg-[#0A0118] text-white overflow-hidden">
      {/* Animated background elements */}
      <div className="fixed inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/30 via-blue-900/20 to-black animate-gradient" />
        <div className="absolute top-0 left-0 w-1/3 h-1/3 bg-purple-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '0s' }} />
        <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-blue-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '-3s' }} />
      </div>
      
      {/* Content */}
      <div className="relative z-10 container mx-auto px-4 py-16">
        {/* Logo */}
        <div className="flex flex-col items-center mb-16 animate-float">
          <div className="flex items-center mb-6 relative">
            <div className="absolute -inset-4 bg-gradient-to-r from-purple-500/20 to-blue-500/20 rounded-full blur animate-glow" />
            <Search size={48} className="text-purple-400 mr-3" />
            <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
              Glooble
            </h1>
          </div>
        </div>

        {/* Search Interface */}
        <div className="flex flex-col items-center space-y-8 max-w-5xl mx-auto">
          <SearchBar onSearch={handleSearch} onUpload={handleUpload} />
          <SearchResults results={results} />
        </div>
      </div>
    </div>
  );
}