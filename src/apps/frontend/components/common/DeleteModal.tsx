import React from 'react';

interface DeleteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title?: string;
  message?: string;
}

const DeleteModal: React.FC<DeleteModalProps> = ({
  isOpen,
  message = 'Are you sure you want to delete this item?',
  onClose,
  onConfirm,
  title = 'Delete Confirmation',
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-6 rounded-lg shadow-lg w-[500px]">
        <h2 className="text-xl font-semibold text-black text-center pb-3">
          {title}
        </h2>
        <p className="text-gray-600 mt-2 text-center mb-5 pb-3">{message}</p>
        <div className="flex justify-center gap-4 mt-5 pb-3">
          <button
            onClick={onClose}
            className="bg-[#8080806b] text-black font-semibold text-lg px-6 py-3 rounded"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="bg-[red] text-white font-semibold text-lg px-6 py-3 rounded"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default DeleteModal;
