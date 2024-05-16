import React from 'react';
import {
  Button,
  FormControl,
  HorizontalStackLayout,
  Input,
  VerticalStackLayout,
} from '../../components';
import Modal from '../../components/modal';
import { ButtonKind, ButtonType } from '../../types/button';
import TextArea from '../../components/textarea/textarea';

interface TaskModalProps {
  buttonText: string;
  isModalOpen: boolean;
  closeModal: (open: boolean) => void;
}

const TaskModal: React.FC<TaskModalProps> = ({
  buttonText,
  isModalOpen,
  closeModal,
}) => {
  return (
    <Modal isModalOpen={isModalOpen}>
      <div className="fill-current absolute right-4 top-4">
        <Button kind={ButtonKind.TERTIARY} onClick={closeModal}>
          <img
            className="fill-current opacity-50"
            src="/assets/img/icon/close.svg"
            alt="close icon"
          />
        </Button>
      </div>

      <form onSubmit={() => {}}>
        <VerticalStackLayout gap={5}>
          <FormControl error={null} label={'Add task title'}>
            <Input
              data-testid="title"
              disabled={false}
              error={null}
              name="title"
              placeholder="title"
              type="text"
            />
          </FormControl>
          <FormControl error={null} label={'Add task description'}>
            <TextArea
              disabled={false}
              error={null}
              name={'description'}
              placeholder="description"
              rows={7}
            />
          </FormControl>
          <FormControl error={null} label={'Task List'}>
            <HorizontalStackLayout gap={4}>
              <Input
                disabled={false}
                error={null}
                placeholder="Add list"
                type="text"
              />
              <Button
                kind={ButtonKind.SECONDARY}
                icon={
                  <img
                    className="opacity-50"
                    src="/assets/img/icon/plus.svg"
                    alt="plus icon"
                  />
                }
              />
            </HorizontalStackLayout>
          </FormControl>
          <Button type={ButtonType.SUBMIT}>{buttonText}</Button>
        </VerticalStackLayout>
      </form>
    </Modal>
  );
};

export default TaskModal;
