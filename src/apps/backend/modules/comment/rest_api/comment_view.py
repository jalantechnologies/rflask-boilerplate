from dataclasses import asdict

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.access_token.rest_api.access_auth_middleware import access_auth_middleware
from modules.comment.comment_service import CommentService
from modules.comment.errors import (
    CommentBadRequestError,
    CommentCreationError,
    CommentNotFoundError,
    CommentServiceError,
    CommentUpdateError,
)
from modules.comment.types import CreateCommentParams


class CommentView(MethodView):
    @access_auth_middleware
    def post(self) -> ResponseReturnValue:
        try:
            request_data = request.get_json()
            comment_params = CreateCommentParams(**request_data)
            comment = CommentService.create_comment(params=comment_params)
            comment_dict = asdict(comment)

            return jsonify(comment_dict), 201

        except CommentBadRequestError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except CommentCreationError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except Exception:
            return jsonify({"error": "Internal Server Error"}), 500

    @access_auth_middleware
    def get(self, task_id: str) -> ResponseReturnValue:
        try:
            comment_list = CommentService.get_comments_by_task_id(task_id=task_id)

            comment_dict_list = [
                {
                    "id": str(comment.id),
                    "task_id": str(comment.task_id),
                    "user_id": str(comment.user_id),
                    "content": comment.content,
                    "created_at": comment.created_at,
                    "updated_at": comment.updated_at,
                }
                for comment in comment_list
            ]

            return jsonify(comment_dict_list), 200

        except CommentNotFoundError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except CommentServiceError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except Exception as e:
            return jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500

    def put(self, comment_id: str):
        try:
            request_data = request.get_json()
            new_content = request_data.get("content")

            if not new_content:
                return jsonify({"error": "Content is required to update the comment"}), 400

            updated = CommentService.update_comment(comment_id=comment_id, new_content=new_content)

            if updated:
                return jsonify({"message": "Comment updated successfully"}), 200
            else:
                return jsonify({"error": "Comment update failed"}), 400

        except CommentUpdateError as e:
            return jsonify({"error": e.message}), e.http_status_code

        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
