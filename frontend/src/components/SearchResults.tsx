import React from 'react';
import { ExternalLink } from 'lucide-react';

interface SearchResultsProps {
  results: string[]; // Now expecting an array of strings (URLs)
}

export function SearchResults({ results }: SearchResultsProps) {
  return (
    <div className="w-full max-w-4xl mt-8">
      <div className="space-y-4">
        {results.map((url, index) => (
          <div
            key={index}
            className="group relative"
          >
            <div className="relative glass-effect p-4 rounded-xl transition-all duration-300 hover:scale-[1.02]">
              <a
                href={url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-purple-400 hover:text-blue-400 transition-colors duration-300"
              >
                <ExternalLink size={16} className="opacity-75" />
                <span>{url}</span>
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}