import { AccountProvider } from 'frontend/contexts';
import { AuthProvider } from 'frontend/contexts/auth.provider';
import { Config } from 'frontend/helpers';
import { AppRoutes } from 'frontend/routes';
import InspectLet from 'frontend/vendor/inspectlet';
import React, { useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { BrowserRouter as Router } from 'react-router-dom';

export default function App(): React.ReactElement {
  useEffect(() => {
    const inspectletKey = Config.getConfigValue('inspectletKey');

    if (inspectletKey) {
      InspectLet();
    }
  }, []);

  return (
    <AuthProvider>
      <AccountProvider>
        <Toaster />
        <Router>
          <AppRoutes />
        </Router>
      </AccountProvider>
    </AuthProvider>
  );
}
