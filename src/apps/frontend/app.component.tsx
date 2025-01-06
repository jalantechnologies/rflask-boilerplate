import React, { useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { BrowserRouter as Router } from 'react-router-dom';

import { AccountProvider } from './contexts';
import { AuthProvider } from './contexts/auth.provider';
import { Config } from './helpers';
import { AppRoutes } from './routes';
import InspectLet from './vendor/inspectlet';
import ErrorBoundary from './error/ErrorBoundary';

export default function App(): React.ReactElement {
  useEffect(() => {
    const inspectletKey = Config.getConfigValue('inspectletKey');

    if (inspectletKey) {
      InspectLet();
    }
  }, []);

  return (
    <ErrorBoundary>
      <AuthProvider>
        <ErrorBoundary>
          <AccountProvider>
            <ErrorBoundary>
              <Toaster />
            </ErrorBoundary>
            <ErrorBoundary>
              <Router>
                <ErrorBoundary>
                  <AppRoutes />
                </ErrorBoundary>
              </Router>
            </ErrorBoundary>
          </AccountProvider>
        </ErrorBoundary>
      </AuthProvider>
    </ErrorBoundary>
  );
}
