import React from 'react';
import { ErrorBoundary } from '../../error/ErrorBoundary';

export default function About(): React.ReactElement {
  return (
    <ErrorBoundary>
      <div>
        <img id="companyLogo" src="/assets/img/logo.jpg" />
      </div>
    </ErrorBoundary>
  );
}
