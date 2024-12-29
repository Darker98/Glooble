import React from 'react';
import { Tag } from 'lucide-react';

interface ResultTagsProps {
  tags: string[];
}

export function ResultTags({ tags }: ResultTagsProps) {
  // Filter out empty tags and clean up formatting
  const cleanTags = tags?.filter(tag => tag && tag.trim() !== '')
    .map(tag => tag.replace(/[\[\]'"]/g, '').trim());

  if (!cleanTags?.length) return null;

  return (
    <div className="flex items-center gap-1">
      <Tag 
        size={12} 
        className="text-purple-400 flex-shrink-0" 
        aria-hidden="true"
      />
      <div 
        className="flex flex-wrap gap-1"
        role="list"
        aria-label="Tags"
      >
        {cleanTags.map((tag, index) => (
          <span
            key={`${tag}-${index}`}
            className="px-1.5 py-0.5 text-xs rounded-full bg-purple-500/10 text-purple-400 hover:bg-purple-500/20 transition-colors duration-300"
            role="listitem"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
} 