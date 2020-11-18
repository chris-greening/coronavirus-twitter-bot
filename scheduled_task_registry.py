from scheduled_task import ScheduledTask
from update_numbers import get_daily_update

AUTO_TWEET_REGISTRY = (
    ScheduledTask(
        action=get_daily_update,
        hours=(20)
    )
)