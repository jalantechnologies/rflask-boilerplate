import React, { PropsWithChildren } from 'react';

const TodoFormLayout: React.FC<PropsWithChildren> = ({ children }) => (
  <div className="flex items-center justify-center  md:p-6 2xl:p-10">
    <div className="w-full rounded-sm border border-stroke bg-white p-4 shadow-default dark:border-strokedark dark:bg-boxdark sm:p-12.5 md:w-4/5 lg:p-5 xl:w-3/5">
      {children}
    </div>
  </div>
);

export default TodoFormLayout;
