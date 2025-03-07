import React from 'react';

const TaskHeader: React.FC<{ onAddTask: () => void }> = ({ onAddTask }) => (
  <div>
    <div>
      <h2 className="text-xl font-semibold text-black">Task List</h2>
    </div>
    <div className="flex justify-between items-center bg-white border border-stroke p-3 rounded-md mt-4 mb-4">
      <p className="font-bold	text-black text-lg">Tasks</p>
      <button
        className="p-2 w-[149px] bg-[#0000FF] rounded text-white"
        onClick={onAddTask}
      >
        Add Task
      </button>
    </div>
  </div>
);

export default TaskHeader;
