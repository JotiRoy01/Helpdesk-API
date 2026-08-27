from django.db import transaction

from apps.audit.constants import AuditAction
from apps.audit.services import audit_ticket_action

from .models import Comment


# @transaction.atomic
# def create_comment(
#     *,
#     ticket,
#     author,
#     message,
# ):
#     return Comment.objects.create(
#         ticket=ticket,
#         author=author,
#         message=message.strip(),
#     )

@transaction.atomic
def create_comment(
    *,
    ticket,
    author,
    message,
    ip_address=None,
    user_agent="",
):
    comment = Comment.objects.create(
        ticket=ticket,
        author=author,
        message=message.strip(),
    )

    audit_ticket_action(
        actor=author,
        action=AuditAction.COMMENT_ADDED,
        ticket=ticket,
        new_value={
            "comment_id": str(comment.id),
        },
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return comment