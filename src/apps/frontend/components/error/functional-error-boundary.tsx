import React from 'react';
import { ErrorBoundary } from 'react-error-boundary';

import datadogConfig from './datadog-config';
import sendLogs from './datadog-logger';

const logErrorToDatadog = (
  error: Error,
  errorInfo: { componentStack: string },
): void => {
  console.log(':  Error Sent  :', error, errorInfo);
  if (datadogConfig()?.key != undefined) {
    sendLogs(error, errorInfo);
  }
};

const ErrorFallback: React.FC<{
  error: Error;
  componentRef?: React.RefObject<HTMLElement>;
}> = ({ error, componentRef }) => {
  const width = componentRef?.current?.getBoundingClientRect().width || 'auto';
  const height =
    componentRef?.current?.getBoundingClientRect().height || 'auto';

  const isCriticalError = (message: string) =>
    ['critical', 'fatal', 'severe', 'system failure', 'crash'].some((keyword) =>
      message.toLowerCase().includes(keyword),
    );

  const isCritical = isCriticalError(error.message);
  return (
    <div
      className={`
        font-large rounded-lg border px-3 py-1 text-sm leading-snug transition
        ${isCritical ? 'border-red-500 bg-red-600 text-red-50' : 'border-red-500  bg-red-200 text-red-700'}
      `}
      style={{ width, height, whiteSpace: 'nowrap' }}
      role="alert"
    >
      <strong className="font-semibold">
        {isCritical ? 'Critical Error : ' : 'Error : '}
      </strong>
      <em>{error.message}</em>
    </div>
  );
};

const FunctionalErrorBoundary: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => (
  <ErrorBoundary FallbackComponent={ErrorFallback} onError={logErrorToDatadog}>
    {children}
  </ErrorBoundary>
);

export default FunctionalErrorBoundary;
