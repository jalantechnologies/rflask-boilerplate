import { JsonObject } from './common-types';

export class AccessToken {
  accountId: string;
  token: string;

  constructor(json: JsonObject) {
    this.accountId = json.account_id as string;
    this.token = json.token as string;
  }
}
export enum KeyboardKeys {
  BACKSPACE = 'Backspace',
}

export type PhoneNumber = {
  countryCode: string;
  phoneNumber: string;
};
