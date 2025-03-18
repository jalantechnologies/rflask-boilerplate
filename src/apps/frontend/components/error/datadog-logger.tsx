import { datadogLogs } from '@datadog/browser-logs';
import '@datadog/browser-logs/bundle/datadog-logs';
import { ErrorInfo } from 'react';

datadogLogs.init({
  clientToken: '<CLIENT_TOKEN>',
  site: 'us5.datadoghq.com',
  forwardErrorsToLogs: true,
  sessionSampleRate: 100,
});

const sendLogs = (error: Error, errorInfo: ErrorInfo) => {
  datadogLogs.logger.error(error.message, {
    'error-info': errorInfo.componentStack,
    error: error.name,
  });
};

export default sendLogs;
