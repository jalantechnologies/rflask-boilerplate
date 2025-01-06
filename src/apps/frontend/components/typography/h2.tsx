import React, { PropsWithChildren } from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

const H2: React.FC<PropsWithChildren> = ({ children }) => (
  <ErrorBoundary>
    <h2 className="text-2xl font-bold text-black sm:text-title-xl2">
      {children}
    </h2>
  </ErrorBoundary>
);

export default H2;
