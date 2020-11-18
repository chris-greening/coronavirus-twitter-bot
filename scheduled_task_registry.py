from scheduled_task import ScheduledTask
from update_numbers import get_daily_update

SCHEDULED_TASK_REGISTRY = (
    ScheduledTask(
        action=get_daily_update,
        hours=(20)
    )
)