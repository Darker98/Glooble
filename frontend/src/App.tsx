import React, { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { SearchResults } from './components/SearchResults';
import { Pagination } from './components/Pagination';
import { NoResults } from './components/NoResults';
import { SpellingSuggestion } from './components/SpellingSuggestion';
import { Search, Sparkles } from 'lucide-react';
import type { SearchResult, SearchResponse } from './types/search';

const ITEMS_PER_PAGE = 14;

export default function App() {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [corrections, setCorrections] = useState<[string, string][]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');
  const [totalResults, setTotalResults] = useState(0);

  const fetchResults = async (query: string, page: number, useOriginal = false) => {
    try {
      console.log('Fetching results:', { query, page, useOriginal });
      
      const response = await fetch('http://127.0.0.1:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query: query.trim(),
          useOriginal,
          page_number: page,
          per_page: ITEMS_PER_PAGE
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: SearchResponse = await response.json();
      console.log('Response data:', data);
      return data;
    } catch (error) {
      console.error('Search error:', error);
      return null;
    }
  };

  const handleSearch = async (query: string, useOriginal = false) => {
    if (!query.trim()) {
      setResults([]);
      setCorrections([]);
      setHasSearched(false);
      setCurrentQuery('');
      setTotalResults(0);
      return;
    }

    setIsLoading(true);
    setHasSearched(true);
    setCurrentQuery(query);
    setCurrentPage(1);

    const data = await fetchResults(query, 1, useOriginal);
    
    if (data) {
      if (!useOriginal && data.corrections?.length) {
        setCorrections(data.corrections);
      } else {
        setCorrections([]);
      }

      setResults(data.results || []);
      setTotalResults(data.total_results || 0);
    } else {
      setResults([]);
      setCorrections([]);
      setTotalResults(0);
    }
    
    setIsLoading(false);
  };

  const handlePageChange = async (newPage: number) => {
    setIsLoading(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    const data = await fetchResults(currentQuery, newPage);
    
    if (data) {
      setResults(data.results || []);
      setCurrentPage(newPage);
    }
    
    setIsLoading(false);
  };

  const handleUpload = async (file: File) => {
    setIsLoading(true);
    try {
      console.log('Processing file:', file.name);
      const article = await validateArticleFile(file);
      
      console.log('Uploading article:', article);
      const success = await uploadArticle(article);
      
      if (success) {
        alert('Article uploaded successfully!');
      } else {
        throw new Error('Failed to upload article');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert(error instanceof Error ? error.message : 'Failed to process article');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUseOriginal = () => {
    if (currentQuery && corrections.length > 0) {
      handleSearch(currentQuery, true);
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0118] text-white overflow-hidden">
      <div className="fixed inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/30 via-blue-900/20 to-black animate-gradient" />
        <div className="absolute top-0 left-0 w-1/3 h-1/3 bg-purple-500/10 rounded-full blur-3xl animate-float" />
        <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-blue-500/10 rounded-full blur-3xl animate-float" />
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
          <SearchBar onSearch={handleSearch} isLoading={isLoading} />
          
          {!isLoading && corrections.length > 0 && (
            <SpellingSuggestion
              corrections={corrections}
              onUseOriginal={handleUseOriginal}
            />
          )}

          {!isLoading && hasSearched ? (
            results.length > 0 ? (
              <>
                <SearchResults results={results} totalResults={totalResults} />
                {totalResults > ITEMS_PER_PAGE && (
                  <Pagination
                    currentPage={currentPage}
                    totalPages={Math.ceil(totalResults / ITEMS_PER_PAGE)}
                    onPageChange={handlePageChange}
                  />
                )}
              </>
            ) : (
              <NoResults />
            )
          ) : null}
        </div>
      </div>
    </div>
  );
}