# Duration

Represents a positive or negative span of time.

## Constructor
## duration

Creates a new duration.

You can specify the [duration](/docs/reference/foundations/duration/) using weeks, days, hours, minutes and seconds. You can also get a duration by subtracting two [datetimes](/docs/reference/foundations/datetime/).

```typst
#duration(
  days: 3,
  hours: 12,
).hours()
```

```typst
#duration(
  seconds: int,
  minutes: int,
  hours: int,
  days: int,
  weeks: int
) -> duration
```

### Parameters

- seconds:
  - description: The number of seconds.
  - type: int
  - default: 0
- minutes:
  - description: The number of minutes.
  - type: int
  - default: 0
- hours:
  - description: The number of hours.
  - type: int
  - default: 0
- days:
  - description: The number of days.
  - type: int
  - default: 0
- weeks:
  - description: The number of weeks.
  - type: int
  - default: 0


## Methods

## duration.seconds

The duration expressed in seconds.

This function returns the total duration represented in seconds as a floating-point number rather than the second component of the duration.

## duration.minutes

The duration expressed in minutes.

This function returns the total duration represented in minutes as a floating-point number rather than the second component of the duration.

## duration.hours

The duration expressed in hours.

This function returns the total duration represented in hours as a floating-point number rather than the second component of the duration.

## duration.days

The duration expressed in days.

This function returns the total duration represented in days as a floating-point number rather than the second component of the duration.

## duration.weeks

The duration expressed in weeks.

This function returns the total duration represented in weeks as a floating-point number rather than the second component of the duration.


