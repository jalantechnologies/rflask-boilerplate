export class Todo {
  id: string;
  title: string;
  description?: string;
  status: string;
  dueDate?: Date;
  type?: string;

  constructor(data: any) {
    this.id = data.id;
    this.title = data.title;
    this.description = data.description;
    this.status = data.status;
    this.dueDate = data.due_date ? new Date(data.due_date) : undefined;
    this.type = data.type;
  }
}
