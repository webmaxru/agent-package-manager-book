"""Record only a synthetic lifecycle event, never environment or path data."""
import json
from pathlib import Path
import sys

payload = json.load(sys.stdin)
event = payload.get("event", "unknown")
path = Path("events.json")
events = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
events.append(event)
path.write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
print("Recorded fixture event:", event)
if "--fail" in sys.argv:
    raise SystemExit(7)
