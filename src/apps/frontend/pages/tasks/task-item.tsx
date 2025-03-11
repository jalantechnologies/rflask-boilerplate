import React, { useState } from 'react';
import { Task } from '../../types/task';
import { useFormik } from 'formik';
import MenuItem from '../../components/menu-item';
import { Button } from '../../components';
import { ButtonKind } from '../../types/button';
import CommentSection from './task-comment-section';
import TaskModal from './task-modal';
import * as Yup from 'yup';
import constant from '../../constants';
import DeleteModal from '../../components/common/DeleteModal';

const TaskItem: React.FC<{
  task: Task;
  openTaskId: string | null;
  setOpenTaskId: (id: string | null) => void;
}> = ({ task, openTaskId, setOpenTaskId }) => {
  const handleToggleComments = () => {
    setOpenTaskId(openTaskId === task.id ? null : task.id);
  };

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  const editTaskFormik = useFormik({
    initialValues: {
      id: task.id, // ✅ Fix: Ensure task ID is set
      title: task.title || '',
      description: task.description || '',
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
      resetForm();
      setIsModalOpen(false);
    },
  });

  return (
    <div className="w-full p-5 border border-stroke shadow-sm rounded">
      <div className="flex justify-between border-b-[1px] items-center pb-3">
        <div className="">
          <h3 className="font-bold text-lg pb-2 text-black">{task.title}</h3>
          <p className="text-gray-600 text-md">{task.description}</p>
        </div>
        <div className="flex gap-6 ">
          <button
            onClick={() => handleToggleComments()}
            className="text-gray-600 hover:text-black"
          >
            <img
              alt="Comment"
              src="/assets/img/icon/comment.svg"
              className="h-6 w-6"
            />
          </button>

          <MenuItem>
            <Button
              kind={ButtonKind.SECONDARY}
              onClick={() => setIsModalOpen(true)}
            >
              Edit
            </Button>
            <Button
              kind={ButtonKind.SECONDARY}
              onClick={() => setIsDeleteModalOpen(true)}
            >
              Delete
            </Button>
          </MenuItem>
        </div>
      </div>

      {openTaskId === task.id && <CommentSection taskId={task.id} />}

      <TaskModal
        btnText="Update Task"
        formik={editTaskFormik}
        isOpen={isModalOpen}
        isEdit={true}
        onClose={() => setIsModalOpen(false)}
      />

      <DeleteModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={() => {
          setIsDeleteModalOpen(false);
        }}
        title="Delete Task"
        message="Are you sure you want to delete this task? This action cannot be undone."
      />
    </div>
  );
};

export default TaskItem;
