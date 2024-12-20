import React from 'react';

import {
    Button,
    DateInput,
    FormControl,
    Input,

    Select,
    VerticalStackLayout,
} from '../../../components';

import { AsyncError, TaskPayload } from '../../../types';
import { ButtonKind, ButtonType } from '../../../types/button';

import useEditTaskForm from './edit-task-form.hook'; // The hook you provided

interface EditTaskFormProps {
    onError: (error: AsyncError) => void;
    onSuccess: () => void;
    task: TaskPayload;
}

const EditTaskForm: React.FC<EditTaskFormProps> = ({ task, onError, onSuccess }) => {
    // Pass task as part of the hook
    const { formik, isEditTaskLoading, handleSelectChange } = useEditTaskForm({ onSuccess, onError, task });
    
    return (
        <form onSubmit={formik.handleSubmit}>
            <VerticalStackLayout gap={5}>
                <FormControl
                    label={'Task Title'}
                    error={formik.touched.title && formik.errors.title}
                >
                    <Input
                        error={formik.touched.title && formik.errors.title}
                        data-testid="title"
                        disabled={isEditTaskLoading}
                        name="title"
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        placeholder="Enter task title"
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
                        disabled={isEditTaskLoading}
                        name="description"
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}
                        placeholder="Enter task description"
                        value={formik.values.description}
                    />
                </FormControl>

                <FormControl
                    label={'Task Type'}
                    error={formik.touched.type && formik.errors.type}
                >
                    <Select
                        handleChange={handleSelectChange} 
                        isLoading={isEditTaskLoading}
                        options={[
                            { value: '', label: 'Select task type' },
                            { value: 'Official', label: 'Official' },
                            { value: 'Personal', label: 'Personal' },
                            { value: 'Hobby', label: 'Hobby' },
                        ]}
                        value={formik.values.type} // Make sure Formik's value is correctly passed
                    />
                </FormControl>



                <FormControl
                    label={'Due Date'}
                    error={formik.touched.dueDate && formik.errors.dueDate}
                >
                    <DateInput
                        name="dueDate"
                        value={formik.values.dueDate}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                        error={formik.touched.dueDate && formik.errors.dueDate}
                        placeholder="Select a due date"
                    />
                </FormControl>

                <Button
                    type={ButtonType.SUBMIT}
                    kind={ButtonKind.PRIMARY}
                    isLoading={isEditTaskLoading}
                >
                    Edit Task
                </Button>
            </VerticalStackLayout>
        </form>
    );
};

export default EditTaskForm;
