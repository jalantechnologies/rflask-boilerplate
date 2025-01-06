import React, { PropsWithChildren } from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

interface VerticalStackLayoutProps {
  gap?: number;
}

const VerticalStackLayout: React.FC<
  PropsWithChildren<VerticalStackLayoutProps>
> = ({ children, gap = 0 }) => (
  <ErrorBoundary>
    <div className={`gap-${gap} flex flex-col justify-center`}>{children}</div>
  </ErrorBoundary>
);

export default VerticalStackLayout;
