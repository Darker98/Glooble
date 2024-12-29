import React from 'react';
import { SearchX } from 'lucide-react';

export function NoResults() {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      <SearchX size={48} className="text-purple-400 mb-4 opacity-50" />
      <h3 className="text-xl font-semibold text-gray-300 mb-2">No results found</h3>
      <p className="text-gray-400">
        Try adjusting your search terms or using different keywords
      </p>
    </div>
  );
} 