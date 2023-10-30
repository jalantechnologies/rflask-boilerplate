export {};

declare global {
  interface Window {
    Config: {
      env: string,
      inspectletKey: string,
    };
  }
}
