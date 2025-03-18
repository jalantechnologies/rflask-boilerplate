import React from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import send_logs from './datadog-logger';

const logErrorToDatadog = (
  error: Error,
  errorInfo: { componentStack: string },
): void => {
  send_logs(error, errorInfo);
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
  <ErrorBoundary FallbackComponent={ErrorFallback} onError={logErrorToDatadog}>
    {children}
  </ErrorBoundary>
);

export default FunctionalErrorBoundary;
