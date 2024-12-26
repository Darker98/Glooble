import React, { useState } from 'react';
import { Search, Upload } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  onUpload: (file: File) => void;
}

export function SearchBar({ onSearch, onUpload }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isFocused, setIsFocused] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query);
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file && file.type === 'application/json') {
      onUpload(file);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto relative">
      <form onSubmit={handleSubmit} className="relative group">
        <div className={`absolute -inset-1 bg-gradient-to-r from-purple-500 via-blue-500 to-purple-500 rounded-full blur transition-all duration-500 group-hover:opacity-100 ${isFocused ? 'opacity-100' : 'opacity-50'}`} />
        <div className="relative flex items-center">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder="Search the digital cosmos..."
            className="w-full px-6 py-4 bg-gray-900/80 backdrop-blur-lg rounded-full text-white placeholder-gray-400 focus:outline-none transition-all duration-300"
          />
          <button
            type="submit"
            className="absolute right-4 p-2 bg-purple-500/20 rounded-full hover:bg-purple-500/40 transition-colors duration-300"
          >
            <Search size={20} className="text-purple-400" />
          </button>
        </div>
      </form>

      <label className="absolute -right-16 top-1/2 -translate-y-1/2 group cursor-pointer">
        <div className="absolute -inset-1 bg-gradient-to-r from-purple-500/50 to-blue-500/50 rounded-full blur opacity-75 transition-opacity duration-300 group-hover:opacity-100" />
        <div className="relative p-3 bg-gray-900/80 backdrop-blur-lg rounded-full hover:bg-gray-800/80 transition-colors duration-300">
          <Upload size={18} className="text-purple-400" />
        </div>
        <input
          type="file"
          accept="application/json"
          onChange={handleFileUpload}
          className="hidden"
        />
      </label>
    </div>
  );
}