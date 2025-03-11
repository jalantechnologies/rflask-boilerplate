export class Task {
  description: string;
  id: string;
  title: string;

  constructor(description: string, id: string, title: string) {
    this.description = description;
    this.id = id;
    this.title = title;
  }

  static fromApiArray(data: any[]): Task[] {
    return data.map(
      (item) =>
        new Task(item.description || '', item.id || '', item.title || ''),
    );
  }
}
