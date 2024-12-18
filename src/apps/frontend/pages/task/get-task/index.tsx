import React, { useEffect, useState } from 'react';

import { useTaskContext } from '../../../contexts';
import { TaskPayload } from '../../../types';
import { useNavigate } from 'react-router-dom';

const TaskList: React.FC = () => {
  const { getTasks, isGetTasksLoading, getTasksError } = useTaskContext();
  const [tasks, setTasks] = useState<TaskPayload[]>([]);
  const navigate = useNavigate();
  // Fetch tasks when the component mounts
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await getTasks();
        if (response) {
          setTasks(response); // Populate tasks in state
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
    navigate(`/edit-task/${task.taskId}`, { state: { task } }); // Pass TaskPayload to EditTask component
  };

  return (
    <div>
      <h1>Task List</h1>
      {tasks.length === 0 ? (
        <p>No tasks found.</p>
      ) : (
        <ul>
          {tasks.map((task) => (
            <li key={task.taskId}>
              <h3>{task.title}</h3>
              <p>{task.description}</p>
              <p>Type: {task.type}</p>
              <p>Due Date: {task.dueDate}</p>
              <button onClick={() => handleEditTask(task)}>Edit Task</button> {/* Edit button */}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
  
};

export default TaskList;
