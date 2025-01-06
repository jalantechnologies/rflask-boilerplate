import React from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

const Spinner: React.FC = () => (
  <ErrorBoundary>
    <div
      className="
      inline-block
      size-6
      animate-spin
      rounded-full
      border-4
      border-solid
      border-current
      border-r-transparent
      align-[-0.125em]
      motion-reduce:animate-[spin_1.5s_linear_infinite]
    "
    ></div>
  </ErrorBoundary>
);

export default Spinner;
