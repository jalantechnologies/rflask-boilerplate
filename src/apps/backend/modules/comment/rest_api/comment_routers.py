from flask import Blueprint

from modules.comment.rest_api.comment_view import CommentView


class CommentRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule("/comments", view_func=CommentView.as_view("create_comment"), methods=["POST"])
        blueprint.add_url_rule(
            "/comments/<task_id>", view_func=CommentView.as_view("get_comments_by_task"), methods=["GET"]
        )
        blueprint.add_url_rule(
            "/comments/<string:comment_id>", view_func=CommentView.as_view("comment_view_update"), methods=["PUT"]
        )
        return blueprint
