# Datetime

Represents a date, a time, or a combination of both.

Can be created by either specifying a custom datetime using this type's constructor function or getting the current date with [`datetime.today`](/docs/reference/foundations/datetime/#definitions-today).

## Example

```typst
#let date = datetime(
  year: 2020,
  month: 10,
  day: 4,
)

#date.display() \
#date.display(
  "y:[year repr:last_two]"
)

#let time = datetime(
  hour: 18,
  minute: 2,
  second: 23,
)

#time.display() \
#time.display(
  "h:[hour repr:12][period]"
)
```

## Datetime and Duration

You can get a [duration](/docs/reference/foundations/duration/) by subtracting two datetime:

```typst
#let first-of-march = datetime(day: 1, month: 3, year: 2024)
#let first-of-jan = datetime(day: 1, month: 1, year: 2024)
#let distance = first-of-march - first-of-jan
#distance.hours()
```

You can also add/subtract a datetime and a duration to retrieve a new, offset datetime:

```typst
#let date = datetime(day: 1, month: 3, year: 2024)
#let two-days = duration(days: 2)
#let two-days-earlier = date - two-days
#let two-days-later = date + two-days

#date.display() \
#two-days-earlier.display() \
#two-days-later.display()
```

## Format

You can specify a customized formatting using the [`display`](/docs/reference/foundations/datetime/#definitions-display) method. The format of a datetime is specified by providing _components_ with a specified number of _modifiers_. A component represents a certain part of the datetime that you want to display, and with the help of modifiers you can define how you want to display that component. In order to display a component, you wrap the name of the component in square brackets (e.g. `[year]` will display the year). In order to add modifiers, you add a space after the component name followed by the name of the modifier, a colon and the value of the modifier (e.g. `[month repr:short]` will display the short representation of the month).

The possible combination of components and their respective modifiers is as follows:

- `year`: Displays the year of the datetime. 
  - `padding`: Can be either `zero`, `space` or `none`. Specifies how the year is padded.
  - `repr` Can be either `full` in which case the full year is displayed or `last_two` in which case only the last two digits are displayed.
  - `sign`: Can be either `automatic` or `mandatory`. Specifies when the sign should be displayed.
- `month`: Displays the month of the datetime. 
  - `padding`: Can be either `zero`, `space` or `none`. Specifies how the month is padded.
  - `repr`: Can be either `numerical`, `long` or `short`. Specifies if the month should be displayed as a number or a word. Unfortunately, when choosing the word representation, it can currently only display the English version. In the future, it is planned to support localization.
- `day`: Displays the day of the datetime. 
  - `padding`: Can be either `zero`, `space` or `none`. Specifies how the day is padded.
- `week_number`: Displays the week number of the datetime. 
  - `padding`: Can be either `zero`, `space` or `none`. Specifies how the week number is padded.
  - `repr`: Can be either `ISO`, `sunday` or `monday`. In the case of `ISO`, week numbers are between 1 and 53, while the other ones are between 0 and 53.
- `weekday`: Displays the weekday of the date. 
  - `repr` Can be either `long`, `short`, `sunday` or `monday`. In the case of `long` and `short`, the corresponding English name will be displayed (same as for the month, other languages are currently not supported). In the case of `sunday` and `monday`, the numerical value will be displayed (assuming Sunday and Monday as the first day of the week, respectively).
  - `one_indexed`: Can be either `true` or `false`. Defines whether the numerical representation of the week starts with 0 or 1.
- `hour`: Displays the hour of the date. 
  - `padding`: Can be either `zero`, `space` or `none`. Specifies how the hour is padded.
  - `repr`: Can be either `24` or `12`. Changes whether the hour is displayed in the 24-hour or 12-hour format.
- `period`: The AM/PM part of the hour 
  - `case`: Can be `lower` to display it in lower case and `upper` to display it in upper case.
- `minute`: Displays the minute of the date. 
  - `padding`: Can be either `zero`, `space` or `none`. Specifies how the minute is padded.
- `second`: Displays the second of the date. 
  - `padding`: Can be either `zero`, `space` or `none`. Specifies how the second is padded.

Keep in mind that not always all components can be used. For example, if you create a new datetime with `datetime(year: 2023, month: 10, day: 13)`, it will be stored as a plain date internally, meaning that you cannot use components such as `hour` or `minute`, which would only work on datetimes that have a specified time.

## Constructor
## datetime

Creates a new datetime.

You can specify the [datetime](/docs/reference/foundations/datetime/) using a year, month, day, hour, minute, and second.

_Note_: Depending on which components of the datetime you specify, Typst will store it in one of the following three ways:

- If you specify year, month and day, Typst will store just a date.
- If you specify hour, minute and second, Typst will store just a time.
- If you specify all of year, month, day, hour, minute and second, Typst will store a full datetime.

Depending on how it is stored, the [`display`](/docs/reference/foundations/datetime/#definitions-display) method will choose a different formatting by default.

```typst
#datetime(
  year: 2012,
  month: 8,
  day: 3,
).display()
```

```typst
#datetime(
  year: int,
  month: int,
  day: int,
  hour: int,
  minute: int,
  second: int
) -> datetime
```

### Parameters

- year:
  - description: The year of the datetime.
  - type: int
  - default: None
- month:
  - description: The month of the datetime.
  - type: int
  - default: None
- day:
  - description: The day of the datetime.
  - type: int
  - default: None
- hour:
  - description: The hour of the datetime.
  - type: int
  - default: None
- minute:
  - description: The minute of the datetime.
  - type: int
  - default: None
- second:
  - description: The second of the datetime.
  - type: int
  - default: None


## Methods

## datetime.today

Returns the current date.

In the CLI, this can be overridden with the `--creation-timestamp` argument or by setting the [`SOURCE_DATE_EPOCH`](https://reproducible-builds.org/specs/source-date-epoch/) environment variable. In both cases, the value should be given as a UNIX timestamp.

```typst
Today's date is
#datetime.today().display().
```

```typst
#datetime.today(
  offset: auto | int
) -> datetime
```

### Parameters

- offset:
  - description: An offset to apply to the current UTC date. If set to `auto`, the offset will be the local offset.
  - type: auto | int
  - default: auto

## datetime.display

Displays the datetime in a specified format.

Depending on whether you have defined just a date, a time or both, the default format will be different. If you specified a date, it will be `[year]-[month]-[day]`. If you specified a time, it will be `[hour]:[minute]:[second]`. In the case of a datetime, it will be `[year]-[month]-[day] [hour]:[minute]:[second]`.

See the [format syntax](/docs/reference/foundations/datetime/#format) for more information.

```typst
#datetime.display(
  pattern
) -> str
```

### Parameters

- pattern:
  - description: The format used to display the datetime.
  - type: auto | str
  - default: auto

## datetime.year

The year if it was specified, or `none` for times without a date.

## datetime.month

The month if it was specified, or `none` for times without a date.

## datetime.weekday

The weekday (counting Monday as 1) or `none` for times without a date.

## datetime.day

The day if it was specified, or `none` for times without a date.

## datetime.hour

The hour if it was specified, or `none` for dates without a time.

## datetime.minute

The minute if it was specified, or `none` for dates without a time.

## datetime.second

The second if it was specified, or `none` for dates without a time.

## datetime.ordinal

The ordinal (day of the year), or `none` for times without a date.


