import React from 'react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

import {
  H2Header,
  VerticalStackLayout,
  TodoFormLayout,
} from '../../../components';
import routes from '../../../constants/routes';
import { AsyncError } from '../../../types';

import UpdateTodoForm from './update-todo-form';

export const UpdateTodo: React.FC = () => {
  const navigate = useNavigate();
  const onSuccess = () => {
    navigate(routes.TODOS);
    toast.success('Todo updated successfully.');
  };

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };
  return (
    <TodoFormLayout>
      <VerticalStackLayout gap={2}>
        <H2Header>Update Todo</H2Header>
        <UpdateTodoForm onSuccess={onSuccess} onError={onError} />
      </VerticalStackLayout>
    </TodoFormLayout>
  );
};

export default UpdateTodo;
