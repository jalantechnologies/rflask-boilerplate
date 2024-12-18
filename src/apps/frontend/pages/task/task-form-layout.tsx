import React, { PropsWithChildren } from 'react';

const TaskFormLayout: React.FC<PropsWithChildren> = ({
  children,
}) => (
  <div className="flex h-[calc(100vh-74px)] items-center justify-center p-4 md:p-6 2xl:p-10">
    <div className="w-full rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-boxdark sm:p-12.5 md:w-4/5 xl:w-3/5">
      {children}
    </div>
  </div>
);

export default TaskFormLayout;
