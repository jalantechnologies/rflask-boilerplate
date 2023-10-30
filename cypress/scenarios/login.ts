import DataManagers from '../../test/data-managers';

import { Scenario } from './types';

const loginScenario: Scenario = {
  async cleanup() {
    await DataManagers.accounts.clear();
  },
  async setup<CreateAccountParams>() {
    const credentials = await DataManagers.accounts.seedOne();
    return credentials as unknown as CreateAccountParams;
  },
};

export default loginScenario;
