# Center Component

## Purpose
Centers its children within itself using flex properties.

## Technical Details
- Based on the flex component
- Inherits all flex component props
- Provides flexible layout control for centering content both horizontally and vertically

## Key Properties
- **direction**: Can be "row" or "column"
- **align**: Options like "start" or "center"
- **justify**: Options like "start" or "center"  
- **wrap**: Options like "nowrap" or "wrap"
- **spacing**: Numeric values

## Usage Example
```python
rx.center(
    rx.text("Hello World!"),
    # Additional props inherited from flex
)
```

## Key Characteristic
"Centers its children within itself" using flex properties for alignment and positioning.

## Inheritance
Inherits all properties from the flex component, providing comprehensive layout control.

Source: https://reflex.dev/docs/library/layout/center/