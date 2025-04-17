"""
Reports and Analytics utilities for SIMRS
This module provides utility functions for report generation and data analysis.
"""
import os
import json
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime, timedelta
from flask import current_app, render_template
import tempfile
import sqlalchemy
from sqlalchemy import text
from app import db

def execute_report_query(query, params=None):
    """
    Execute a SQL query for report generation
    
    Args:
        query (str): SQL query string
        params (dict, optional): Query parameters
        
    Returns:
        list: List of dictionaries with query results
    """
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result.fetchall()]
            return {
                'success': True,
                'data': data,
                'columns': columns,
                'row_count': len(data)
            }
    except Exception as e:
        current_app.logger.error(f"Error executing report query: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'data': [],
            'columns': [],
            'row_count': 0
        }

def generate_chart(chart_type, data, labels, title=None, x_label=None, y_label=None, 
                   width=8, height=6, colors=None, **kwargs):
    """
    Generate a chart as base64 encoded image
    
    Args:
        chart_type (str): Type of chart ('bar', 'line', 'pie', 'scatter', etc.)
        data (list or dict): Chart data
        labels (list): Labels for data points
        title (str, optional): Chart title
        x_label (str, optional): X-axis label
        y_label (str, optional): Y-axis label
        width (int, optional): Chart width in inches
        height (int, optional): Chart height in inches
        colors (list, optional): Colors for the data series
        **kwargs: Additional chart options
        
    Returns:
        str: Base64 encoded image of the chart
    """
    try:
        plt.figure(figsize=(width, height))
        
        if chart_type == 'bar':
            if isinstance(data, dict):
                # Multiple series
                bar_width = 0.8 / len(data)
                positions = np.arange(len(labels))
                
                for i, (label, values) in enumerate(data.items()):
                    offset = i - (len(data) - 1) / 2
                    plt.bar(positions + offset * bar_width, values, 
                           width=bar_width, label=label, 
                           color=colors[i] if colors and i < len(colors) else None)
            else:
                # Single series
                plt.bar(labels, data, color=colors)
                
            plt.xticks(rotation=45, ha='right')
            
        elif chart_type == 'line':
            if isinstance(data, dict):
                # Multiple series
                for label, values in data.items():
                    plt.plot(labels, values, label=label)
            else:
                # Single series
                plt.plot(labels, data)
                
            plt.xticks(rotation=45, ha='right')
            
        elif chart_type == 'pie':
            plt.pie(data, labels=labels, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
            plt.axis('equal')
            
        elif chart_type == 'scatter':
            plt.scatter(data['x'], data['y'])
            
        elif chart_type == 'histogram':
            plt.hist(data, bins=kwargs.get('bins', 10))
            
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")
        
        if title:
            plt.title(title)
            
        if x_label:
            plt.xlabel(x_label)
            
        if y_label:
            plt.ylabel(y_label)
        
        if isinstance(data, dict) and len(data) > 1:
            plt.legend()
            
        plt.tight_layout()
        
        # Save chart to memory buffer
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        # Encode as base64
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
        
    except Exception as e:
        current_app.logger.error(f"Error generating chart: {str(e)}")
        return None

def format_report_data(data, format_type):
    """
    Format report data for different output formats
    
    Args:
        data (dict): Report data with columns and rows
        format_type (str): Output format (csv, json, html, etc.)
        
    Returns:
        tuple: (formatted_data, mime_type)
    """
    try:
        if format_type == 'json':
            result = json.dumps(data['data'], default=str, indent=2)
            return result, 'application/json'
            
        elif format_type == 'csv':
            output = BytesIO()
            writer = csv.DictWriter(output, fieldnames=data['columns'])
            writer.writeheader()
            writer.writerows(data['data'])
            return output.getvalue().decode('utf-8'), 'text/csv'
            
        elif format_type == 'html':
            # Simple HTML table
            rows = []
            rows.append('<table border="1">')
            
            # Header
            rows.append('<tr>')
            for col in data['columns']:
                rows.append(f'<th>{col}</th>')
            rows.append('</tr>')
            
            # Data rows
            for row in data['data']:
                rows.append('<tr>')
                for col in data['columns']:
                    rows.append(f'<td>{row[col]}</td>')
                rows.append('</tr>')
                
            rows.append('</table>')
            return ''.join(rows), 'text/html'
            
        elif format_type == 'excel':
            # Create a pandas DataFrame
            df = pd.DataFrame(data['data'])
            
            # Use a temporary file for Excel output
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
                df.to_excel(tmp.name, index=False)
                tmp_path = tmp.name
                
            with open(tmp_path, 'rb') as f:
                content = f.read()
                
            os.unlink(tmp_path)  # Delete the temporary file
            return content, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
            
    except Exception as e:
        current_app.logger.error(f"Error formatting report data: {str(e)}")
        return str(e), 'text/plain'

def generate_pdf_report(template_name, data, title=None, subtitle=None, logo_path=None):
    """
    Generate a PDF report using a template
    
    Args:
        template_name (str): Name of the template to use
        data (dict): Report data
        title (str, optional): Report title
        subtitle (str, optional): Report subtitle
        logo_path (str, optional): Path to logo image
        
    Returns:
        bytes: PDF content
    """
    try:
        from weasyprint import HTML
        
        # Render the template to HTML
        html_content = render_template(
            template_name,
            data=data,
            title=title,
            subtitle=subtitle,
            logo_path=logo_path,
            generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # Convert HTML to PDF
        pdf = HTML(string=html_content).write_pdf()
        return pdf
        
    except Exception as e:
        current_app.logger.error(f"Error generating PDF report: {str(e)}")
        return None

def calculate_date_range(period, custom_start=None, custom_end=None):
    """
    Calculate date range based on period
    
    Args:
        period (str): Period type (daily, weekly, monthly, quarterly, yearly, custom)
        custom_start (datetime, optional): Custom start date
        custom_end (datetime, optional): Custom end date
        
    Returns:
        tuple: (start_date, end_date)
    """
    today = datetime.now().date()
    
    if period == 'daily':
        return today, today
        
    elif period == 'weekly':
        # Start from Monday of current week
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)  # End on Sunday
        return start, end
        
    elif period == 'monthly':
        # Start from first day of current month
        start = today.replace(day=1)
        # End on last day of current month
        if today.month == 12:
            end = today.replace(day=31)
        else:
            end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        return start, end
        
    elif period == 'quarterly':
        # Determine current quarter
        quarter = (today.month - 1) // 3 + 1
        # Start from first day of current quarter
        start = datetime(today.year, 3 * quarter - 2, 1).date()
        # End on last day of current quarter
        if quarter == 4:
            end = datetime(today.year, 12, 31).date()
        else:
            end = datetime(today.year, 3 * quarter + 1, 1).date() - timedelta(days=1)
        return start, end
        
    elif period == 'yearly':
        # Start from first day of current year
        start = today.replace(month=1, day=1)
        # End on last day of current year
        end = today.replace(month=12, day=31)
        return start, end
        
    elif period == 'custom' and custom_start and custom_end:
        return custom_start, custom_end
        
    else:
        # Default to last 30 days
        return today - timedelta(days=30), today

def calculate_comparison(current_value, previous_value):
    """
    Calculate comparison between current and previous values
    
    Args:
        current_value (float): Current value
        previous_value (float): Previous value
        
    Returns:
        dict: Comparison data with absolute and percentage change
    """
    if previous_value == 0:
        percentage_change = 100 if current_value > 0 else 0
    else:
        percentage_change = ((current_value - previous_value) / abs(previous_value)) * 100
        
    return {
        'current': current_value,
        'previous': previous_value,
        'absolute_change': current_value - previous_value,
        'percentage_change': percentage_change,
        'direction': 'up' if current_value > previous_value else 'down' if current_value < previous_value else 'same'
    }

def get_report_template_variables():
    """
    Get available variables for report templates
    
    Returns:
        dict: Template variables with descriptions
    """
    return {
        'system': {
            'current_date': 'Current date (format: YYYY-MM-DD)',
            'current_time': 'Current time (format: HH:MM:SS)',
            'current_user': 'Username of the current user',
            'hospital_name': 'Name of the hospital',
            'report_period': 'Report period description',
        },
        'date_formats': {
            'format_date': 'Function to format date values',
            'format_datetime': 'Function to format datetime values',
            'format_time': 'Function to format time values',
        },
        'number_formats': {
            'format_number': 'Function to format numbers',
            'format_currency': 'Function to format currency values',
            'format_percentage': 'Function to format percentage values',
        },
        'data_access': {
            'data': 'The report data',
            'columns': 'List of column names',
            'row_count': 'Number of rows in the data',
            'chart_url': 'URL to the chart image (if applicable)',
        }
    }

def send_scheduled_report(report_id, recipients, subject=None, message=None):
    """
    Send a scheduled report via email
    
    Args:
        report_id (int): Report ID
        recipients (list): List of email recipients
        subject (str, optional): Email subject
        message (str, optional): Email message
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from flask_mail import Message
        from app import mail
        
        from models.reports import Report, ReportExport
        
        # Get report information
        report = Report.query.get(report_id)
        if not report:
            current_app.logger.error(f"Report not found: {report_id}")
            return False
            
        # Get latest report export
        export = ReportExport.query.filter_by(
            report_id=report_id,
            status='success'
        ).order_by(ReportExport.generated_at.desc()).first()
        
        if not export or not export.file_path:
            current_app.logger.error(f"No successful export found for report: {report_id}")
            return False
            
        # Create email
        email_subject = subject or f"Scheduled Report: {report.name}"
        email_body = message or f"Please find attached the scheduled report: {report.name}"
        
        msg = Message(
            subject=email_subject,
            recipients=recipients,
            body=email_body
        )
        
        # Attach the file
        with open(export.file_path, 'rb') as f:
            filename = os.path.basename(export.file_path)
            msg.attach(
                filename=filename,
                content_type=f"application/{export.format.value}",
                data=f.read()
            )
            
        # Send email
        mail.send(msg)
        current_app.logger.info(f"Scheduled report {report_id} sent to {recipients}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error sending scheduled report: {str(e)}")
        return False