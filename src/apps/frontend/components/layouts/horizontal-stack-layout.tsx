import React, { PropsWithChildren } from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

interface HorizontalStackLayoutProps {
  gap?: number;
}

const HorizontalStackLayout: React.FC<
  PropsWithChildren<HorizontalStackLayoutProps>
> = ({ children, gap = 0 }) => (
  <ErrorBoundary>
    <div className={`gap-${gap} flex items-center`}>{children}</div>
  </ErrorBoundary>
);

export default HorizontalStackLayout;
