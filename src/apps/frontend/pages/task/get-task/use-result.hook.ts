import { useEffect, useState } from 'react';
import { useTaskContext } from '../../../contexts';
import { AsyncError, TaskPayload } from '../../../types';

interface TaskResultsProps {
  onError: (err: AsyncError) => void;
}

const useTaskResults = ({ onError }: TaskResultsProps) => {
  const { getTasks, isGetTasksLoading, getTasksError } = useTaskContext();
  const [tasks, setTasks] = useState<TaskPayload[]>([]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await getTasks();
        setTasks(response);  // Assuming API response has `data` field
      } catch (err) {
        onError(err as AsyncError);
      }
    };

    fetchTasks();
  }, [getTasks, onError]);

  return {
    tasks,
    isGetTasksLoading,
    getTasksError,
  };
};

export default useTaskResults;
