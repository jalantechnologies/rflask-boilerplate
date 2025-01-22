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

import CreateTodoForm from './create-todo-form';

export const CreateTodo: React.FC = () => {
  const navigate = useNavigate();
  const onSuccess = () => {
    navigate(routes.TODOS);
    toast.success('Todo created successfully.');
  };

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };
  return (
    <TodoFormLayout>
      <VerticalStackLayout gap={2}>
        <H2Header>Create Todo</H2Header>
        <CreateTodoForm onSuccess={onSuccess} onError={onError} />
      </VerticalStackLayout>
    </TodoFormLayout>
  );
};

export default CreateTodo;
