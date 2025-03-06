import React from 'react';
import { Button } from '../../components';
import { ButtonKind } from '../../types/button';

const TaskHeader: React.FC<{ onAddTask: () => void }> = ({ onAddTask }) => (
  <div className="flex items-start justify-between gap-3 mb-6">
    <div>
      <h2 className="text-xl font-semibold text-black">Task List</h2>
    </div>
    <div>
      <Button kind={ButtonKind.PRIMARY} onClick={onAddTask}>
        Add New Task
      </Button>
    </div>
  </div>
);

export default TaskHeader;
