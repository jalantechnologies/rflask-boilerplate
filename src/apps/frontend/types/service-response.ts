import { AsyncError, AsyncResult } from './async-operation';
import { JsonObject } from './common-types';

export class ApiError implements AsyncError {
  code: string;
  httpStatusCode: number;
  message: string;

  constructor(json: JsonObject) {
    this.code = json.code as string;
    this.httpStatusCode = json.httpStatusCode as number;
    this.message = json.message as string;
  }
}

export class ApiResponse<T> implements AsyncResult<T> {
  data?: T;
  error?: ApiError;

  constructor(data?: T, error?: ApiError) {
    this.data = data;
    this.error = error;
  }
}
