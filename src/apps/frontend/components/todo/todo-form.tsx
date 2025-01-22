import React, { PropsWithChildren } from 'react';

import useTodoForm from '../../pages/todos/todo-form.hook';
import { AsyncError, Todo } from '../../types';
import { ButtonKind, ButtonType } from '../../types/button';
import {
  Button,
  DateInput,
  FormControl,
  Input,
  Select,
  VerticalStackLayout,
} from '../index';

interface TodoFormProps {
  todo?: Todo;
  onError: (error: AsyncError) => void;
  onSuccess: () => void;
}

const TodoForm: React.FC<PropsWithChildren<TodoFormProps>> = ({
  todo,
  onSuccess,
  onError,
}) => {
  const todoId = todo ? todo.id : undefined;
  const {
    formik,
    isCreateTodoLoading,
    isUpdateTodoLoading,
    handleSelectChange,
  } = useTodoForm({
    todoId,
    onSuccess,
    onError,
  });

  const isTodoLoading = todoId ? isUpdateTodoLoading : isCreateTodoLoading;

  // useEffect(() => {
  //   if (todo) {
  //     // eslint-disable-next-line @typescript-eslint/no-floating-promises
  //     formik.setValues({
  //       title: todo.title || '',
  //       description: todo.description || '',
  //       type: todo.type || '',
  //       dueDate: todo.dueDate
  //         ? new Date(todo.dueDate).toISOString().split("T")[0]
  //         : '',
  //     });
  //   }
  // }, [formik, todo]);

  return (
    <form onSubmit={formik.handleSubmit}>
      <VerticalStackLayout gap={5}>
        <FormControl
          label={'Todo Title'}
          error={formik.touched.title && formik.errors.title}
        >
          <Input
            error={formik.touched.title && formik.errors.title}
            data-testid="title"
            disabled={isTodoLoading}
            name="title"
            onBlur={formik.handleBlur}
            onChange={formik.handleChange}
            placeholder="Enter todo title"
            value={formik.values.title}
          />
        </FormControl>

        <FormControl
          label={'Description'}
          error={formik.touched.description && formik.errors.description}
        >
          <Input
            error={formik.touched.description && formik.errors.description}
            data-testid="description"
            disabled={isTodoLoading}
            name="description"
            onBlur={formik.handleBlur}
            onChange={formik.handleChange}
            placeholder="Enter todo description"
            value={formik.values.description}
          />
        </FormControl>

        <FormControl
          label={'Todo Type'}
          error={formik.touched.type && formik.errors.type}
        >
          <Select
            handleChange={handleSelectChange}
            isLoading={isTodoLoading}
            options={[
              { value: '', label: 'Select todo type' },
              { value: 'Official', label: 'Official' },
              { value: 'Personal', label: 'Personal' },
              { value: 'Hobby', label: 'Hobby' },
            ]}
            value={formik.values.type}
          />
        </FormControl>

        <FormControl
          label={'Due Date'}
          error={formik.touched.dueDate && formik.errors.dueDate}
        >
          <DateInput
            name="dueDate"
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            error={formik.touched.dueDate && formik.errors.dueDate}
            placeholder="Select a due date"
            value={formik.values.dueDate}
          />
        </FormControl>

        <Button
          type={ButtonType.SUBMIT}
          kind={ButtonKind.PRIMARY}
          isLoading={isTodoLoading}
        >
          {todoId ? 'Update Todo' : 'Create Todo'}
        </Button>
      </VerticalStackLayout>
    </form>
  );
};
export default TodoForm;
