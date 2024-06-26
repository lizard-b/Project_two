import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.runapsheduler_tasks import *

logger = logging.getLogger(__name__)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            posts_weekly_notification,
            trigger=CronTrigger(day_of_week='wed', hour='11', minute='30'),
            # То же, что и интервал, но задача триггера таким образом более понятна django
            id="post_weekly_notif",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'posts_weekly_notification'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week='wed', hour='11', minute='30'
            ),
            # Каждую неделю будут удаляться старые задачи, которые
            # либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
