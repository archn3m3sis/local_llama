"""Export utilities for data export functionality."""
import reflex as rx
import pandas as pd
import json
from datetime import datetime
from io import BytesIO, StringIO
from typing import List, Dict, Any


def export_to_csv(data: List[Dict[str, Any]], filename_prefix: str = "export") -> rx.Component:
    """Export data to CSV format."""
    if not data:
        return rx.window_alert("No data to export")
    
    df = pd.DataFrame(data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.csv"
    
    return rx.download(
        data=csv_data.encode(),
        filename=filename
    )


def export_to_json(data: List[Dict[str, Any]], filename_prefix: str = "export") -> rx.Component:
    """Export data to JSON format."""
    if not data:
        return rx.window_alert("No data to export")
    
    json_data = json.dumps(data, indent=2, default=str)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.json"
    
    return rx.download(
        data=json_data.encode(),
        filename=filename
    )


def export_to_excel(data: List[Dict[str, Any]], filename_prefix: str = "export", sheet_name: str = "Data") -> rx.Component:
    """Export data to Excel format with formatting."""
    if not data:
        return rx.window_alert("No data to export")
    
    df = pd.DataFrame(data)
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Add some formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BD',
            'border': 1
        })
        
        # Write the column headers with the defined format
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Auto-adjust column widths
        for i, col in enumerate(df.columns):
            # Find the maximum length of the column
            max_len = df[col].astype(str).map(len).max()
            max_len = max(max_len, len(col)) + 2
            worksheet.set_column(i, i, min(max_len, 50))  # Cap at 50 chars width
    
    output.seek(0)
    excel_data = output.read()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.xlsx"
    
    return rx.download(
        data=excel_data,
        filename=filename
    )


def export_to_print(data: List[Dict[str, Any]], title: str = "Data Export") -> rx.Component:
    """Export data to printable HTML format."""
    if not data:
        return rx.window_alert("No data to export")
    
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a simple HTML table for printing
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{title} - {timestamp}</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                margin: 20px;
                color: #333;
            }}
            h1 {{ 
                text-align: center; 
                color: #2c3e50;
                margin-bottom: 10px;
            }}
            .info {{
                text-align: center;
                color: #7f8c8d;
                margin-bottom: 20px;
            }}
            table {{ 
                border-collapse: collapse; 
                width: 100%; 
                margin: 20px 0;
                box-shadow: 0 2px 3px rgba(0,0,0,0.1);
            }}
            th, td {{ 
                border: 1px solid #ddd; 
                padding: 12px 8px; 
                text-align: left; 
            }}
            th {{ 
                background-color: #3498db; 
                color: white;
                font-weight: bold; 
                position: sticky;
                top: 0;
            }}
            tr:nth-child(even) {{ 
                background-color: #f9f9f9; 
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            @media print {{
                body {{ margin: 0; }}
                h1 {{ page-break-after: avoid; }}
                table {{ page-break-inside: auto; }}
                tr {{ page-break-inside: avoid; page-break-after: auto; }}
                thead {{ display: table-header-group; }}
                tfoot {{ display: table-footer-group; }}
            }}
        </style>
        <script>
            window.onload = function() {{
                window.print();
                setTimeout(function() {{
                    window.close();
                }}, 1000);
            }}
        </script>
    </head>
    <body>
        <h1>{title}</h1>
        <div class="info">
            <p>Generated: {timestamp}</p>
            <p>Total Records: {len(data)}</p>
        </div>
        {df.to_html(index=False, table_id="data-table", escape=False)}
    </body>
    </html>
    """
    
    # Create a data URL and open in new window
    # We need to escape the HTML content properly for JavaScript
    escaped_html = html_content.replace('`', '\\`').replace('${', '\\${')
    
    return rx.call_script(
        f"""
        const printWindow = window.open('', '_blank', 'width=1000,height=800');
        printWindow.document.write(`{escaped_html}`);
        printWindow.document.close();
        """
    )