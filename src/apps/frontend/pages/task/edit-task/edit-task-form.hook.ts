import { useFormik } from 'formik';
import * as Yup from 'yup';
import React from 'react';

import constant from '../../../constants';
import { useTaskContext } from '../../../contexts';
import { AsyncError, TaskPayload } from '../../../types';

interface EditTaskFormProps {
    onError: (err: AsyncError) => void;
    onSuccess: () => void;
    task: TaskPayload;
}

const useEditTaskForm = ({ onError, onSuccess, task }: EditTaskFormProps) => {
    const { isUpdateTaskLoading, updateTaskError, updateTask } = useTaskContext();

    const formik = useFormik({
        initialValues: {
            title: task.title || '',
            description: task.description || '',
            type: task.type || '', // Official, Personal, Hobby, etc.
            dueDate: task.dueDate ? task.dueDate: '',
        },
        validationSchema: Yup.object({
            title: Yup.string()
                .min(constant.TITLE_MIN_LENGTH, constant.TITLE_VALIDATION_ERROR)
                .required(constant.TITLE_VALIDATION_ERROR),
            description: Yup.string()
                .min(constant.DESCRIPTION_MIN_LENGTH, constant.DESCRIPTION_VALIDATION_ERROR)
                .required(constant.DESCRIPTION_VALIDATION_ERROR),
            type: Yup.string()
                .oneOf(['Official', 'Personal', 'Hobby'], constant.TYPE_VALIDATION_ERROR)
                .required(constant.TYPE_VALIDATION_ERROR),
            dueDate: Yup.date()
                .min(new Date(), constant.DUE_DATE_VALIDATION_ERROR)
                .required(constant.DUE_DATE_VALIDATION_ERROR),
        }),
        onSubmit: (values) => {
            const taskPayload: Partial<TaskPayload> = {
                title: values.title,
                description: values.description,
                type: values.type as 'Official' | 'Personal' | 'Hobby', // Narrow type to match TaskPayload
                dueDate: values.dueDate, // Assuming dueDate is already in ISO format
            };
            updateTask(taskPayload)
                .then(() => {
                    onSuccess();
                })
                .catch((err) => {
                    onError(err as AsyncError);
                });
        },
    });
    // Custom handler for Select change
    const handleSelectChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const { value } = e.target;
        formik.setFieldValue('type', value); // Update Formik field value
    };

    return {
        formik,
        isUpdateTaskLoading,
        updateTaskError,
        handleSelectChange
    };
};

export default useEditTaskForm;
