export class Comment {
  id: string;
  text: string;
  comment: string;

  constructor(id: string, text: string) {
    this.id = id;
    this.text = text;
  }

  static fromApiArray(data: any[]): Comment[] {
    return data.map((item) => new Comment(item.id || '', item.text || ''));
  }
}
