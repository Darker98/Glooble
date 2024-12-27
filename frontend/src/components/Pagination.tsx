import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ currentPage, totalPages, onPageChange }: PaginationProps) {
  // Calculate the range of pages to display
  const pageRange = 10; // Number of surrounding pages to show
  const startPage = Math.max(1, currentPage - Math.floor(pageRange / 2));
  const endPage = Math.min(totalPages, startPage + pageRange - 1);

  // Adjust startPage if endPage reaches totalPages and there's space for more pages
  const adjustedStartPage = Math.max(1, endPage - pageRange + 1);

  return (
    <div className="flex items-center justify-center space-x-2 mt-8">
      {/* Prev Button */}
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 rounded-lg bg-gray-900/80 backdrop-blur-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-800/80 transition-colors duration-300"
      >
        <ChevronLeft size={20} className="text-purple-400" />
      </button>

      {/* Page Numbers */}
      <div className="flex items-center space-x-2">
        {adjustedStartPage > 1 && (
          <>
            <button
              onClick={() => onPageChange(1)}
              className={`w-8 h-8 rounded-lg transition-colors duration-300 ${
                currentPage === 1
                  ? 'bg-purple-500/20 text-purple-400'
                  : 'bg-gray-900/80 text-gray-400 hover:bg-gray-800/80'
              }`}
            >
              1
            </button>
            {adjustedStartPage > 2 && (
              <span className="text-gray-500">...</span>
            )}
          </>
        )}
        {Array.from({ length: endPage - adjustedStartPage + 1 }, (_, i) => adjustedStartPage + i).map((page) => (
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
        {endPage < totalPages && (
          <>
            {endPage < totalPages - 1 && (
              <span className="text-gray-500">...</span>
            )}
            <button
              onClick={() => onPageChange(totalPages)}
              className={`w-8 h-8 rounded-lg transition-colors duration-300 ${
                currentPage === totalPages
                  ? 'bg-purple-500/20 text-purple-400'
                  : 'bg-gray-900/80 text-gray-400 hover:bg-gray-800/80'
              }`}
            >
              {totalPages}
            </button>
          </>
        )}
      </div>

      {/* Next Button */}
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
