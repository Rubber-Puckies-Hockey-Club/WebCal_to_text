# ICS Calendar Event Lister

A small Python script that fetches an `.ics` calendar subscription (including `webcal://` URLs), parses the events, and prints each event title with its start time converted to Central Time.

## Requirements

### For Python Script
- Python 3.9+
- `requests`
- `icalendar`

Install Python dependencies with:

```bash
pip install requests icalendar
```

### For Building the Universal Binary
- macOS with both Intel and Apple Silicon support (or Rosetta 2)
- Python 3.9+ (same as above)
- `pyinstaller`
- All dependencies listed above

Install all build dependencies via the virtual environment set up in the project.


## Usage

### Python Script

```bash
python list_ics_events.py <source>
```

### Compiled Universal Binary (macOS)

A precompiled universal binary is available in `dist/list_ics_events`. It works on both Intel and Apple Silicon Macs:

```bash
./dist/list_ics_events <source>
```

### Examples

Use a `webcal://` subscription URL:

```bash
python list_ics_events.py "webcal://example.com/calendar.ics"
# or
./dist/list_ics_events "webcal://example.com/calendar.ics"
```

Use a local `.ics` file:

```bash
python list_ics_events.py ./calendar.ics
# or
./dist/list_ics_events ./calendar.ics
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

## Building the Universal Binary

The `dist/list_ics_events` binary includes support for both Intel (x86_64) and Apple Silicon (arm64) architectures.

### Quick Rebuild

Use the included `Makefile`:

```bash
make build
```

This will:
1. Build x86_64 binary
2. Build arm64 binary  
3. Combine them into a universal binary at `dist/list_ics_events`

### Manual Build

If you prefer to build manually without Make:

```bash
# Install build dependencies
pip install pyinstaller

# Build for both architectures and combine
make build
```

### Clean Build

To remove build artifacts and start fresh:

```bash
make clean
```

## Notes

- `webcal://` URLs are automatically rewritten to `https://`.
- Event start times are converted to `America/Chicago` (Central Time).
- If the script cannot fetch or parse the calendar, it prints an error message and exits with status code `1`.
- The universal binary includes all Python dependencies, so no additional packages need to be installed.
- Minor OpenSSL warnings from urllib3 can be safely ignored.
