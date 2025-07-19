# Container Component

## Purpose
"Constrains the maximum width of page content, while keeping flexible margins for responsive layouts"
- Typically used to wrap main page content

## Sizing Properties
- Supports multiple predefined size options: "1", "2", "3", "4"
- Default size is set to "3"
- Sizes correspond to different maximum content widths:
  - Size "1": 448px
  - Size "2": 688px  
  - Size "3": 880px
  - Size "4": 1136px

## Responsive Behavior
- Adapts to different screen sizes
- Maintains flexible margins across various device widths
- Ensures content remains centered and readable

## Usage Example
```python
rx.container(
    # Content goes here
    size="3"  # Optional size parameter
)
```

## Key Features
- Part of Reflex's layout library
- Provides consistent content presentation
- Responsive across different screen sizes
- Automatic centering with flexible margins

Source: https://reflex.dev/docs/library/layout/container/