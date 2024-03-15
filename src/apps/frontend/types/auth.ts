import { JsonObject } from './common-types';

export class AccessToken {
  accountId: string;
  token: string;

  constructor(json: JsonObject) {
    this.accountId = json.accountId as string;
    this.token = json.token as string;
  }
}
