from datetime import datetime


ATTENDANCE_EXPORT_COLUMNS = [
    "Student Name",
    "Student ID",
    "Subject ID",
    "Subject Name",
    "Subject Code",
    "Teacher Name",
    "Timestamp",
    "Date",
    "Method",
    "AI Confidence Score",
    "Status",
]


def format_timestamp(value):
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime(
            "%Y-%m-%d %I:%M %p"
        )
    except (TypeError, ValueError):
        return str(value)


def build_attendance_csv(records):
    """Return complete per-student attendance records with a stable column set."""
    import pandas as pd

    dataframe = pd.DataFrame(records)
    complete = dataframe.reindex(columns=ATTENDANCE_EXPORT_COLUMNS)
    return complete.to_csv(index=False).encode("utf-8-sig")
