import React from 'react';

import { AsyncError } from '../../../types';

import { TodoForm } from '../../../components';

interface CreateTodoFormProps {
  onError: (error: AsyncError) => void;
  onSuccess: () => void;
}

const CreateTodoForm: React.FC<CreateTodoFormProps> = ({
  onError,
  onSuccess,
}) => {
  return <TodoForm onSuccess={onSuccess} onError={onError} />;
};

export default CreateTodoForm;
