import { JsonObject } from './common-types';

export interface AsyncError {
  code: string;
  message: string;
}

export interface AsyncResult<T> {
  error?: AsyncError;
  data?: T;
}

export interface UseAsyncResponse<T> extends AsyncResult<T> {
  result: T;
  asyncCallback: (...args: unknown[]) => Promise<T>;
  isLoading: boolean;
}

export class AsyncOperationError implements AsyncError {
  code: string;
  message: string;

  constructor(json: JsonObject) {
    this.code = json.code as string;
    this.message = json.message as string;
  }
}
