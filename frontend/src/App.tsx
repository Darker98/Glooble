import React, { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { SearchResults } from './components/SearchResults';
import { Pagination } from './components/Pagination';
import { NoResults } from './components/NoResults';
import { SpellingSuggestion } from './components/SpellingSuggestion';
import { Search, Sparkles } from 'lucide-react';

const ITEMS_PER_PAGE = 10;

export default function App() {
  const [results, setResults] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [corrections, setCorrections] = useState<[string, string][]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');
  const [error, setError] = useState<string | null>(null);

  const totalPages = Math.ceil(results.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedResults = results.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  const handleSearch = async (query: string, useOriginal = false) => {
    if (!query.trim()) {
      setResults([]);
      setCorrections([]);
      setHasSearched(false);
      setCurrentQuery('');
      setError(null);
      return;
    }

    setIsLoading(true);
    setHasSearched(true);
    setCurrentQuery(query);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: query.trim(),
          useOriginal 
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('API Response:', data); // Debug log

      // Handle corrections first
      if (!useOriginal && data.corrections) {
        const newCorrections = Array.isArray(data.corrections) ? data.corrections : [];
        console.log('Setting corrections:', newCorrections);
        setCorrections(newCorrections);
      } else {
        setCorrections([]);
      }

      // Handle results
      const newResults = Array.isArray(data.urls) ? data.urls : [];
      console.log('Setting results:', newResults);
      setResults(newResults);
      setCurrentPage(1);
    } catch (error) {
      console.error('Error:', error);
      setError(error instanceof Error ? error.message : 'An error occurred');
      setResults([]);
      setCorrections([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUseOriginal = () => {
    if (currentQuery && corrections.length > 0) {
      console.log('Using original query:', currentQuery);
      handleSearch(currentQuery, true);
    }
  };

  const handleUpload = async (file: File) => {
    if (!file) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      console.log('Uploading file:', file.name);
      // Add your file upload logic here
    } catch (error) {
      console.error('Upload error:', error);
      setError('Failed to upload file');
    } finally {
      setIsLoading(false);
    }
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
        <div className="flex flex-col items-center mb-16 animate-float-gentle">
          <div className="flex items-center mb-6 relative">
            <div className="absolute -inset-4 bg-gradient-to-r from-purple-500/10 to-blue-500/10 rounded-full blur animate-glow" />
            <Search size={48} className="text-purple-400 mr-3" />
            <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400 bg-clip-text text-transparent">
              Glooble
            </h1>
          </div>
          <div className="flex items-center space-x-2 text-gray-400">
            <Sparkles size={16} className="text-purple-400" />
            <p className="text-lg">Discover knowledge through the digital cosmos</p>
            <Sparkles size={16} className="text-purple-400" />
          </div>
        </div>

        {/* Search Interface */}
        <div className="flex flex-col items-center space-y-8 max-w-5xl mx-auto">
          <SearchBar onSearch={handleSearch} onUpload={handleUpload} isLoading={isLoading} />
          
          {error && (
            <div className="text-red-400 bg-red-500/10 px-4 py-2 rounded-lg">
              {error}
            </div>
          )}
          
          {!isLoading && corrections.length > 0 && (
            <SpellingSuggestion
              corrections={corrections}
              onUseOriginal={handleUseOriginal}
            />
          )}

          {!isLoading && hasSearched && results.length === 0 ? (
            <NoResults />
          ) : !isLoading && results.length > 0 ? (
            <>
              <SearchResults 
                results={paginatedResults}
                totalResults={results.length}
              />
              {totalPages > 1 && (
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={setCurrentPage}
                />
              )}
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}