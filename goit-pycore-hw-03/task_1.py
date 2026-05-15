from datetime import datetime

def get_days_from_today(date: str) -> int:
    try:
        target = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Invalid date format: '{date}'. Expected 'YYYY-MM-DD'.")
    
    today = datetime.today().date()
    return (today - target).days

# Let's Test!
print(get_days_from_today("2021-10-09"))
print(get_days_from_today("1995-12-31"))
print(get_days_from_today("2222-4-23"))