import { PhoneNumber } from './auth';
import { JsonObject } from './common-types';

export class Account {
  id: string;
  firstName: string;
  lastName: string;
  phoneNumber?: PhoneNumber;
  username: string;

  constructor(json: JsonObject) {
    this.id = json.id as string;
    this.firstName = json.first_name as string;
    this.lastName = json.last_name as string;
    this.phoneNumber = json.phone_number ? new PhoneNumber(json.phone_number as JsonObject) : null;
    this.username = json.username as string;
  }

  displayName(): string {
    return (`${this.firstName} ${this.lastName}`).trim();
  }
}
