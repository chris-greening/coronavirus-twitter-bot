"""
Registry of all the scheduled tasks to be performed by the bot
"""

from scheduled_task import ScheduledTask
from update_numbers import get_daily_update
from weekly_graphs import get_daily_infection_plot

SCHEDULED_TASK_REGISTRY = [
    ScheduledTask(
        task_function=get_daily_update,
        hours=[22]
    ),
    ScheduledTask(
        task_function=get_daily_infection_plot,
        weekdays=['Sunday'],
        hours=[9]
    )
]