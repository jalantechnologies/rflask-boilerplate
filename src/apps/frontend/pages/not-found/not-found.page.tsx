import React from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

export default function NotFound(): React.ReactElement {
  return (
    <ErrorBoundary>
      <div data-testid="notFoundContainer">Page Not Found</div>
    </ErrorBoundary>
  );
}
