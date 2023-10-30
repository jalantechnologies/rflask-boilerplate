interface CleanupFunc {
  (): Promise<void>;
}

interface SetupFunc {
  <T>(): Promise<T>;
}

export interface Scenario {
  cleanup: CleanupFunc;

  setup: SetupFunc;
}

export interface Scenarios {
  [key: string]: Scenario;
}
