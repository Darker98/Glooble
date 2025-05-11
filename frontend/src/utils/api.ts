import type { SearchResult } from '../types/search';

export const uploadArticle = async (article: SearchResult): Promise<boolean> => {
  try {
    const response = await fetch('/upload', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(article),
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data.success === true;
  } catch (error) {
    console.error('Upload error:', error);
    return false;
  }
};

export const searchArticles = async (query: string, page: number, perPage: number): Promise<Response> => {
  return fetch('/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      page,
      per_page: perPage
    }),
  });
}; 