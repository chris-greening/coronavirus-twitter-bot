"""
Registry of all the scheduled tasks to be performed by the bot
"""

from scheduled_task import ScheduledTask
from update_numbers import get_daily_update
from weekly_graphs import get_daily_infection_plot

SCHEDULED_TASK_REGISTRY = [
    #Scrape daily infections/death data from Worldometers and tweet update
    ScheduledTask(
        task_function=get_daily_update,
        hours=[20]
    ),
    #Scrape graph from Worldometers and tweet the graph
    ScheduledTask(
        task_function=get_daily_infection_plot,
        weekdays=["Wednesday", "Sunday"],
        hours=[21]
    )
]
