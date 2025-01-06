import React, { PropsWithChildren } from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

const ParagraphMedium: React.FC<PropsWithChildren> = ({ children }) => (
  <ErrorBoundary>
    <p className="text-xl font-medium">{children}</p>
  </ErrorBoundary>
);

export default ParagraphMedium;
