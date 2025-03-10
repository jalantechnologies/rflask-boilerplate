import React, { useState } from 'react';
import { Task } from '../../types/task';
import TaskItem from './task-item';

const TaskList: React.FC<{ tasks: Task[] }> = ({ tasks }) => {
  const [openTaskId, setOpenTaskId] = useState<string | null>(null);

  return (
    <div>
      {tasks.length > 0 && (
        <h4 className="font-bold text-black mb-4">To Do ({tasks.length})</h4>
      )}

      <div className="">
        <div className="flex flex-col gap-4 ">
          {tasks.length > 0 ? (
            tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                openTaskId={openTaskId}
                setOpenTaskId={setOpenTaskId}
              />
            ))
          ) : (
            <p className="text-gray-500">No tasks available</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskList;
