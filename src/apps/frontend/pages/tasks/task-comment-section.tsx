import React, { useState } from 'react';
import { Formik, FormikProps } from 'formik';
import MenuItem from '../../components/menu-item';
import { Button } from '../../components';
import { ButtonKind } from '../../types/button';
import { Comment } from '../../types/comment';
import CommentModal from './comment-modal';
import DeleteModal from '../../components/common/DeleteModal';

const CommentSection: React.FC<{ taskId: string }> = () => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedComment, setSelectedComment] = useState<Comment | null>(null);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  const handleAddComment = () => {
    if (!newComment.trim()) return;
    const newCommentObj = new Comment(
      (comments.length + 1).toString(),
      newComment,
    );
    setComments([...comments, newCommentObj]);
    setNewComment('');
  };

  const handleEditComment = (comment: Comment) => {
    setSelectedComment(comment);
    setIsModalOpen(true);
  };

  const handleSaveComment = (values: Comment) => {
    setComments((prevComments) =>
      prevComments.map((comment) =>
        comment.id === values.id ? { ...comment, text: values.text } : comment,
      ),
    );
    setIsModalOpen(false);
  };

  return (
    <div className="mt-3 bg-gray-100 rounded-lg p-4">
      <div className="space-y-2">
        {comments.map((comment) => (
          <div
            key={comment.id}
            className="flex items-start justify-between space-x-2 bg-[#aba7a726] rounded-xl px-5 py-3"
          >
            <div className="flex gap-3">
              <div className="w-8 h-8 bg-cyan-500 rounded-full flex items-center justify-center text-white font-bold">
                U
              </div>
              <div>
                <p className="text-md font-semibold text-black pb-2">
                  User
                  <span className="text-[#808080] text-[11px] inline-block pl-1 align-bottom">
                    17:30
                  </span>
                </p>
                <p className="text-gray-600 text-md text-black">
                  {comment.text}
                </p>
              </div>
            </div>

            <MenuItem>
              <Button
                kind={ButtonKind.SECONDARY}
                onClick={() => handleEditComment(comment)}
              >
                Edit
              </Button>
              <Button
                kind={ButtonKind.SECONDARY}
                onClick={() => setIsDeleteModalOpen(true)}
              >
                Delete
              </Button>
            </MenuItem>
          </div>
        ))}
      </div>

      <div className="flex items-center border rounded-lg overflow-hidden mt-5 pr-2">
        <input
          type="text"
          className="flex-1 p-3 outline-none"
          placeholder="Add a comment..."
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
        />
        <button
          onClick={handleAddComment}
          className="p-2 bg-blue-500 text-white rounded-lg"
        >
          ➤
        </button>
      </div>

      {isModalOpen && selectedComment && (
        <Formik
          initialValues={selectedComment}
          onSubmit={(values) => handleSaveComment(values)}
        >
          {(formik: FormikProps<Comment>) => (
            <CommentModal
              btnText="Update Comment"
              formik={formik}
              isOpen={isModalOpen}
              onClose={() => setIsModalOpen(false)}
            />
          )}
        </Formik>
      )}

      <DeleteModal
        isOpen={isDeleteModalOpen}
        onClose={() => setIsDeleteModalOpen(false)}
        onConfirm={() => {
          setIsDeleteModalOpen(false);
        }}
        title="Delete Comment"
        message="Are you sure you want to delete this comment? This action cannot be undone."
      />
    </div>
  );
};

export default CommentSection;
