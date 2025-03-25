import { datadogLogs } from '@datadog/browser-logs';
import '@datadog/browser-logs/bundle/datadog-logs';
import { ErrorInfo } from 'react';

import datadogConfig from './datadog-config';

datadogLogs.init({
  clientToken: datadogConfig()?.key ?? '',
  site: 'us5.datadoghq.com',
  forwardErrorsToLogs: true,
  sessionSampleRate: 100,
  service: datadogConfig()?.app_name ?? '',
});

const sendLogs = (error: Error, errorInfo: ErrorInfo) => {
  datadogLogs.logger.error(error.message, {
    'error-info': errorInfo.componentStack,
    error: error.name,
  });
};

export default sendLogs;
