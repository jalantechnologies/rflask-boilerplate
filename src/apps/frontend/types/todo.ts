import { JsonObject } from './common-types';

export class Todo {
  id: string;
  accountId: string;
  title: string;
  description: string;
  type: string;
  dueDate: string;
  completed: boolean;
  completedDate: string;

  constructor(json: JsonObject) {
    this.id = json.id as string;
    this.accountId = json.accountId as string;
    this.title = json.title as string;
    this.description = json.description as string;
    this.type = json.type as string;
    this.dueDate = json.dueDate as string;
    this.completed = json.completed as boolean;
    this.completedDate = json.completedDate as string;
  }
}
