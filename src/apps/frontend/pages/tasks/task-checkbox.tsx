import React, { PropsWithChildren } from 'react';

interface TaskCheckboxProps {
  taskId: string;
}

const TaskCheckBox: React.FC<PropsWithChildren<TaskCheckboxProps>> = ({
  children,
  taskId,
}) => (
  <label htmlFor={taskId} className="flex cursor-pointer select-none">
    <div className="flex items-center content-center">
      <input type="checkbox" id={taskId} className="peer taskCheckbox sr-only" />
      <div className="box flex mr-4 size-5 font-semibold items-center justify-center rounded border border-stroke ">
        <img alt="check" src="/assets/img/icon/form-checkbox-checkmark.svg" />
      </div>
    </div>
    <p className="font-medium peer-checked:line-through">{children}</p>
  </label>
);

export default TaskCheckBox;
