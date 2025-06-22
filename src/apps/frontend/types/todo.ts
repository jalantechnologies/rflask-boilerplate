export enum TodoType {
  Personal = 'Personal',
  Official = 'Official',
  Hobby = 'Hobby',
}

export enum TodoStatus {
  Todo = 'todo',
  InProgress = 'in_progress',
  Done = 'done',
}

export class Todo {
  id: string;
  title: string;
  description?: string;
  status: TodoStatus;
  due_date?: Date;
  type?: TodoType;

  constructor(data: any) {
    this.id = data.id;
    this.title = data.title;
    this.description = data.description;
    this.status = data.status;
    this.due_date = data.due_date ? new Date(data.due_date) : undefined;
    this.type = data.type;
  }
}
