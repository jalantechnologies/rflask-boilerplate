import React from 'react';
import clsx from 'clsx';
import Tag from '../tag';
import H3 from '../typography/h3';  // Import H3 component

interface TaskItemProps {
  task: {
    taskId: string;
    title: string;
    type: string;
    dueDate: string;
  };
  handleEditTask: (task: any) => void;
  getTypeColor: (type: string) => string;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, handleEditTask, getTypeColor }) => (
  <div
    onClick={() => handleEditTask(task)}
    className={clsx([
      'flex flex-col rounded-lg px-4 py-2 m-1',
      'border border-gray-300', // Add a line after each task item
    ])}
    key={task.taskId}
    style={{ margin: '10px' }}
  >
    <div className={clsx(['flex items-center justify-between rounded-lg'])}>
      <H3>{task.title}</H3>
      <div className={clsx(['font-bold'])}>{'>'}</div>
    </div>

    <div className={clsx(['inline-flex rounded-lg m-1'])}>
      <Tag
        startEnhancer={
          <div
            style={{
              width: '10px',
              height: '10px',
              backgroundColor: getTypeColor(task.type),
            }}
            className="opacity-50"
          />
        }
        text={task.type}
        textAlign="center"
        colorVal="lightgrey"
      />

      <Tag
        startEnhancer={
          <img
            alt="calendar icon"
            className="fill-current opacity-50"
            src="/assets/img/icon/calendar.svg"
            style={{
              verticalAlign: 'middle',
              width: '10px',
              height: '10px',
            }}
          />
        }
        text={task.dueDate}
        textAlign="center"
        colorVal="lightgrey"
      />
    </div>
  </div>
);

export default TaskItem;
