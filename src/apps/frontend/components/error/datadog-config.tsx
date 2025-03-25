import { Config } from '../../helpers';

const datadogConfig = (): { key: string; app_name: string } | undefined => {
  const logTransports = Config.getConfigValue<string[]>('logger.transports');
  if (logTransports?.includes('datadog')) {
    const Key: string =
      Config.getConfigValue<string>('datadog.client_key') ?? '';
    const appName: string =
      Config.getConfigValue<string>('datadog.app_name') ?? '';
    return { key: Key, app_name: appName };
  }
  return undefined;
};

export default datadogConfig;
