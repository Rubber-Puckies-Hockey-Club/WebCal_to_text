#!/usr/bin/env python3
import argparse
from datetime import datetime, time
from zoneinfo import ZoneInfo
from urllib.parse import urlparse

import requests
from icalendar import Calendar, vDate, vDatetime


def load_ics(source: str) -> bytes:
    parsed = urlparse(source)
    scheme = parsed.scheme.lower()
    if scheme == "webcal":
        source = source.replace("webcal://", "https://", 1)
        scheme = "https"
    if scheme in ("http", "https"):
        response = requests.get(source, timeout=20)
        response.raise_for_status()
        return response.content
    with open(source, "rb") as f:
        return f.read()


CENTRAL_TZ = ZoneInfo("America/Chicago")
UTC_TZ = ZoneInfo("UTC")


def normalize_datetime(value):
    if value is None:
        return None
    if isinstance(value, vDatetime):
        value = value.dt
    elif isinstance(value, vDate):
        value = datetime.combine(value.dt, time.min)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC_TZ)
        return value
    return value


def format_dt(value):
    if value is None:
        return ""
    if isinstance(value, datetime):
        central = value.astimezone(CENTRAL_TZ)
        return central.strftime("%a, %b %d %I:%M %p")
    return str(value)


def parse_events(ics_data: bytes):
    calendar = Calendar.from_ical(ics_data)
    events = []
    for component in calendar.walk():
        if component.name != "VEVENT":
            continue
        dtstart = normalize_datetime(component.get("dtstart").dt if component.get("dtstart") else None)
        dtend = normalize_datetime(component.get("dtend").dt if component.get("dtend") else None)
        summary = str(component.get("summary", "(No title)"))
        location = str(component.get("location", "")).strip()
        description = str(component.get("description", "")).strip()
        uid = str(component.get("uid", "")).strip()
        events.append({
            "summary": summary,
            "start": dtstart,
            "end": dtend,
            "location": location,
            "description": description,
            "uid": uid,
        })
    events.sort(key=lambda e: (e["start"] or datetime.max))
    return events


def main():
    parser = argparse.ArgumentParser(description="List events from an .ics calendar subscription.")
    parser.add_argument("source", help="URL or local .ics file path")
    parser.add_argument("--limit", type=int, default=0, help="Maximum events to show (0 = all)")
    args = parser.parse_args()

    ics_data = load_ics(args.source)
    events = parse_events(ics_data)

    if not events:
        print("No events found.")
        return

    max_events = args.limit if args.limit > 0 else len(events)
    for event in events[:max_events]:
        title = event['summary']
        start = format_dt(event['start'])
        print(f"{title} - {start}")


if __name__ == "__main__":
    main()
