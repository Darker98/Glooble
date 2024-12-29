import React from 'react';
import { Users } from 'lucide-react';

interface ResultAuthorsProps {
  authors: string[];
}

export function ResultAuthors({ authors }: ResultAuthorsProps) {
  // Clean up authors and handle empty case
  const cleanAuthors = authors?.filter(author => author && author.trim() !== '')
    .map(author => author.replace(/[\[\]'"]/g, '').trim());

  const displayAuthors = cleanAuthors?.length ? cleanAuthors : ['Unknown'];

  return (
    <div className="flex items-center gap-1">
      <Users 
        size={12} 
        className="text-purple-400 flex-shrink-0" 
        aria-hidden="true"
      />
      <span 
        className="text-gray-400 line-clamp-1 text-xs"
        title={displayAuthors.join(', ')}
      >
        {displayAuthors.join(', ')}
      </span>
    </div>
  );
} 