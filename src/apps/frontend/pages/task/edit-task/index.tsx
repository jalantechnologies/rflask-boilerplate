import React from 'react';
import toast from 'react-hot-toast';
import { H2, VerticalStackLayout } from '../../../components';
import EditTaskForm from './edit-task-form';
import { AsyncError } from '../../../types';
import { useLocation } from 'react-router-dom';
import TaskFormLayout from '../task-form-layout';
import TaskPageLayout from '../task-page-layout';



export const EditTask: React.FC = () => {
    const location = useLocation();
    const task = location.state?.task;
    const onSuccess = () => {
        toast.success(
            'Task added successfully',
        );
    };

    const onError = (error: AsyncError) => {
        toast.error(error.message);
    };
    return (
        <TaskPageLayout>
            <TaskFormLayout>
                <VerticalStackLayout gap={2}>
                    <H2>EDIT TASK</H2>
                    {!task ? (
                        <H2>No Task found</H2>  // Show this if task is not found
                    ) : (
                        <EditTaskForm task={task} onSuccess={onSuccess} onError={onError} />
                    )}
                </VerticalStackLayout>
            </TaskFormLayout>
        </TaskPageLayout>
    );
};

export default EditTask;