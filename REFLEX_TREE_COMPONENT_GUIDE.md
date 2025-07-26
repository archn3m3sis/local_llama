# Reflex Tree Component Implementation Guide

## Overview
This guide explains how to properly implement recursive/nested tree components in Reflex, addressing common errors and providing working solutions.

## Common Errors and Solutions

### 1. "CustomVarOperation has no len()" Error
**Cause**: Missing or improper type annotations for nested data structures.

**Solution**: Always use proper type annotations:
```python
# Good
tree_data: List[Dict[str, Any]] = [...]
expanded_nodes: List[int] = []

# Bad
tree_data = []  # No type annotation
```

### 2. "Icon name must be a string" Error
**Cause**: Trying to use dynamic values for icon names.

**Solution**: Use conditional rendering with static icon names:
```python
# Bad
rx.icon(node["icon"])  # Dynamic icon name

# Good
rx.cond(
    node["type"] == "folder",
    rx.icon("folder", size=16),
    rx.icon("file", size=16)
)
```

### 3. Lambda Functions in Templates
**Cause**: Reflex doesn't support lambda functions in templates.

**Solution**: Create helper methods in state:
```python
# Bad
on_click=lambda: State.toggle(node_id)

# Good
def toggle_node(self, node_id: int):
    # implementation
# Then use: on_click=State.toggle_node(node_id)
```

## Working Tree Component Pattern

### 1. State Definition
```python
class TreeState(rx.State):
    # Properly typed tree data
    tree_data: List[Dict[str, Any]] = [
        {
            "id": 1,
            "name": "Root",
            "icon": "folder",
            "children": [
                {
                    "id": 2,
                    "name": "Child",
                    "icon": "file",
                    "children": []
                }
            ]
        }
    ]
    
    # Track expanded nodes
    expanded_nodes: List[int] = []
    
    def toggle_node(self, node_id: int):
        """Toggle node expansion."""
        if node_id in self.expanded_nodes:
            self.expanded_nodes.remove(node_id)
        else:
            self.expanded_nodes.append(node_id)
```

### 2. Recursive Component Function
```python
def render_tree_node(node: Dict[str, Any], level: int = 0) -> rx.Component:
    """Recursively render tree nodes."""
    node_id = node["id"]
    has_children = len(node.get("children", [])) > 0
    
    # Node display
    node_content = rx.hstack(
        # Indentation
        rx.box(width=f"{level * 20}px"),
        
        # Expand/collapse button
        rx.cond(
            has_children,
            rx.button(
                rx.cond(
                    TreeState.expanded_nodes.contains(node_id),
                    rx.icon("chevron-down", size=14),
                    rx.icon("chevron-right", size=14)
                ),
                on_click=lambda: TreeState.toggle_node(node_id),
                size="sm",
            ),
            rx.box(width="24px")
        ),
        
        # Icon (use static names)
        rx.icon("folder", size=16),
        
        # Label
        rx.text(node["name"]),
        
        spacing="2",
        align="center",
    )
    
    # Recursive children
    children = rx.cond(
        TreeState.expanded_nodes.contains(node_id) & has_children,
        rx.vstack(
            rx.foreach(
                node.get("children", []),
                lambda child: render_tree_node(child, level + 1)
            ),
            spacing="0",
        ),
        rx.box()
    )
    
    return rx.vstack(
        node_content,
        children,
        spacing="0",
    )
```

### 3. Main Tree Component
```python
def tree_view() -> rx.Component:
    """Main tree component."""
    return rx.box(
        rx.foreach(
            TreeState.tree_data,
            lambda node: render_tree_node(node, 0)
        ),
        padding="1rem",
    )
```

## Best Practices

### 1. Type Annotations
Always provide complete type annotations for state variables:
```python
# For complex nested structures
from typing import List, Dict, Any, Optional

directories: List[Dict[str, Any]] = []
current_directory_id: Optional[int] = None
```

### 2. List Operations
Use Reflex's list methods instead of Python operations:
```python
# Check if item in list
TreeState.expanded_nodes.contains(node_id)

# Get list length
TreeState.items.length()

# Convert to string
TreeState.count.to_string()
```

### 3. Conditional Rendering
Use `rx.cond` for all conditional UI:
```python
rx.cond(
    condition,
    true_component,
    false_component  # Optional
)
```

### 4. Event Handlers
Define methods in state class:
```python
class MyState(rx.State):
    def handle_click(self, item_id: int):
        # Handle the click
        pass

# Use in component
on_click=lambda: MyState.handle_click(item_id)
```

## Advanced Features

### 1. Breadcrumb Navigation
```python
def breadcrumbs() -> rx.Component:
    return rx.hstack(
        rx.foreach(
            DirectoryState.breadcrumbs,
            lambda crumb, idx: rx.fragment(
                rx.cond(
                    idx > 0,
                    rx.text("/", color="gray.600"),
                ),
                rx.button(
                    crumb["name"],
                    on_click=lambda: DirectoryState.navigate_to(crumb["id"]),
                    variant="ghost",
                    size="sm",
                ),
            )
        ),
        spacing="1",
    )
```

### 2. Search/Filter
```python
@rx.var
def filtered_tree(self) -> List[Dict[str, Any]]:
    """Computed var for filtered tree."""
    if not self.search_query:
        return self.tree_data
    
    # Filter logic here
    return filtered_data
```

### 3. Drag and Drop
Use Reflex's event system with proper state management:
```python
def handle_drop(self, source_id: int, target_id: int):
    """Handle drag and drop."""
    # Update tree structure in state
    pass
```

## Performance Considerations

1. **Use `rx.scroll_area` for large trees**:
```python
rx.scroll_area(
    tree_content,
    height="400px",
    scrollbars="vertical",
)
```

2. **Implement virtualization for very large trees** (future enhancement)

3. **Use computed vars for derived data**:
```python
@rx.var
def visible_nodes(self) -> List[Dict]:
    # Return only visible nodes based on expansion state
    pass
```

## Debugging Tips

1. **Check Type Annotations**: Most errors come from missing or incorrect types
2. **Use Static Values**: Icons, styles, and other properties should use static values
3. **Test with Simple Data**: Start with a simple tree structure and build up
4. **Check Browser Console**: Frontend errors often provide more details
5. **Use `print` Debugging**: Add print statements in state methods

## Example Implementation Files

- `/components/directory_tree_v2.py` - Full featured directory tree
- `/pages/directory_tree_demo.py` - Working demo with examples
- `/states/directory_state.py` - State management for tree data

## Common Patterns Summary

```python
# 1. Recursive component with proper typing
def render_node(node: Dict[str, Any], level: int = 0) -> rx.Component:
    return rx.vstack(
        # Node content
        render_node_content(node, level),
        # Recursive children
        rx.foreach(
            node.get("children", []),
            lambda child: render_node(child, level + 1)
        ),
    )

# 2. State with proper methods
class TreeState(rx.State):
    tree_data: List[Dict[str, Any]] = []
    expanded: List[int] = []
    
    def toggle(self, node_id: int):
        if node_id in self.expanded:
            self.expanded.remove(node_id)
        else:
            self.expanded.append(node_id)

# 3. Conditional rendering
rx.cond(
    TreeState.expanded.contains(node_id),
    rx.icon("chevron-down", size=14),
    rx.icon("chevron-right", size=14)
)
```

This pattern can be extended for any hierarchical data display in Reflex.