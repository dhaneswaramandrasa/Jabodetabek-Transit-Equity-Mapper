# KRL Commuterline GTFS — Construction Notes

**Generated**: 2026-03-21
**Method**: Manual construction from published schedules and OSM station data
**Feed validity**: 2026-01-01 to 2026-12-31

## Sources

- Station coordinates: OpenStreetMap + Google Maps cross-reference
- Schedule headways: GAPEKA 2025 published timetables
- Line structure: KAI Commuter official route map
- Community reference: github.com/comuline/api

## Lines

| Line | Stations | Peak headway | Off-peak headway |
|------|----------|-------------|------------------|
| Bogor | 24 | 8 min | 15 min |
| Cikarang | 20 | 10 min | 20 min |
| Rangkasbitung | 19 | 15 min | 30 min |
| Tangerang | 10 | 12 min | 20 min |
| Tanjung Priok | 4 | 15 min | 30 min |

## Limitations

- Schedules are approximated from published headways, not exact timetables
- Inter-station travel times use average values, not actual per-segment times
- Express/limited-stop services are not modeled
- Holiday schedules not included (calendar.txt has WEEKDAY/WEEKEND only)
- Nambo branch not modeled as separate trips (would need branching logic)
