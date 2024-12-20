import React from 'react';
import toast from 'react-hot-toast';
import { H2, VerticalStackLayout } from '../../../components';
import AddTaskForm from './add-task-form';
import { AsyncError } from '../../../types';
import TaskFormLayout from '../task-form-layout';

export const AddTask: React.FC = () => {
  const onSuccess = () => {
    toast.success(
      'Task added successfully',
    );
  };

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };
  return (
      <TaskFormLayout>
        <VerticalStackLayout gap={2}>
          <H2>ADD TASK</H2>
          <AddTaskForm onSuccess={onSuccess} onError={onError} />
        </VerticalStackLayout>
      </TaskFormLayout>
  );
};

export default AddTask;