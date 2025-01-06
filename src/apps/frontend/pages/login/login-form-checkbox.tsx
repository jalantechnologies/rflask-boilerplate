import React from 'react';
import ErrorBoundary from '../../error/ErrorBoundary';

const LoginFormCheckbox: React.FC = () => (
  <ErrorBoundary>
    <div className="relative pt-0.5">
      <ErrorBoundary>
        <input
          type="checkbox"
          id="formCheckbox"
          className="taskCheckbox sr-only"
        />
      </ErrorBoundary>
      <ErrorBoundary>
        <div className="box mr-3 flex size-5 items-center justify-center rounded border border-stroke dark:border-form-strokedark dark:bg-form-input">
          <ErrorBoundary>
            <span className="opacity-0">
              <ErrorBoundary>
                <img
                  alt="checkbox tick mark icon"
                  className="size-3"
                  src="/assets/img/icon/form-checkbox-checkmark.svg"
                />
              </ErrorBoundary>
            </span>
          </ErrorBoundary>
        </div>
      </ErrorBoundary>
    </div>
  </ErrorBoundary>
);

export default LoginFormCheckbox;
