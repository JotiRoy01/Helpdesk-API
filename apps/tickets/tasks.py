from celery import shared_task

from .overdue import OverdueTicketService


@shared_task
def process_overdue_tickets():
    return OverdueTicketService.count()
