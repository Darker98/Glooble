import React from 'react';
import { AlertCircle } from 'lucide-react';

interface SpellingSuggestionProps {
  corrections: [string, string][]; // Array of tuples [original, corrected]
  onUseOriginal: () => void;
}

export function SpellingSuggestion({ corrections, onUseOriginal }: SpellingSuggestionProps) {
  if (!corrections.length) return null;

  return (
    <div className="mb-4 p-4 bg-gray-900/80 backdrop-blur-lg rounded-lg border border-purple-500/20">
      <div className="flex items-start space-x-3">
        <AlertCircle size={20} className="text-purple-400 mt-1 flex-shrink-0" />
        <div className="flex-1">
          <p className="text-gray-300">
            Showing results for{' '}
            {corrections.map(([original, corrected], index) => (
              <span key={original}>
                <span className="text-purple-400">{corrected}</span>
                {index < corrections.length - 1 ? ', ' : ''}
              </span>
            ))}
          </p>
          <button
            onClick={onUseOriginal}
            className="mt-2 text-sm text-gray-400 hover:text-purple-400 transition-colors duration-300"
          >
            Search instead for{' '}
            {corrections.map(([original], index) => (
              <span key={original}>
                <span className="font-semibold">{original}</span>
                {index < corrections.length - 1 ? ', ' : ''}
              </span>
            ))}
          </button>
        </div>
      </div>
    </div>
  );
} 