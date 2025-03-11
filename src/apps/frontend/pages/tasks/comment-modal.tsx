import React from 'react';
import { FormikProps } from 'formik';
import { Button, FormControl, VerticalStackLayout } from '../../components';
import TextArea from '../../components/input/text-area';
import Modal from '../../components/modal';
import { ButtonType } from '../../types/button';
import { Comment } from '../../types/comment'; // Assuming you have a Comment type

interface CommentModalProps {
  btnText: string;
  formik: FormikProps<Comment>;
  isOpen: boolean;
  onClose: () => void;
}

const CommentModal: React.FC<CommentModalProps> = ({
  btnText,
  formik,
  isOpen,
  onClose,
}) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <h4 className="mb-2 text-2xl font-semibold text-black">Edit Comment</h4>
      <form onSubmit={formik.handleSubmit} className="p-6">
        <VerticalStackLayout gap={4}>
          <FormControl label="Comment">
            <TextArea
              name="comment"
              onBlur={formik.handleBlur}
              onChange={formik.handleChange}
              placeholder="Enter your comment"
              rows={5}
              cols={30}
              value={formik.values.comment}
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

export default CommentModal;
