import React from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export function Pagination({ currentPage, totalPages, onPageChange }: PaginationProps) {
  // Show at most 7 page numbers, with ellipsis if needed
  const getPageNumbers = () => {
    if (totalPages <= 7) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    if (currentPage <= 3) {
      return [1, 2, 3, 4, '...', totalPages];
    }

    if (currentPage >= totalPages - 2) {
      return [1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages];
    }

    return [
      1,
      '...',
      currentPage - 1,
      currentPage,
      currentPage + 1,
      '...',
      totalPages,
    ];
  };

  const pageNumbers = getPageNumbers();

  return (
    <div className="flex items-center justify-center space-x-2 mt-8 mb-8 w-full overflow-x-auto px-4">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 rounded-lg bg-gray-900/80 backdrop-blur-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-800/80 transition-colors duration-300"
        aria-label="Previous page"
      >
        <ChevronLeft size={20} className="text-purple-400" />
      </button>
      
      <div className="flex items-center space-x-2">
        {pageNumbers.map((page, index) => (
          <React.Fragment key={index}>
            {typeof page === 'number' ? (
              <button
                onClick={() => onPageChange(page)}
                className={`min-w-[2rem] h-8 rounded-lg transition-colors duration-300 ${
                  currentPage === page
                    ? 'bg-purple-500/20 text-purple-400'
                    : 'bg-gray-900/80 text-gray-400 hover:bg-gray-800/80'
                }`}
                aria-label={`Page ${page}`}
                aria-current={currentPage === page ? 'page' : undefined}
              >
                {page}
              </button>
            ) : (
              <span className="text-gray-400 px-1" aria-hidden="true">
                •••
              </span>
            )}
          </React.Fragment>
        ))}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 rounded-lg bg-gray-900/80 backdrop-blur-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-800/80 transition-colors duration-300"
        aria-label="Next page"
      >
        <ChevronRight size={20} className="text-purple-400" />
      </button>
    </div>
  );
} 
