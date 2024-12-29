import React, { useState, useRef } from 'react';
import { Search, Upload, Loader2, X } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  onUpload: (file: File) => void;
  isLoading?: boolean;
}

export function SearchBar({ onSearch, onUpload, isLoading }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.type === 'application/json') {
        onUpload(file);
      } else {
        alert('Please upload a JSON file');
      }
      e.target.value = '';
    }
  };

  const handleClear = () => {
    setQuery('');
    inputRef.current?.focus();
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full max-w-2xl mx-auto relative">
      <form 
        onSubmit={handleSubmit} 
        className="relative group"
        role="search"
      >
        <div 
          className={`
            absolute -inset-1 bg-gradient-to-r from-purple-500 via-blue-500 to-purple-500 
            rounded-full blur transition-all duration-500 group-hover:opacity-100 
            ${isFocused ? 'opacity-100' : 'opacity-50'}
          `} 
          aria-hidden="true"
        />
        <div className="relative flex items-center">
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Search the digital cosmos..."
            className="
              w-full px-6 py-4 pr-24 bg-gray-900/80 backdrop-blur-lg rounded-full 
              text-white placeholder-gray-400 focus:outline-none transition-all duration-300
              [&::-webkit-search-cancel-button]:hidden [&::-webkit-search-decoration]:hidden
            "
            disabled={isLoading}
            aria-label="Search input"
          />
          
          {query && !isLoading && (
            <button
              type="button"
              onClick={handleClear}
              className="
                absolute right-16 p-2 hover:bg-purple-500/20 rounded-full 
                transition-colors duration-300
              "
              aria-label="Clear search"
            >
              <X size={16} className="text-gray-400" />
            </button>
          )}

          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="
              absolute right-4 p-2 bg-purple-500/20 rounded-full 
              hover:bg-purple-500/40 transition-colors duration-300 
              disabled:opacity-50 disabled:cursor-not-allowed
            "
            aria-label={isLoading ? 'Searching...' : 'Search'}
          >
            {isLoading ? (
              <Loader2 size={20} className="text-purple-400 animate-spin" />
            ) : (
              <Search size={20} className="text-purple-400" />
            )}
          </button>
        </div>
      </form>

      <button
        onClick={handleUploadClick}
        className="
          absolute -right-12 top-1/2 -translate-y-1/2 group 
          cursor-pointer focus:outline-none focus:ring-2 
          focus:ring-purple-400 focus:ring-offset-2 
          focus:ring-offset-gray-900 rounded-full
        "
        aria-label="Upload JSON file"
      >
        <div 
          className="
            absolute -inset-1 bg-gradient-to-r from-purple-500/50 
            to-blue-500/50 rounded-full blur opacity-75 
            transition-opacity duration-300 group-hover:opacity-100
          " 
          aria-hidden="true"
        />
        <div className="
          relative p-2 bg-gray-900/80 backdrop-blur-lg rounded-full 
          hover:bg-gray-800/80 transition-colors duration-300
        ">
          <Upload size={16} className="text-purple-400" />
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept="application/json"
          onChange={handleFileUpload}
          className="hidden"
          aria-hidden="true"
        />
      </button>
    </div>
  );
}