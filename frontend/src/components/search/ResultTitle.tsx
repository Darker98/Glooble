import React from 'react';
import { ExternalLink } from 'lucide-react';

interface ResultTitleProps {
  title: string;
  url: string;
}

export function ResultTitle({ title, url }: ResultTitleProps) {
  // Clean up title if needed
  const displayTitle = title?.trim() || new URL(url).hostname;

  return (
    <h2 className="text-lg font-semibold mb-2">
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="group flex items-center gap-2 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400 hover:from-blue-400 hover:to-purple-400 transition-all duration-300"
        title={displayTitle}
      >
        <span className="line-clamp-1">
          {displayTitle}
        </span>
        <ExternalLink 
          size={14} 
          className="flex-shrink-0 opacity-50 group-hover:opacity-100 transition-opacity duration-300" 
          aria-hidden="true"
        />
      </a>
    </h2>
  );
} 