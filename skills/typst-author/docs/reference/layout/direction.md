# Direction

The four directions into which content can be laid out.

Possible values are:

- `ltr`: Left to right.
- `rtl`: Right to left.
- `ttb`: Top to bottom.
- `btt`: Bottom to top.

These values are available globally and also in the direction type's scope, so you can write either of the following two:

```typst
#stack(dir: rtl)[A][B][C]
#stack(dir: direction.rtl)[A][B][C]
```


## Methods

## direction.from

Returns a direction from a starting point.

```typst
#direction.from(left) \
#direction.from(right) \
#direction.from(top) \
#direction.from(bottom)
```

```typst
#direction.from(
  side
) -> direction
```

### Parameters

- side:
  - description: 
  - type: alignment
  - default: None

## direction.to

Returns a direction from an end point.

```typst
#direction.to(left) \
#direction.to(right) \
#direction.to(top) \
#direction.to(bottom)
```

```typst
#direction.to(
  side
) -> direction
```

### Parameters

- side:
  - description: 
  - type: alignment
  - default: None

## direction.axis

The axis this direction belongs to, either `"horizontal"` or `"vertical"`.

```typst
#ltr.axis() \
#ttb.axis()
```

## direction.sign

The corresponding sign, for use in calculations.

```typst
#ltr.sign() \
#rtl.sign() \
#ttb.sign() \
#btt.sign()
```

## direction.start

The start point of this direction, as an alignment.

```typst
#ltr.start() \
#rtl.start() \
#ttb.start() \
#btt.start()
```

## direction.end

The end point of this direction, as an alignment.

```typst
#ltr.end() \
#rtl.end() \
#ttb.end() \
#btt.end()
```

## direction.inv

The inverse direction.

```typst
#ltr.inv() \
#rtl.inv() \
#ttb.inv() \
#btt.inv()
```


