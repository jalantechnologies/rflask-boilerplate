import React, { PropsWithChildren } from 'react';

interface TaskCheckboxProps {
  taskId: string;
}

const TaskCheckBox: React.FC<PropsWithChildren<TaskCheckboxProps>> = ({
  children,
  taskId,
}) => (
  <label htmlFor={taskId} className="flex cursor-pointer select-none">
    <span className="flex items-center content-center">
      <input type="checkbox" id={taskId} className="peer taskCheckbox sr-only" />
      <span className="box flex mr-4 size-5 font-semibold items-center justify-center rounded border border-stroke ">
        <img alt="check" src="/assets/img/icon/form-checkbox-checkmark.svg" />
      </span>
    </span>
    <span className="font-medium peer-checked:line-through">{children}</span>
  </label>
);

export default TaskCheckBox;
