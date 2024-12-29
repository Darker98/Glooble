import type { SearchResult } from '../types/search';

export const validateArticle = (data: any): data is SearchResult => {
  return (
    typeof data.title === 'string' &&
    typeof data.text === 'string' &&
    typeof data.url === 'string' &&
    Array.isArray(data.tags) &&
    Array.isArray(data.authors)
  );
};

export const validateArticleFile = async (file: File): Promise<SearchResult> => {
  try {
    const text = await file.text();
    const data = JSON.parse(text);
    
    if (!validateArticle(data)) {
      throw new Error('Invalid article format');
    }
    
    return data;
  } catch (error) {
    throw new Error('Failed to parse article file');
  }
}; 