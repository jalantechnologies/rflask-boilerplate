import React, { useEffect, useState } from 'react';
import clsx from 'clsx';
import { useNavigate } from 'react-router-dom';

import { TaskPayload } from '../../../types';
import { useTaskContext } from '../../../contexts';
import { FlexItem, H2 } from '../../../components';
import TaskItem from '../../../components/tasks/task-item';
import routes from '../../../constants/routes';

const TaskList: React.FC = () => {
  const { getTasks, isGetTasksLoading, getTasksError } = useTaskContext();
  const [tasks, setTasks] = useState<TaskPayload[]>([]);
  const navigate = useNavigate();

  
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await getTasks();
        if (response) {
          setTasks(response); 
        } else {
          console.error('Failed to fetch tasks:', response);
        }
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    fetchTasks();
  }, [getTasks]);

  if (isGetTasksLoading) {
    return <div>Loading tasks...</div>;
  }

  if (getTasksError) {
    return <div>Error loading tasks: {getTasksError.message}</div>;
  }

  const handleEditTask = (task: TaskPayload) => {
    navigate(routes.EDITTASK(task.taskId), { state: { task } }); 
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Official':
        return 'red';
      case 'Personal':
        return 'dodgerblue';
      case 'Hobby':
        return 'green';
      default:
        return 'black';
    }
  };

  return (
    <div className={clsx(['flex flex-col rounded-lg px-4 py-2 m-1'])} style={{ margin: '20px' }}>
      <div className={clsx(['inline-flex rounded-lg px-4 py-2 m-1'])}>
        <H2 className="mr-10">Task List</H2>
        <H2 className="justify-self-end" style={{ fontStyle: 'italic', marginLeft: '10px', marginRight: '10px' }}>
          {tasks.length}
        </H2>
      </div>
      
      {tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <FlexItem>
          {tasks.map((task) => (
            <TaskItem
              key={task.taskId}
              task={task}
              handleEditTask={handleEditTask}
              getTypeColor={getTypeColor}
            />
          ))}
        </FlexItem>
      )}
    </div>
  );
};

export default TaskList;
