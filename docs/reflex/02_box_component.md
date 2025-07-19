# Box Component

## Overview
A generic container component based on a `<div>` element, primarily used for applying styles. Rendered as a block-level element by default.

## Primary Use Case
"Box is a generic container component that can be used to group other components."

## Styling Properties Available
- **Background**: CSS colors (yellow, orange), Radix Colors, Radix Theme Colors
- **Background Types**: Solid colors, gradients (linear and radial), background images
- **Border**: Border radius customizable
- **Spacing**: Width, margin, padding adjustable

## Example Styling
```python
rx.box(
    # content,
    background_color="yellow",
    border_radius="2px",
    width="20%",
    margin="4px",
    padding="4px"
)
```

## Props
- No component-specific props
- Inherits standard event triggers from base elements

## Key Features
- Highly flexible for layout and styling purposes
- Foundation for other layout components
- Supports CSS styling system

Source: https://reflex.dev/docs/library/layout/box/