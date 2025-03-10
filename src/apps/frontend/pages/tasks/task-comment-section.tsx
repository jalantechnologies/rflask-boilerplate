import React, { useState } from 'react';

const CommentSection: React.FC<{ taskId: string }> = () => {
  const [comments, setComments] = useState<{ name: string; text: string }[]>(
    [],
  );
  const [newComment, setNewComment] = useState('');

  const handleAddComment = () => {
    if (!newComment.trim()) return;
    setComments([...comments, { name: 'User', text: newComment }]);
    setNewComment('');
  };

  return (
    <div className="mt-3 bg-gray-100  rounded-lg">
      <div className="space-y-2">
        {comments.map((comment, index) => (
          <div
            key={index}
            className="flex items-start space-x-2 bg-[#aba7a726] rounded-xl px-5 py-3"
          >
            <div className="w-8 h-8 bg-cyan-500 rounded-full flex items-center justify-center text-white font-bold">
              {comment.name[0]}
            </div>
            <div>
              <p className="text-md font-semibold text-black pb-2">
                {comment.name}
                <span className="text-[#808080] text-[11px] inline-block	pl-1 align-bottom">
                  17:30
                </span>
              </p>
              <p className="text-gray-600 text-md text-black">{comment.text}</p>
            </div>
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
    </div>
  );
};

export default CommentSection;
