import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

import routes from '../../../constants/routes';
import { useTodoContext } from '../../../contexts';

export const DeleteTodo: React.FC = () => {
  const navigate = useNavigate();
  const todoId = useParams().id;

  const { deleteTodo, deleteTodoError, isDeleteTodoLoading } = useTodoContext();
  const [deleteError, setDeleteError] = useState<string>('');

  useEffect(() => {
    const delTodo = async () => {
      try {
        await deleteTodo(todoId);
        toast.success('Todo deleted successfully.');
        navigate(routes.TODOS);
      } catch (error) {
        setDeleteError('Error deleting todo');
      }
    };

    // noinspection JSIgnoredPromiseFromCall
    delTodo();
  }, [deleteTodo, todoId, navigate]);

  useEffect(() => {
    if (deleteTodoError) {
      toast.error(deleteTodoError.message);
      navigate(routes.TODOS);
    }
  }, [deleteTodoError, navigate]);

  useEffect(() => {
    if (deleteError) {
      toast.error(deleteError);
      navigate(routes.TODOS);
    }
  }, [deleteError, navigate]);

  if (isDeleteTodoLoading) {
    return <div>Deleting todo...</div>;
  }

  return null;
};

export default DeleteTodo;
