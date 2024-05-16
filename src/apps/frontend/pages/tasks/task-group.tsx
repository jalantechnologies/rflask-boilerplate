import React, { useState } from 'react';
import { Button, H4 } from '../../components';
import { ButtonKind } from '../../types/button';
import TaskCheckBox from './task-checkbox';

interface TaskGroupProps {
  groupTitle: string;
  tasksCount: number;
}

const TaskGroup: React.FC<TaskGroupProps> = ({ groupTitle, tasksCount }) => {
  const [showControls, setShowControls] = useState(false);

  const toggleControlVisibility = (forceValue?: boolean) => {
    setShowControls((prevState) => {
      return forceValue !== undefined ? forceValue : !prevState;
    });
  };
  return (
    <div className="flex flex-col gap-4 mt-4">
      <h4 className="text-xl font-bold text-black">
        {groupTitle} ({tasksCount})
      </h4>
      <div className="flex flex-col gap-y-5 pt-8 justify-between relative rounded-lg border border-stroke bg-white p-4 shadow-4">
        <div className="absolute right-4 top-4">
          <Button
            fullWidth
            icon={
              <img
                className="fill-current opacity-50"
                src="/assets/img/icon/menu.svg"
                alt="plus icon"
              />
            }
            onBlur={() => toggleControlVisibility(false)}
            onClick={() => toggleControlVisibility()}
            kind={ButtonKind.TERTIARY}
          ></Button>
          {showControls && (
            <div className="absolute right-0 top-full z-100 w-50 rounded-lg border border-stroke bg-white p-2 shadow-1">
              <Button
                fullWidth
                kind={ButtonKind.SECONDARY}
                icon={
                  <img
                    className="fill-current"
                    src="/assets/img/icon/edit.svg"
                    alt="plus icon"
                  />
                }
              >
                Edit
              </Button>

              <Button
                fullWidth
                kind={ButtonKind.SECONDARY}
                icon={
                  <img
                    className="fill-current"
                    src="/assets/img/icon/delete.svg"
                    alt="plus icon"
                  />
                }
              >
                Delete
              </Button>
            </div>
          )}
        </div>
        <H4>Task Title</H4>
        {['Sample Task 1', 'Sample Task 2', 'Sample Task 3'].map(
          (task, index) => (
            <TaskCheckBox taskId={`todos-${index}`} key={task}>
              {task}
            </TaskCheckBox>
          ),
        )}
      </div>
    </div>
  );
};

export default TaskGroup;
