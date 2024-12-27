import React from 'react';
import { ExternalLink, Sparkle } from 'lucide-react';

interface SearchResultsProps {
  results: string[]; // Array of URLs
  totalResults?: number; // Optional total count for pagination
}

export function SearchResults({ results, totalResults = results.length }: SearchResultsProps) {
  return (
    <div className="w-full max-w-4xl mt-8">
      <div className="flex items-center space-x-2 mb-8">
        <Sparkle size={16} className="text-purple-400 animate-pulse-gentle" />
        <p className="text-gray-400">
          Found{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400 font-semibold">
            {totalResults}
          </span>{' '}
          cosmic discoveries
        </p>
      </div>

      <div className="space-y-6">
        {results.map((url, index) => (
          <article
            key={index}
            className="group relative"
          >
            <div className="absolute -inset-1 bg-gradient-to-r from-purple-500/20 via-blue-500/20 to-purple-500/20 rounded-xl blur opacity-50 transition-opacity duration-300 group-hover:opacity-100" />
            <div className="relative glass-effect p-6 rounded-xl transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg hover:shadow-purple-500/10">
              <h2 className="text-xl font-semibold mb-3 truncate">
                <a
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400 hover:from-blue-400 hover:to-purple-400 transition-all duration-300"
                >
                  <span className="truncate">{url}</span>
                  <ExternalLink 
                    size={16} 
                    className="flex-shrink-0 opacity-50 group-hover:opacity-100 transition-opacity" 
                  />
                </a>
              </h2>
              <div className="mt-4 flex items-center space-x-2">
                <Sparkle 
                  size={14} 
                  className="text-purple-400 animate-pulse-gentle" 
                  style={{ animationDelay: `${index * 0.1}s` }} 
                />
                <a
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-purple-400 hover:text-blue-400 transition-colors duration-300"
                >
                  Visit site →
                </a>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}