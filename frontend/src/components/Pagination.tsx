import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ currentPage, totalPages, onPageChange }: PaginationProps) {
  return (
    <div className="flex items-center justify-center space-x-2 mt-8">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 rounded-lg bg-gray-900/80 backdrop-blur-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-800/80 transition-colors duration-300"
      >
        <ChevronLeft size={20} className="text-purple-400" />
      </button>
      
      <div className="flex items-center space-x-2">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            className={`w-8 h-8 rounded-lg transition-colors duration-300 ${
              currentPage === page
                ? 'bg-purple-500/20 text-purple-400'
                : 'bg-gray-900/80 text-gray-400 hover:bg-gray-800/80'
            }`}
          >
            {page}
          </button>
        ))}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 rounded-lg bg-gray-900/80 backdrop-blur-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-800/80 transition-colors duration-300"
      >
        <ChevronRight size={20} className="text-purple-400" />
      </button>
    </div>
  );
} 