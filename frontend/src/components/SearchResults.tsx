import React from 'react';
import { Sparkle } from 'lucide-react';
import { ResultCard } from './search/ResultCard';
import type { SearchResult } from '../types/search';

interface SearchResultsProps {
  results: SearchResult[];
  totalResults: number;
}

export function SearchResults({ results, totalResults }: SearchResultsProps) {
  return (
    <div className="w-full max-w-5xl mt-3">
      <div className="flex items-center space-x-2 mb-3">
        <Sparkle 
          size={14} 
          className="text-purple-400 animate-pulse-gentle" 
          aria-hidden="true"
        />
        <p className="text-sm text-gray-400">
          Found{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400 font-semibold">
            {totalResults}
          </span>
          {' '}cosmic discoveries
        </p>
      </div>

      <div 
        className="space-y-2"
        role="feed"
        aria-label="Search results"
      >
        {results.map((result, index) => (
          <div
            key={`${result.url}-${index}`}
            className="animate-fade-in"
            style={{ 
              animationDelay: `${index * 0.03}s`,
              opacity: 1
            }}
          >
            <ResultCard 
              result={result} 
              index={index}
            />
          </div>
        ))}
      </div>
    </div>
  );
}