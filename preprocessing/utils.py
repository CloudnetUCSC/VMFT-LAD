from datetime import datetime


def logTimestampToDateTime(month: str, day: str, time: str) -> datetime:
    month_code = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Nov": "11",
        "Dec": "12",
    }

    month = month.replace(" ", "")
    month = month.replace("\x00", "")

    log_timestamp = "2024 " + month_code[month] + " " + day + " " + time
    return datetime.strptime(log_timestamp, "%Y %m %d %H:%M:%S")
