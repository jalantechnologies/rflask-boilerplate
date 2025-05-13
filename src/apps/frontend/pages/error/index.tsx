import { Button } from 'frontend/components';
import { ButtonKind } from 'frontend/types/button';
import React from 'react';

type ErrorFallbackProps = {
  error: Error;
  resetError: () => void;
};

export const ErrorFallback: React.FC<ErrorFallbackProps> = ({ resetError }) => (
  <div data-testid="errorFallbackContainer" className="p-8 text-center">
    <h1 className="mb-4 text-2xl font-bold">Something went wrong.</h1>
    <p className="mb-6">We're sorry, but an unexpected error has occurred.</p>
    <Button onClick={resetError} kind={ButtonKind.PRIMARY}>
      Try Again
    </Button>
  </div>
);
