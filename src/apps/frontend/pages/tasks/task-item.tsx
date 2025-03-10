import React from 'react';
import { Task } from '../../types/task';
import MenuItem from '../../components/menu-item';
import { Button } from '../../components';
import { ButtonKind } from '../../types/button';
import CommentSection from './task-comment-section';

const TaskItem: React.FC<{
  task: Task;
  openTaskId: string | null;
  setOpenTaskId: (id: string | null) => void;
}> = ({ task, openTaskId, setOpenTaskId }) => {
  const handleToggleComments = () => {
    setOpenTaskId(openTaskId === task.id ? null : task.id);
  };

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
            <Button kind={ButtonKind.SECONDARY}>Edit</Button>
            <Button kind={ButtonKind.SECONDARY}>Delete</Button>
          </MenuItem>
        </div>
      </div>

      {openTaskId === task.id && <CommentSection taskId={task.id} />}
    </div>
  );
};

export default TaskItem;
