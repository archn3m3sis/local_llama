# Reflex Responsive Design

Reflex provides flexible responsive design capabilities for creating adaptive interfaces across different device sizes.

## Key Features

- Style properties can be set with lists of values for different screen sizes
- Default breakpoints range from 0px to 96em
- Named breakpoint sizes: `xs`, `sm`, `md`, `lg`, `xl`
- Components can be conditionally displayed based on screen size

## Responsive Techniques

### 1. Responsive Values
"You can pass a list of values to any style property to specify its value on different screen sizes"

```python
# Text color changes based on screen size
rx.text(
    "Hello World", 
    color=[
        "orange",  # default
        "purple",  # from 48em
        "green"    # from 80em
    ]
)
```

### 2. Display Control
- Helper components allow showing/hiding content at different breakpoints
- Can specify custom display breakpoints using the `display` style property

### 3. Breakpoint Mapping
- Use `rx.breakpoints` to map screen sizes to specific values
- Granular control for creating adaptive interfaces

## Default Breakpoints

- **xs**: 0px
- **sm**: 30em (480px)
- **md**: 48em (768px)
- **lg**: 80em (1280px)
- **xl**: 96em (1536px)

## Best Practices

- Start with mobile-first design approach
- Use responsive values for critical layout properties
- Test across different screen sizes
- Leverage display control for conditional content

Source: https://reflex.dev/docs/styling/responsive/