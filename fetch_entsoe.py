import requests
from pathlib import Path
import os
from datetime import datetime, timedelta

TOKEN = os.environ.get("ENTSOE_TOKEN")
if not TOKEN:
    raise RuntimeError("ENTSOE_TOKEN ontbreekt")

end = datetime.utcnow().replace(hour=0, minute=0)
start = end - timedelta(days=1)

periodStart = start.strftime("%Y%m%d%H%M")
periodEnd   = end.strftime("%Y%m%d%H%M")

outdir = Path("raw/ENTSOE")
outdir.mkdir(parents=True, exist_ok=True)

params = {
    "securityToken": TOKEN,
    "documentType": "A78",
    "in_Domain": "10YNL----------L",
    "periodStart": periodStart,
    "periodEnd": periodEnd
}

r = requests.get(
    "https://transparency.entsoe.eu/api",
    params=params,
    headers={"Accept": "application/xml"},
    timeout=60
)
r.raise_for_status()

outfile = outdir / f"A78_NL_{periodStart}_{periodEnd}.xml"
outfile.write_text(r.text, encoding="utf-8")

print(f"Saved {outfile}")
