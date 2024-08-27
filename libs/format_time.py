"""
Holds the function for formatting times for st tables/charts
"""
from datetime import datetime as dt, timedelta
from zoneinfo import ZoneInfo

def format_time(dt_object: dt, local_tz: ZoneInfo) -> str:
    """
    Returns the correctly formatted date according to user's region -
    (Today or Yesterday, %I:%M AM or PM)
    """
    current_time = dt.now(local_tz)
    # finding date info
    local_time = dt_object.astimezone(local_tz)
    # formatting date as either today or yesterday w/ some logic
    if local_time.date() == current_time.date():
        day_label = "Today"
    elif local_time.date() == (current_time - timedelta(days=1)).date():
        day_label = "Yesterday"
    else:
        day_label = local_time.strftime('%B %d, %Y')

    time_str = local_time.strftime('%I:%M %p').lstrip('0')
    full_date = f"{day_label}, {time_str}"

    return full_date