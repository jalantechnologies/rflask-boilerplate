import React from 'react';
import { Task } from '../../types/task';
import MenuItem from '../../components/menu-item';
import { Button } from '../../components';
import { ButtonKind } from '../../types/button';

const TaskList: React.FC<{ tasks: Task[] }> = ({ tasks }) => (
  <div className="p-4 mx-auto md:p-6 border border-[#e4e7ec]">
    <h2 className="text-base font-medium text-black">To Do</h2>
    <div className="flex flex-col gap-1 mt-3">
      {tasks.length > 0 ? (
        tasks.map((task) => (
          <div
            key={task.id}
            className="flex justify-between items-center w-full p-4 mb-4 border border-[#e4e7ec] task rounded-xl shadow-theme-sm dark:border-gray-800"
          >
            <div>
              <h2 className="text-black">{task.title}</h2>
              <p className="mt-[7px]">{task.description}</p>
            </div>

            <div>
              <MenuItem>
                <Button kind={ButtonKind.SECONDARY}>Edit</Button>
                <Button kind={ButtonKind.SECONDARY}>Delete</Button>
              </MenuItem>
            </div>
          </div>
        ))
      ) : (
        <p className="text-gray-500">No tasks available</p>
      )}
    </div>
  </div>
);

export default TaskList;
