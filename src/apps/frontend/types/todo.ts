// src/apps/frontend/types/todo.ts
export interface Todo {
  id: string;
  title: string;
  description: string;
  type: 'Personal' | 'Official' | 'Hobby';
  due_date: string;
  completed: boolean;
}
