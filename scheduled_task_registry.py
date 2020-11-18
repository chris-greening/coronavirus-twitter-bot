from scheduled_task import ScheduledTask
from update_numbers import get_daily_update

SCHEDULED_TASK_REGISTRY = [
    ScheduledTask(
        task_function=get_daily_update,
        hours=[22]
    )
]