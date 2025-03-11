import React from 'react';
import axios from 'axios';
import { ErrorBoundary } from 'react-error-boundary';
import { JsonObject } from '../../types/common-types';

interface ErrorData extends JsonObject {
  'error-info': string;
  'error-message': string;
  'error-name': string;
}

const logErrorToServer = async (
  error: Error,
  errorInfo: { componentStack: string },
) => {
  const errorData: ErrorData = {
    'error-name': error.name,
    'error-message': error.message,
    'error-info': errorInfo.componentStack,
  };

  try {
    await axios.post('http://127.0.0.1:8080/client_logs', errorData);
  } catch (err) {
    console.error('Error logging client logs:', err);
  }
};

const ErrorFallback = ({
  error,
  resetErrorBoundary,
}: {
  error: Error;
  resetErrorBoundary: () => void;
}) => (
  <div className="p-4 border border-red-500 bg-red-100 text-red-800 rounded">
    <h2 className="font-bold text-lg">Something went wrong</h2>
    <p>{error.message}</p>
    <button
      className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
      onClick={resetErrorBoundary}
    >
      Try Again
    </button>
  </div>
);

const FunctionalErrorBoundary: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  return (
    <ErrorBoundary FallbackComponent={ErrorFallback} onError={logErrorToServer}>
      {children}
    </ErrorBoundary>
  );
};

export default FunctionalErrorBoundary;
