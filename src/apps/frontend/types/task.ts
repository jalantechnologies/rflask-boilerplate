export class Task {
  description: string;
  id: string;
  title: string;

  constructor(description: string, id: string, title: string) {
    this.description = description;
    this.id = id;
    this.title = title;
  }
}
