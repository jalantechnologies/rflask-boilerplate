import React, { PropsWithChildren } from 'react';

interface ModalProps {
  isModalOpen: boolean;
}

const Modal: React.FC<PropsWithChildren<ModalProps>> = ({
  children,
  isModalOpen,
}) => (
  <div
    className={`fixed left-0 top-0 z-99999 flex h-screen w-full justify-center overflow-y-scroll bg-black/80 backdrop-blur-sm  ${
      isModalOpen ? 'block' : 'hidden'
    }`}
  >
    <div className="relative m-auto w-full max-w-203 rounded-sm border border-stroke bg-gray p-10 shadow-default">
      {children}
    </div>
  </div>
);

export default Modal;
