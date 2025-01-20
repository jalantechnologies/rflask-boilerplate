import { JsonObject } from './common-types';

export class AccessToken {
  accountId: string;
  token: string;
  expiresAt:Date;

  constructor(json: JsonObject) {
    this.accountId = json.account_id as string;
    this.token = json.token as string;
    // Convert from Unix timestamp (seconds) to Date object
    this.expiresAt = new Date(parseFloat(json.expires_at as string) * 1000);
  }
  
  toJson(): JsonObject { 
    return{ 
      account_id:this.accountId,
      // Convert Date object back to Unix timestamp (seconds)
      expires_at:(this.expiresAt.getTime()/1000).toString(),
      token:this.token 
    }
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
