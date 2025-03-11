import React, { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import TaskModal from './task-modal';
import constant from '../../constants';
import TaskHeader from './task-header';
import { Task } from '../../types/task';
import TaskList from './task-list';
import { useTaskContext } from '../../contexts/task.provider';
import { AsyncError } from '../../types';

const Tasks: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const onError = (error: AsyncError) => {
    toast.error(error.message);
  };

  const { getTaskList } = useTaskContext();

  useEffect(() => {
    getTaskList().catch((error) => onError(error as AsyncError));
  }, []);

  const addTaskFormik = useFormik({
    initialValues: {
      id: '',
      title: '',
      description: '',
    },
    validationSchema: Yup.object({
      title: Yup.string()
        .min(constant.ADD_TASK_MIN_LENGTH, constant.ADD_TASK_VALIDATION_ERROR)
        .required(constant.ADD_TASK_VALIDATION_ERROR),
      description: Yup.string()
        .min(
          constant.ADD_TASK_DESCRIPTION_MIN_LENGTH,
          constant.ADD_TASK_DESCRIPTION_VALIDATION_ERROR,
        )
        .required(constant.ADD_TASK_DESCRIPTION_VALIDATION_ERROR),
    }),
    onSubmit: (values, { resetForm }) => {
      if (!values.title || !values.description) {
        console.error('Task details are missing!');
        return;
      }
      setTasks((prevTasks) => [
        ...prevTasks,
        { ...values, id: Date.now().toString() },
      ]);
      resetForm();
      setIsModalOpen(false);
    },
  });

  return (
    <div className="p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6">
      <TaskHeader onAddTask={() => setIsModalOpen(true)} />
      <div className="">
        <TaskList tasks={tasks} />
      </div>
      <TaskModal
        btnText="Add Task"
        formik={addTaskFormik}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};

export default Tasks;
