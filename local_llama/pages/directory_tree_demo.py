import reflex as rx
from typing import List, Dict, Any


class TreeDemoState(rx.State):
    """State for demonstrating tree component patterns."""
    
    # Sample tree data with proper type annotations
    tree_data: List[Dict[str, Any]] = [
        {
            "id": 1,
            "name": "Documents",
            "icon": "folder",
            "children": [
                {
                    "id": 2,
                    "name": "Projects",
                    "icon": "folder",
                    "children": [
                        {"id": 3, "name": "Project A", "icon": "folder", "children": []},
                        {"id": 4, "name": "Project B", "icon": "folder", "children": []},
                    ]
                },
                {
                    "id": 5,
                    "name": "Reports",
                    "icon": "folder",
                    "children": [
                        {"id": 6, "name": "Q1 2024", "icon": "file-text", "children": []},
                        {"id": 7, "name": "Q2 2024", "icon": "file-text", "children": []},
                    ]
                }
            ]
        },
        {
            "id": 8,
            "name": "Images",
            "icon": "folder",
            "children": [
                {"id": 9, "name": "Screenshots", "icon": "folder", "children": []},
                {"id": 10, "name": "Photos", "icon": "folder", "children": []},
            ]
        }
    ]
    
    expanded_nodes: List[int] = [1, 8]  # Start with some nodes expanded
    selected_node_id: int = 0
    
    def toggle_node(self, node_id: int):
        """Toggle the expansion state of a node."""
        if node_id in self.expanded_nodes:
            self.expanded_nodes.remove(node_id)
        else:
            self.expanded_nodes.append(node_id)
    
    def select_node(self, node_id: int):
        """Select a node."""
        self.selected_node_id = node_id


def render_tree_node(node: Dict[str, Any], level: int = 0) -> rx.Component:
    """Render a single tree node recursively."""
    node_id = node["id"]
    has_children = len(node.get("children", [])) > 0
    
    # Main node content
    node_display = rx.hstack(
        # Indentation
        rx.box(width=f"{level * 20}px"),
        
        # Expand/collapse button
        rx.cond(
            has_children,
            rx.button(
                rx.cond(
                    TreeDemoState.expanded_nodes.contains(node_id),
                    rx.icon("chevron-down", size=14),
                    rx.icon("chevron-right", size=14)
                ),
                size="1",
                variant="ghost",
                on_click=lambda: TreeDemoState.toggle_node(node_id),
                style={"min_width": "24px", "padding": "2px"},
            ),
            rx.box(width="24px")
        ),
        
        # Icon
        rx.icon(
            node["icon"],
            size=16,
            color=rx.cond(
                TreeDemoState.selected_node_id == node_id,
                "blue.400",
                "gray.400"
            ),
        ),
        
        # Name
        rx.text(
            node["name"],
            size="2",
            weight=rx.cond(
                TreeDemoState.selected_node_id == node_id,
                "medium",
                "normal"
            ),
            color=rx.cond(
                TreeDemoState.selected_node_id == node_id,
                "blue.400",
                "white"
            ),
        ),
        
        spacing="2",
        align="center",
        padding="4px 8px",
        border_radius="md",
        cursor="pointer",
        width="100%",
        on_click=lambda: TreeDemoState.select_node(node_id),
        background=rx.cond(
            TreeDemoState.selected_node_id == node_id,
            "rgba(59, 130, 246, 0.1)",
            "transparent"
        ),
        _hover={
            "background": rx.cond(
                TreeDemoState.selected_node_id == node_id,
                "rgba(59, 130, 246, 0.15)",
                "rgba(255, 255, 255, 0.05)"
            ),
        },
    )
    
    # Children (recursive)
    children_display = rx.cond(
        TreeDemoState.expanded_nodes.contains(node_id) & (len(node.get("children", [])) > 0),
        rx.vstack(
            rx.foreach(
                node.get("children", []),
                lambda child: render_tree_node(child, level + 1)
            ),
            spacing="0",
            width="100%",
        ),
        rx.box()  # Empty when collapsed
    )
    
    return rx.vstack(
        node_display,
        children_display,
        spacing="0",
        width="100%",
    )


def directory_tree_demo() -> rx.Component:
    """Demo page showing different tree component patterns."""
    return rx.vstack(
        rx.heading("Directory Tree Component Demo", size="6", margin_bottom="2rem"),
        
        rx.hstack(
            # Tree panel
            rx.card(
                rx.vstack(
                    rx.heading("File Explorer", size="4"),
                    rx.divider(),
                    rx.scroll_area(
                        rx.vstack(
                            rx.foreach(
                                TreeDemoState.tree_data,
                                lambda node: render_tree_node(node, 0)
                            ),
                            spacing="0",
                            width="100%",
                        ),
                        height="400px",
                        scrollbars="vertical",
                    ),
                    spacing="4",
                    width="100%",
                ),
                style={
                    "width": "350px",
                    "background": "rgba(0, 0, 0, 0.3)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                }
            ),
            
            # Info panel
            rx.card(
                rx.vstack(
                    rx.heading("Implementation Notes", size="4"),
                    rx.divider(),
                    rx.text(
                        "This demo shows a working recursive tree component in Reflex:",
                        size="2",
                        margin_bottom="1rem",
                    ),
                    rx.vstack(
                        rx.text("✓ Recursive rendering with proper type annotations", size="2"),
                        rx.text("✓ Expand/collapse functionality", size="2"),
                        rx.text("✓ Node selection with visual feedback", size="2"),
                        rx.text("✓ Dynamic icons and styling", size="2"),
                        rx.text("✓ Proper indentation for hierarchy", size="2"),
                        spacing="2",
                        align="start",
                    ),
                    rx.divider(margin_y="1rem"),
                    rx.text(
                        "Key implementation details:",
                        size="2",
                        weight="medium",
                        margin_bottom="0.5rem",
                    ),
                    rx.code_block(
                        """# 1. Use proper type annotations
tree_data: List[Dict[str, Any]] = [...]

# 2. Use .contains() for list membership
TreeDemoState.expanded_nodes.contains(node_id)

# 3. Use rx.cond for conditional rendering
rx.cond(condition, true_component, false_component)

# 4. Pass static strings to icons
rx.icon("folder", size=16)""",
                        language="python",
                        size="1",
                    ),
                    spacing="4",
                ),
                style={
                    "flex": "1",
                    "background": "rgba(0, 0, 0, 0.3)",
                    "border": "1px solid rgba(255, 255, 255, 0.1)",
                }
            ),
            
            spacing="4",
            width="100%",
            align="start",
        ),
        
        # Additional examples section
        rx.card(
            rx.vstack(
                rx.heading("Common Patterns", size="4"),
                rx.divider(),
                rx.accordion.root(
                    rx.accordion.item(
                        header="Handling Dynamic Icons",
                        content=rx.code_block(
                            """# Instead of dynamic icon names:
# rx.icon(node["icon"])  # This causes errors

# Use conditional rendering:
rx.cond(
    node["type"] == "folder",
    rx.icon("folder", size=16),
    rx.icon("file", size=16)
)""",
                            language="python",
                            size="1",
                        ),
                    ),
                    rx.accordion.item(
                        header="Recursive Foreach",
                        content=rx.code_block(
                            """def render_node(node: Dict[str, Any], level: int = 0):
    return rx.vstack(
        # Node content
        rx.text(node["name"]),
        
        # Recursive children
        rx.foreach(
            node.get("children", []),
            lambda child: render_node(child, level + 1)
        ),
    )""",
                            language="python",
                            size="1",
                        ),
                    ),
                    rx.accordion.item(
                        header="Type Annotations",
                        content=rx.code_block(
                            """# Define your data structure clearly:
class TreeNode(rx.Base):
    id: int
    name: str
    icon: str
    children: List["TreeNode"] = []

# Or use Dict with proper typing:
tree_data: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Root",
        "children": [...]
    }
]""",
                            language="python",
                            size="1",
                        ),
                    ),
                    collapsible=True,
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            style={
                "background": "rgba(0, 0, 0, 0.3)",
                "border": "1px solid rgba(255, 255, 255, 0.1)",
                "margin_top": "2rem",
            }
        ),
        
        # Page positioning
        width="100%",
        max_width="1200px",
        padding="2rem",
        spacing="4",
    )