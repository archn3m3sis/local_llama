# Reflex Styling Overview

Reflex styling system designed to be flexible, allowing developers to create consistent and customizable web applications.

## Three Main Styling Methods

### 1. Inline Styles
- Applied to individual component instances
- **Highest precedence**
- Can be set directly as props or using a `style` prop
- Children components inherit inline styles

### 2. Component Styles
- Set default styles for specific component types
- Allows creating consistent themes
- Can target specific CSS classes and IDs

### 3. Global Styles
- Applied to all components in the app
- Can set default font family, font size, etc.
- Useful for establishing base styling across the entire application

## Key Styling Features

- **Full CSS Support**: Supports complete CSS property range
- **Responsive Design**: Media queries support
- **Pseudo-styles**: Hover states and other pseudo-selectors
- **Theming**: Capabilities introduced in v0.4.0
- **Style Dictionaries**: Flexible implementation

## Style Inheritance and Precedence

- Style dictionaries can be layered
- Later styles override earlier ones
- Supports inheritance and specific component styling
- Integrated theme management through `Theme` and `Theme Panel` components

## Usage Examples

```python
# Inline styling
rx.box(
    background_color="blue",
    padding="1em",
    style={"border": "1px solid red"}
)

# Component styling through theme
# Global styling for entire app
```

## Best Practices

- Use inline styles for component-specific customization
- Leverage component styles for consistent theming
- Apply global styles for app-wide defaults

Source: https://reflex.dev/docs/styling/overview/