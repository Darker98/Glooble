import React, { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { SearchResults } from './components/SearchResults';
import { Pagination } from './components/Pagination';
import { NoResults } from './components/NoResults';
import { SpellingSuggestion } from './components/SpellingSuggestion';
import { Search, Sparkles } from 'lucide-react';
import type { SearchResult, SearchResponse, SearchState } from './types/search';

const RESULTS_PER_PAGE = 14;

export default function App() {
  const [state, setState] = useState<SearchState>({
    results: [],
    isLoading: false,
    error: null,
    hasSearched: false,
    currentQuery: '',
    corrections: [],
  });
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(state.results.length / RESULTS_PER_PAGE);
  const startIndex = (currentPage - 1) * RESULTS_PER_PAGE;
  const paginatedResults = state.results.slice(startIndex, startIndex + RESULTS_PER_PAGE);

  const handleSearch = async (query: string, useOriginal = false) => {
    console.log('Search initiated:', { query, useOriginal });

    if (!query.trim()) {
      setState(prev => ({
        ...prev,
        results: [],
        corrections: [],
        hasSearched: false,
        currentQuery: '',
        error: null,
      }));
      return;
    }

    setState(prev => ({
      ...prev,
      isLoading: true,
      hasSearched: true,
      currentQuery: query,
      error: null,
    }));

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

      const data: SearchResponse = await response.json();
      
      if (!response.ok && response.status !== 404) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setState(prev => ({
        ...prev,
        results: data.results || [],
        corrections: !useOriginal && data.corrections ? data.corrections : [],
        isLoading: false,
        error: null,
        hasSearched: true,
      }));
      
      setCurrentPage(1);
    } catch (error) {
      console.error('Search error:', error);
      setState(prev => ({
        ...prev,
        results: [],
        corrections: [],
        error: null,
        isLoading: false,
        hasSearched: true,
      }));
    } finally {
      console.log('Search completed');
    }
  };

  const handleUseOriginal = () => {
    if (state.currentQuery && state.corrections.length > 0) {
      console.log('Using original query:', state.currentQuery);
      handleSearch(state.currentQuery, true);
    }
  };

  const handleUpload = async (file: File) => {
    if (!file) return;
    
    setState(prev => ({
      ...prev,
      isLoading: true,
      error: null,
    }));
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      console.log('Uploading file:', file.name);
      // Add your file upload logic here
      
      setState(prev => ({
        ...prev,
        isLoading: false,
      }));
    } catch (error) {
      console.error('Upload error:', error);
      setState(prev => ({
        ...prev,
        error: 'Failed to upload file',
        isLoading: false,
      }));
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0118] text-white overflow-hidden">
      <div className="fixed inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/30 via-blue-900/20 to-black animate-gradient" />
        <div className="absolute top-0 left-0 w-1/3 h-1/3 bg-purple-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '0s' }} />
        <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-blue-500/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '-3s' }} />
      </div>
      
      <div className="relative z-10 container mx-auto px-4 py-16">
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

        <div className="flex flex-col items-center space-y-8 max-w-5xl mx-auto">
          <SearchBar 
            onSearch={handleSearch} 
            onUpload={handleUpload} 
            isLoading={state.isLoading} 
          />
          
          {state.error && (
            <div className="text-red-400 bg-red-500/10 px-4 py-2 rounded-lg">
              {state.error}
            </div>
          )}
          
          {!state.isLoading && state.corrections.length > 0 && (
            <SpellingSuggestion
              corrections={state.corrections}
              onUseOriginal={handleUseOriginal}
            />
          )}

          {!state.isLoading && state.hasSearched && state.results.length === 0 ? (
            <NoResults />
          ) : !state.isLoading && state.results.length > 0 ? (
            <>
              <SearchResults 
                results={paginatedResults}
                totalResults={state.results.length}
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