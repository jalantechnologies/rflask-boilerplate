import React from 'react';
import { FormikProps } from 'formik';
import {
  Button,
  FormControl,
  VerticalStackLayout,
  Input,
} from '../../components';
import TextArea from '../../components/input/text-area';
import Modal from '../../components/modal';
import { ButtonType } from '../../types/button';
import { Task } from '../../types/task';

interface TaskModalProps {
  btnText: string;
  formik: FormikProps<Task>;
  isOpen: boolean;
  onClose: () => void;
}

const TaskModal: React.FC<TaskModalProps> = ({
  btnText,
  formik,
  isOpen,
  onClose,
}) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <h4 className="mb-2 text-2xl font-semibold text-black">Add a new Task</h4>
      <form onSubmit={formik.handleSubmit} className="p-6">
        <VerticalStackLayout gap={4}>
          <FormControl label="Task Title">
            <Input
              name="title"
              onBlur={formik.handleBlur}
              onChange={formik.handleChange}
              placeholder="Enter task title"
              type="text"
              value={formik.values.title}
            />
          </FormControl>
          <FormControl label="Task Description">
            <TextArea
              name="description"
              onBlur={formik.handleBlur}
              onChange={formik.handleChange}
              placeholder="Enter task description"
              rows={5}
              cols={30}
              value={formik.values.description}
            />
          </FormControl>
          <div className="flex justify-end gap-2">
            <Button type={ButtonType.SUBMIT}>{btnText}</Button>
          </div>
        </VerticalStackLayout>
      </form>
    </Modal>
  );
};

export default TaskModal;
