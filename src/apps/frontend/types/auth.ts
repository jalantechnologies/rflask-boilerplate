import { JsonObject } from './common-types';

export class AccessToken {
  accountId: string;
  token: string;
  expiresAt:string

  constructor(json: JsonObject) {
    this.accountId = json.account_id as string;
    this.token = json.token as string;
    this.expiresAt = json.expires_at as string;
  }
}
export enum KeyboardKeys {
  BACKSPACE = 'Backspace',
}

export class PhoneNumber {
  countryCode: string;
  phoneNumber: string;

  constructor(json: JsonObject) {
    this.countryCode = json.country_code as string;
    this.phoneNumber = json.phone_number as string;
  }

  displayPhoneNumber(): string {
    return `${this.countryCode} ${this.phoneNumber}`;
  }
}
