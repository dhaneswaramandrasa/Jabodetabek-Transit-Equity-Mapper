# MRT Jakarta GTFS — Construction Notes

**Generated**: 2026-03-21
**Method**: Manual construction from published schedules and OSM station data
**Feed validity**: 2026-01-01 to 2026-12-31

## Line

- **North-South Phase 1**: Lebak Bulus Grab → Bundaran HI (13 stations)
- Peak headway: 5 min (06:00-09:00, 17:00-20:00)
- Off-peak headway: 10 min
- End-to-end time: ~24 min
- Operating hours: 05:00-24:00

## Sources

- Station coordinates: OpenStreetMap + jakartamrt.co.id
- Schedule: jakartamrt.co.id published timetable (2025-2026)
- Community reference: github.com/reksamamur/mrt-jakarta-api

## Limitations

- Phase 2 extension (Bundaran HI → Kota) not included (under construction)
- Exact per-segment travel times approximated with 2-min average
- Holiday schedules not included
- Fare data not encoded in GTFS (no fare_attributes.txt)
