# ICS Calendar Event Lister

A small Python script that fetches an `.ics` calendar subscription (including `webcal://` URLs), parses the events, and prints each event title with its start time converted to Central Time.

## Requirements

- Python 3.9+
- `requests`
- `icalendar`

Install dependencies with:

```bash
pip install requests icalendar
```

## Usage

```bash
python list_ics_events.py <source>
```

### Examples

Use a `webcal://` subscription URL:

```bash
python list_ics_events.py "webcal://example.com/calendar.ics"
```

Use a local `.ics` file:

```bash
python list_ics_events.py ./calendar.ics
```

## Output

Each event is printed on a single line as:

```text
<Event Title> - <Day>, <Mon> <DD> <HH:MM> <AM/PM>
```

Example:

```text
Practice - Tue, Apr 20 01:45 PM
```

## Notes

- `webcal://` URLs are automatically rewritten to `https://`.
- Event start times are converted to `America/Chicago` (Central Time).
- If the script cannot fetch or parse the calendar, it prints an error message and exits with status code `1`.
