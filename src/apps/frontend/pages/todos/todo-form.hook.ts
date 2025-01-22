import { useFormik } from 'formik';
import React from 'react';
import * as Yup from 'yup';

import constant from '../../constants';
import { useTodoContext } from '../../contexts';
import { AccessToken, AsyncError, Todo } from '../../types';
import { JsonObject } from '../../types/common-types';

interface TodoFormProps {
  todoId?: string;
  onError: (err: AsyncError) => void;
  onSuccess: () => void;
}

const useTodoForm = ({ todoId, onError, onSuccess }: TodoFormProps) => {
  const {
    createTodo,
    createTodoError,
    isCreateTodoLoading,
    updateTodo,
    updateTodoError,
    isUpdateTodoLoading,
  } = useTodoContext();

  const formik = useFormik({
    initialValues: {
      title: '',
      description: '',
      type: '',
      dueDate: '',
    },
    validationSchema: Yup.object({
      title: Yup.string()
        .min(
          constant.TODO_TITLE_MIN_LENGTH,
          constant.TODO_TITLE_VALIDATION_ERROR,
        )
        .required(constant.TODO_TITLE_VALIDATION_ERROR),
      description: Yup.string()
        .min(
          constant.TODO_DESCRIPTION_MIN_LENGTH,
          constant.TODO_DESCRIPTION_VALIDATION_ERROR,
        )
        .required(constant.TODO_DESCRIPTION_VALIDATION_ERROR),
      type: Yup.string()
        .oneOf(
          ['Official', 'Personal', 'Hobby'],
          constant.TODO_TYPE_VALIDATION_ERROR,
        )
        .required(constant.TODO_TYPE_VALIDATION_ERROR),
      dueDate: Yup.date()
        .min(new Date(), constant.TODO_DUE_DATE_VALIDATION_ERROR)
        .required(constant.TODO_DUE_DATE_VALIDATION_ERROR),
    }),
    onSubmit: (values) => {
      const userAccessToken = new AccessToken(
        JSON.parse(localStorage.getItem('access-token')) as JsonObject,
      );

      if (todoId) {
        const todo: Partial<Todo> = {
          id: todoId,
          accountId: userAccessToken.accountId,
          title: values.title,
          description: values.description,
          type: values.type as 'Official' | 'Personal' | 'Hobby',
          dueDate: values.dueDate,
        };
        updateTodo(todo)
          .then(() => {
            onSuccess();
          })
          .catch((err) => {
            onError(err as AsyncError);
          });
      } else {
        const todo: Partial<Todo> = {
          accountId: userAccessToken.accountId,
          title: values.title,
          description: values.description,
          type: values.type as 'Official' | 'Personal' | 'Hobby',
          dueDate: values.dueDate,
        };
        createTodo(todo)
          .then(() => {
            onSuccess();
          })
          .catch((err) => {
            onError(err as AsyncError);
          });
      }
    },
  });

  const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { value } = e.target;
    // eslint-disable-next-line @typescript-eslint/no-floating-promises
    formik.setFieldValue('type', value);
  };

  if (todoId) {
    return {
      formik,
      isUpdateTodoLoading,
      updateTodoError,
      handleSelectChange,
    };
  }
  return {
    formik,
    isCreateTodoLoading,
    createTodoError,
    handleSelectChange,
  };
};

export default useTodoForm;
