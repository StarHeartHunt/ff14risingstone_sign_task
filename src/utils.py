from datetime import UTC, datetime, timezone, timedelta


def get_current_month():
    utc_dt = datetime.now(UTC)
    asia_shanghai_zone = timezone(timedelta(hours=8))
    asia_shanghai_now = utc_dt.astimezone(asia_shanghai_zone)
    month = asia_shanghai_now.strftime("%Y-%m")

    return month
