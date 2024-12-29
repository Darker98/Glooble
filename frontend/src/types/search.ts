export interface SearchResult {
  url: string;
  title: string;
  text: string;
  tags: string[];
  authors: string[];
}

export interface SearchResponse {
  results: SearchResult[];
  corrections?: [string, string][];
  total_results: number;
}

export interface SearchRequest {
  query: string;
  useOriginal?: boolean;
  page?: number;
  pageSize?: number;
  filters?: {
    tags?: string[];
    authors?: string[];
    dateRange?: {
      start: string;
      end: string;
    };
  };
}

export interface PaginatedResults<T> {
  items: T[];
  total: number;
  page: number;
  totalPages: number;
}

export interface SearchState {
  results: SearchResult[];
  isLoading: boolean;
  error: string | null;
  hasSearched: boolean;
  currentQuery: string;
  corrections: [string, string][];
  metadata?: SearchResponse['metadata'];
} 