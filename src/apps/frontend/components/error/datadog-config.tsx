import { Config } from '../../helpers';

const datadogConfig = (): { app_name: string; key: string } | null => {
  const logTransports =
    Config.getConfigValue<string[]>('loggerTransports') ?? [];
  if (logTransports?.includes('datadog')) {
    const Key: string = Config.getConfigValue<string>('datadogClientKey') ?? '';
    const appName: string =
      Config.getConfigValue<string>('datadogAppName') ?? '';
    return { key: Key, app_name: appName + ':frontend' };
  }
  return null;
};

export default datadogConfig;
