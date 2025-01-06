import React, { PropsWithChildren } from 'react';

import VerticalStackLayout from '../layouts/vertical-stack-layout';
import ErrorBoundary from '../../error/ErrorBoundary';

interface FormControlProps {
  error: string;
  label: string;
}

const FormControl: React.FC<PropsWithChildren<FormControlProps>> = ({
  children,
  error,
  label,
}) => (
  <ErrorBoundary>
    <VerticalStackLayout gap={3}>
      <label className="block min-h-6 font-medium text-black dark:text-white">
        {label}
      </label>
      <div className="relative">{children}</div>
      {error && (
        <div className="flex items-center text-xs font-medium tracking-wide text-red-500">
          {error}
        </div>
      )}
    </VerticalStackLayout>
  </ErrorBoundary>
);

export default FormControl;
