import React from 'react';
import { CheckCircle, XCircle } from 'lucide-react';

interface UploadConfirmationProps {
  success: boolean;
  onClose: () => void;
}

export function UploadConfirmation({ success, onClose }: UploadConfirmationProps) {
  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-gray-900/90 p-6 rounded-lg shadow-xl border border-purple-500/20 max-w-md w-full mx-4">
        <div className="flex items-center justify-center mb-4">
          {success ? (
            <CheckCircle className="w-12 h-12 text-green-400" />
          ) : (
            <XCircle className="w-12 h-12 text-red-400" />
          )}
        </div>
        <h3 className="text-xl font-semibold text-center mb-4">
          {success ? 'Article Uploaded Successfully' : 'Upload Failed'}
        </h3>
        <p className="text-gray-300 text-center mb-6">
          {success 
            ? 'Your article has been added to the search index.'
            : 'There was an error uploading your article. Please try again.'}
        </p>
        <button
          onClick={onClose}
          className="w-full py-2 px-4 bg-purple-500/20 hover:bg-purple-500/30 text-purple-400 rounded-lg transition-colors duration-300"
        >
          Close
        </button>
      </div>
    </div>
  );
} 