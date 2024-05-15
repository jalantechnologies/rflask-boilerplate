import React, { useState } from 'react';
import { Button, H2, H3, VerticalStackLayout } from '../../components';
import TaskGroup from './task-group';
import TaskModal from './task-modal';

const Tasks: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const toggleModal = (forceValue?: boolean) => {
    setIsModalOpen((prevState) => {
      return forceValue !== undefined ? forceValue : !prevState;
    });
  };
  return (
    <div className="p-4 mx-auto h-screen overflow-y-auto">
      <div className="mx-auto pb-60">
        <VerticalStackLayout gap={7}>
          <H2>Tasks List</H2>
          <div className="flex gap-y-4 justify-between items-center rounded-lg border border-stroke bg-white p-2 px-4 shadow-4">
            <H3>Tasks</H3>
            <Button onClick={() => toggleModal()}>Add task</Button>
          </div>
          <TaskGroup groupTitle={`ToDo's`} tasksCount={3} />
          <TaskGroup groupTitle={`InProgress's`} tasksCount={2} />
          <TaskGroup groupTitle={`Completed`} tasksCount={1} />
        </VerticalStackLayout>
      </div>
      <TaskModal
        isModalOpen={isModalOpen}
        closeModal={() => toggleModal(false)}
        buttonText={'Add Task'}
      />
    </div>
  );
};

export default Tasks;
