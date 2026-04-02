#!/usr/bin/env python3
"""Fix TransJakarta GTFS: deduplicate trip_ids, fill empty service_ids, fix fare_attributes."""
import zipfile, csv, os, tempfile, shutil

path = "data/raw/gtfs/transjakarta/transjakarta_gtfs.zip"
tmpdir = tempfile.mkdtemp()

with zipfile.ZipFile(path) as z:
    z.extractall(tmpdir)

# Fix trips.txt
trips_path = os.path.join(tmpdir, "trips.txt")
with open(trips_path) as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

print(f"Original trips: {len(rows)}")

for row in rows:
    if not row.get("service_id", "").strip():
        row["service_id"] = "weekday"

seen = set()
unique_rows = []
for row in rows:
    tid = row["trip_id"]
    if tid not in seen:
        seen.add(tid)
        unique_rows.append(row)

print(f"After dedup: {len(unique_rows)} (removed {len(rows) - len(unique_rows)})")

with open(trips_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(unique_rows)

# Fix fare_attributes.txt
fare_path = os.path.join(tmpdir, "fare_attributes.txt")
if os.path.exists(fare_path):
    with open(fare_path) as f:
        reader = csv.DictReader(f)
        fn = reader.fieldnames
        frows = list(reader)
    for row in frows:
        if not row.get("price", "").strip():
            row["price"] = "0"
    with open(fare_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fn)
        writer.writeheader()
        writer.writerows(frows)
    print("Fixed fare_attributes")

# Clean stop_times.txt
stop_times_path = os.path.join(tmpdir, "stop_times.txt")
if os.path.exists(stop_times_path):
    with open(stop_times_path) as f:
        reader = csv.DictReader(f)
        st_fn = reader.fieldnames
        st_rows = list(reader)
    orig = len(st_rows)
    st_rows = [r for r in st_rows if r["trip_id"] in seen]
    print(f"stop_times: {orig} -> {len(st_rows)}")
    with open(stop_times_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=st_fn)
        writer.writeheader()
        writer.writerows(st_rows)

# Repack
os.remove(path)
with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
    for fname in os.listdir(tmpdir):
        fpath = os.path.join(tmpdir, fname)
        if os.path.isfile(fpath):
            z.write(fpath, fname)

shutil.rmtree(tmpdir)
print("TransJakarta GTFS cleaned and repacked")
