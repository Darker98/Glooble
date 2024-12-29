import React from 'react';
import { ExternalLink, Clock } from 'lucide-react';
import { ResultTitle } from './ResultTitle';
import { ResultTags } from './ResultTags';
import { ResultAuthors } from './ResultAuthors';
import type { SearchResult } from '../../types/search';

interface ResultCardProps {
  result: SearchResult;
  index?: number;
}

export function ResultCard({ result, index }: ResultCardProps) {
  if (!result || !result.url) {
    return null;
  }

  // Clean up text and add ellipsis
  const truncateText = (text: string, maxLength: number = 180) => {
    if (!text) return '';
    const cleanText = text.toString()
      .replace(/[\[\]'"]/g, '')
      .replace(/\\n/g, ' ')
      .trim();
    return cleanText.length > maxLength 
      ? `${cleanText.slice(0, maxLength)}...` 
      : cleanText;
  };

  // Clean up authors and tags
  const cleanAuthors = result.authors?.filter(author => author && author.trim() !== '')
    .map(author => author.replace(/[\[\]'"]/g, '').trim());
  const displayAuthors = cleanAuthors?.length ? cleanAuthors : ['Unknown'];

  const cleanTags = result.tags?.filter(tag => tag && tag.trim() !== '')
    .map(tag => tag.replace(/[\[\]'"]/g, '').trim());

  return (
    <article 
      className="group relative"
      style={{ 
        '--animation-delay': `${(index || 0) * 0.1}s` 
      } as React.CSSProperties}
    >
      {/* Background Glow */}
      <div 
        className="absolute -inset-1 bg-gradient-to-r from-purple-500/20 via-blue-500/20 to-purple-500/20 rounded-lg blur opacity-50 transition-opacity duration-300 group-hover:opacity-100" 
        aria-hidden="true"
      />

      {/* Content Container */}
      <div className="relative glass-effect p-4 rounded-lg transition-all duration-300 transform hover:scale-[1.01] hover:shadow-lg hover:shadow-purple-500/10">
        {/* Title */}
        <ResultTitle title={result.title} url={result.url} />

        {/* Text Preview with forced ellipsis */}
        <p className="text-sm text-gray-300 mb-2 line-clamp-2 after:content-['...']">
          {truncateText(result.text)}
        </p>
        
        {/* Metadata Row */}
        <div className="flex flex-wrap items-center gap-3 text-xs">
          <ResultTags tags={cleanTags} />
          <ResultAuthors authors={displayAuthors} />
          
          {/* URL with truncation */}
          <a
            href={result.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-purple-400 hover:text-blue-400 transition-colors duration-300 flex items-center gap-1 group"
            aria-label={`Visit ${result.title}`}
          >
            <span className="truncate max-w-[200px] group-hover:underline">
              {result.url}
            </span>
            <ExternalLink 
              size={10} 
              className="flex-shrink-0"
              aria-hidden="true"
            />
          </a>

          {/* Score if available */}
          {result.score !== undefined && (
            <span className="text-gray-400">
              Score: {result.score.toFixed(2)}
            </span>
          )}
        </div>
      </div>
    </article>
  );
} 