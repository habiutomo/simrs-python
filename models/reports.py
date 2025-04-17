"""
Reports and Analytics models for SIMRS
This module defines models related to reports, analytics, and data visualization.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum, JSON, Date
from sqlalchemy.orm import relationship
import enum

from app import db

class ReportCategory(enum.Enum):
    OPERATIONAL = "operational"
    FINANCIAL = "financial" 
    CLINICAL = "clinical"
    INVENTORY = "inventory"
    HR = "hr"
    CUSTOM = "custom"
    RL1 = "rl1"  # Data Dasar Rumah Sakit
    RL2 = "rl2"  # Ketenagaan Rumah Sakit
    RL3 = "rl3"  # Pelayanan Rumah Sakit
    RL4 = "rl4"  # Morbiditas/Mortalitas
    RL5 = "rl5"  # Bulanan
    RL1 = "rl1"  # Data Dasar Rumah Sakit
    RL2 = "rl2"  # Ketenagaan Rumah Sakit
    RL3 = "rl3"  # Pelayanan Rumah Sakit
    RL4 = "rl4"  # Morbiditas/Mortalitas
    RL5 = "rl5"  # Bulanan

class ReportPeriod(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    CUSTOM = "custom"

class ReportFormat(enum.Enum):
    PDF = "pdf"
    EXCEL = "excel"
    CSV = "csv"
    HTML = "html"
    JSON = "json"

class ScheduleFrequency(enum.Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"

class Report(db.Model):
    """
    Report model for storing report definitions and metadata
    """
    __tablename__ = 'reports'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(Enum(ReportCategory), nullable=False)
    period = Column(Enum(ReportPeriod), nullable=False)
    formats = Column(String(100))  # Comma-separated list of formats
    query = Column(Text)  # SQL query or report definition
    parameters = Column(JSON)  # Report parameters
    start_date = Column(Date)  # For custom period
    end_date = Column(Date)  # For custom period
    created_by = Column(Integer)  # Reference to user who created the report
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    schedules = relationship("ReportSchedule", backref="report", lazy="dynamic")
    exports = relationship("ReportExport", backref="report", lazy="dynamic")
    
    def __repr__(self):
        return f"<Report {self.id} - {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category.value if self.category else None,
            'period': self.period.value if self.period else None,
            'formats': self.formats.split(',') if self.formats else [],
            'parameters': self.parameters,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'created_by': self.created_by,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'is_active': self.is_active
        }

class ReportSchedule(db.Model):
    """
    Report Schedule model for scheduling automated report generation
    """
    __tablename__ = 'report_schedules'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    frequency = Column(Enum(ScheduleFrequency), nullable=False)
    day_of_week = Column(Integer)  # 0-6, 0 is Monday (for weekly reports)
    day_of_month = Column(Integer)  # 1-31 (for monthly reports)
    time = Column(String(5))  # HH:MM format
    recipients = Column(Text)  # Comma-separated list of email addresses
    delivery_method = Column(String(20))  # email, download, both
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<ReportSchedule {self.id} for Report {self.report_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'frequency': self.frequency.value if self.frequency else None,
            'day_of_week': self.day_of_week,
            'day_of_month': self.day_of_month,
            'time': self.time,
            'recipients': self.recipients.split(',') if self.recipients else [],
            'delivery_method': self.delivery_method,
            'is_active': self.is_active,
            'last_run': self.last_run.strftime('%Y-%m-%d %H:%M:%S') if self.last_run else None,
            'next_run': self.next_run.strftime('%Y-%m-%d %H:%M:%S') if self.next_run else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class ReportExport(db.Model):
    """
    Report Export model for tracking report generation history
    """
    __tablename__ = 'report_exports'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(Integer, ForeignKey('reports.id'), nullable=False)
    format = Column(Enum(ReportFormat), nullable=False)
    file_path = Column(String(255))
    file_size = Column(Integer)  # Size in KB
    generated_by = Column(Integer)  # Reference to user or system
    generated_at = Column(DateTime, default=datetime.now)
    parameters = Column(JSON)  # Parameters used for this export
    status = Column(String(20))  # success, failed, processing
    error_message = Column(Text)
    is_scheduled = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<ReportExport {self.id} for Report {self.report_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'report_id': self.report_id,
            'format': self.format.value if self.format else None,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'generated_by': self.generated_by,
            'generated_at': self.generated_at.strftime('%Y-%m-%d %H:%M:%S') if self.generated_at else None,
            'parameters': self.parameters,
            'status': self.status,
            'error_message': self.error_message,
            'is_scheduled': self.is_scheduled
        }

class Dashboard(db.Model):
    """
    Dashboard model for storing custom dashboard configurations
    """
    __tablename__ = 'dashboards'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    layout = Column(JSON)  # Dashboard layout configuration
    is_default = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)
    owner_id = Column(Integer)  # Reference to user who created the dashboard
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    widgets = relationship("DashboardWidget", backref="dashboard", lazy="dynamic")
    
    def __repr__(self):
        return f"<Dashboard {self.id} - {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'layout': self.layout,
            'is_default': self.is_default,
            'is_public': self.is_public,
            'owner_id': self.owner_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class WidgetType(enum.Enum):
    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    TEXT = "text"
    MAP = "map"
    CUSTOM = "custom"

class DashboardWidget(db.Model):
    """
    Dashboard Widget model for storing widget configurations within dashboards
    """
    __tablename__ = 'dashboard_widgets'
    
    id = Column(Integer, primary_key=True)
    dashboard_id = Column(Integer, ForeignKey('dashboards.id'), nullable=False)
    name = Column(String(255), nullable=False)
    widget_type = Column(Enum(WidgetType), nullable=False)
    data_source = Column(String(255))  # SQL query, API endpoint, or report ID
    visualization = Column(String(50))  # Chart type, table format, etc.
    configuration = Column(JSON)  # Widget-specific configuration
    position_x = Column(Integer)  # X position in dashboard grid
    position_y = Column(Integer)  # Y position in dashboard grid
    width = Column(Integer, default=1)  # Widget width in grid units
    height = Column(Integer, default=1)  # Widget height in grid units
    refresh_interval = Column(Integer)  # In seconds, 0 for no auto-refresh
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<DashboardWidget {self.id} - {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'dashboard_id': self.dashboard_id,
            'name': self.name,
            'widget_type': self.widget_type.value if self.widget_type else None,
            'data_source': self.data_source,
            'visualization': self.visualization,
            'configuration': self.configuration,
            'position_x': self.position_x,
            'position_y': self.position_y,
            'width': self.width,
            'height': self.height,
            'refresh_interval': self.refresh_interval,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class DataExport(db.Model):
    """
    Data Export model for tracking data exports to external systems
    """
    __tablename__ = 'data_exports'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    export_type = Column(String(50))  # Type of export (report, raw data, etc.)
    destination = Column(String(255))  # Destination system or file path
    format = Column(Enum(ReportFormat), nullable=False)
    query = Column(Text)  # SQL query or data selection criteria
    parameters = Column(JSON)  # Export parameters
    schedule_id = Column(Integer, ForeignKey('report_schedules.id'))  # Optional schedule
    last_export_date = Column(DateTime)
    last_export_status = Column(String(20))
    last_export_message = Column(Text)
    created_by = Column(Integer)  # Reference to user
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    schedule = relationship("ReportSchedule", backref="data_exports")
    
    def __repr__(self):
        return f"<DataExport {self.id} - {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'export_type': self.export_type,
            'destination': self.destination,
            'format': self.format.value if self.format else None,
            'parameters': self.parameters,
            'schedule_id': self.schedule_id,
            'last_export_date': self.last_export_date.strftime('%Y-%m-%d %H:%M:%S') if self.last_export_date else None,
            'last_export_status': self.last_export_status,
            'last_export_message': self.last_export_message,
            'created_by': self.created_by,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class AnalyticsMetric(db.Model):
    """
    Analytics Metric model for tracking key performance indicators
    """
    __tablename__ = 'analytics_metrics'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # Metric category (financial, operational, clinical, etc.)
    calculation = Column(Text)  # SQL query or formula to calculate the metric
    unit = Column(String(20))  # Unit of measurement (%, days, currency, etc.)
    target_value = Column(Float)  # Target value for the metric
    warning_threshold = Column(Float)  # Threshold for warning
    critical_threshold = Column(Float)  # Threshold for critical alert
    trend_direction = Column(String(10))  # up or down (is up good or bad)
    is_active = Column(Boolean, default=True)
    display_on_dashboard = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    values = relationship("MetricValue", backref="metric", lazy="dynamic")
    
    def __repr__(self):
        return f"<AnalyticsMetric {self.id} - {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'calculation': self.calculation,
            'unit': self.unit,
            'target_value': self.target_value,
            'warning_threshold': self.warning_threshold,
            'critical_threshold': self.critical_threshold,
            'trend_direction': self.trend_direction,
            'is_active': self.is_active,
            'display_on_dashboard': self.display_on_dashboard,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class MetricValue(db.Model):
    """
    Metric Value model for storing historical values of metrics
    """
    __tablename__ = 'metric_values'
    
    id = Column(Integer, primary_key=True)
    metric_id = Column(Integer, ForeignKey('analytics_metrics.id'), nullable=False)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    status = Column(String(20))  # normal, warning, critical
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<MetricValue {self.id} for Metric {self.metric_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_id': self.metric_id,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'value': self.value,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }