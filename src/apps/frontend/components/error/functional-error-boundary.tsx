import axios from 'axios';
import React from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import { JsonObject } from '../../types/common-types';

interface ErrorData extends JsonObject {
  'error-info': string;
  'error-message': string;
  'error-name': string;
}

const logErrorToServer = (
  error: Error,
  errorInfo: { componentStack: string },
): void => {
  const errorData: ErrorData = {
    'error-name': error.name,
    'error-message': error.message,
    'error-info': errorInfo.componentStack,
  };

  axios.post('http://127.0.0.1:8080/client_logs', errorData).catch((err) => {
    console.error('Error logging client logs:', err);
  });
};

const ErrorFallback = ({
  error,
  resetErrorBoundary,
}: {
  error: Error;
  resetErrorBoundary: () => void;
}) => (
  <div className="rounded border border-red-500 bg-red-100 p-4 text-red-800">
    <h2 className="text-lg font-bold">Something went wrong</h2>
    <p>{error.message}</p>
    <button
      className="mt-2 rounded bg-blue-500 px-4 py-2 text-white"
      onClick={resetErrorBoundary}
    >
      Try Again
    </button>
  </div>
);

const FunctionalErrorBoundary: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <ErrorBoundary FallbackComponent={ErrorFallback} onError={logErrorToServer}>
    {children}
  </ErrorBoundary>
);

export default FunctionalErrorBoundary;
