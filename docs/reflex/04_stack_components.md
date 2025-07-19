# Stack Components

Flexible layout components for grouping elements in vertical or horizontal arrangements.

## Available Stack Components

1. **stack**: Flexible layout component for grouping elements
2. **vstack**: Vertical stack (column direction)
3. **hstack**: Horizontal stack (row direction)

## Key Properties

- **spacing**: Controls space between elements (values "0" to multiple levels)
- **direction**: Can be set to "row" or "column"
- **align**: Positioning options like "start", "center"
- **justify**: Alignment options like "start", "center"

## Default Behaviors

- `vstack` defaults to column direction
- `hstack` defaults to row direction
- Default spacing is typically set to "3"
- Default alignment is "start"

## Example Usage

```python
# Vertical stack
rx.vstack(
    rx.text("Item 1"),
    rx.text("Item 2"),
    spacing="4",
    align="center"
)

# Horizontal stack
rx.hstack(
    rx.button("Left"),
    rx.button("Right"),
    spacing="2",
    justify="center"
)
```

## Use Cases

- Stacking UI elements vertically or horizontally
- Creating flexible layouts with controlled spacing
- Aligning components within a container

## Technical Notes

- Based on flex components and inherit flex properties
- Provide versatile layout solution for responsive interfaces

Source: https://reflex.dev/docs/library/layout/stack/