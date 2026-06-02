.PHONY: build clean help deps

VENV_BIN := .venv/bin
PYINSTALLER := $(VENV_BIN)/pyinstaller
PYTHON := $(VENV_BIN)/python

# Hidden imports needed for the binary
HIDDEN_IMPORTS := --hidden-import=requests --hidden-import=icalendar \
                  --hidden-import=urllib3 --hidden-import=chardet \
                  --hidden-import=idna --hidden-import=certifi \
                  --hidden-import=dateutil

help:
	@echo "Available targets:"
	@echo "  make build          Build universal binary (x86_64 + arm64)"
	@echo "  make build-x86      Build x86_64 binary only"
	@echo "  make build-arm64    Build arm64 binary only"
	@echo "  make deps           Install/check all dependencies"
	@echo "  make clean          Remove build artifacts"

deps:
	@echo "Installing dependencies..."
	@$(PYTHON) -m pip install -q requests icalendar urllib3 chardet idna certifi python-dateutil pyinstaller
	@echo "✓ All dependencies installed"

build: deps clean build-x86 build-arm64
	@echo "Creating universal binary..."
	@mkdir -p dist
	@lipo -create dist_x86/list_ics_events_x86 dist_arm64/list_ics_events_arm64 -output dist/list_ics_events
	@rm -rf dist_x86 dist_arm64
	@echo "✓ Universal binary created: dist/list_ics_events"
	@file dist/list_ics_events

build-x86: deps clean
	@echo "Building x86_64 binary..."
	@$(PYINSTALLER) --onefile --target-arch=x86_64 $(HIDDEN_IMPORTS) \
		--specpath . --distpath dist_x86 \
		list_ics_events.py --name list_ics_events_x86
	@echo "✓ x86_64 binary created"

build-arm64: deps clean
	@echo "Building arm64 binary..."
	@$(PYINSTALLER) --onefile --target-arch=arm64 $(HIDDEN_IMPORTS) \
		--specpath . --distpath dist_arm64 \
		list_ics_events.py --name list_ics_events_arm64
	@echo "✓ arm64 binary created"

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build dist_x86 dist_arm64 *.spec
	@echo "✓ Build artifacts removed"
