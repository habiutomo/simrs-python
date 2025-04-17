"""
Payroll models for SIMRS
This module defines models related to employee payroll and compensation.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
import enum

from app import db

class PayrollStatus(enum.Enum):
    DRAFT = "draft"
    PROCESSED = "processed"
    PAID = "paid"
    CANCELLED = "cancelled"

class PayrollPeriod(db.Model):
    """
    Payroll Period model for managing payment periods
    """
    __tablename__ = 'payroll_periods'
    
    id = Column(Integer, primary_key=True)
    period_name = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    payment_date = Column(Date)
    is_locked = Column(Boolean, default=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    payroll_records = relationship("PayrollRecord", backref="period", lazy="dynamic")
    
    def __repr__(self):
        return f"<PayrollPeriod {self.period_name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'period_name': self.period_name,
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'payment_date': self.payment_date.strftime('%Y-%m-%d') if self.payment_date else None,
            'is_locked': self.is_locked,
            'description': self.description,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class PayrollRecord(db.Model):
    """
    Payroll Record model for employee salary records
    """
    __tablename__ = 'payroll_records'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    period_id = Column(Integer, ForeignKey('payroll_periods.id'), nullable=False)
    payroll_number = Column(String(50), unique=True)
    
    # Earnings
    basic_salary = Column(Float, default=0.0)
    overtime_pay = Column(Float, default=0.0)
    allowances = Column(Float, default=0.0)
    bonuses = Column(Float, default=0.0)
    incentives = Column(Float, default=0.0)
    other_earnings = Column(Float, default=0.0)
    
    # Deductions
    tax = Column(Float, default=0.0)
    health_insurance = Column(Float, default=0.0)
    pension = Column(Float, default=0.0)
    loans = Column(Float, default=0.0)
    other_deductions = Column(Float, default=0.0)
    
    # Totals
    gross_pay = Column(Float, default=0.0)
    total_deductions = Column(Float, default=0.0)
    net_pay = Column(Float, default=0.0)
    
    status = Column(Enum(PayrollStatus), default=PayrollStatus.DRAFT)
    processed_date = Column(DateTime)
    processed_by = Column(Integer)  # Reference to the user who processed
    payment_method = Column(String(50))
    payment_reference = Column(String(100))
    payment_date = Column(DateTime)
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    adjustments = relationship("PayrollAdjustment", backref="payroll_record", lazy="dynamic")
    
    def __repr__(self):
        return f"<PayrollRecord {self.payroll_number}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'period_id': self.period_id,
            'payroll_number': self.payroll_number,
            'basic_salary': self.basic_salary,
            'overtime_pay': self.overtime_pay,
            'allowances': self.allowances,
            'bonuses': self.bonuses,
            'incentives': self.incentives,
            'other_earnings': self.other_earnings,
            'tax': self.tax,
            'health_insurance': self.health_insurance,
            'pension': self.pension,
            'loans': self.loans,
            'other_deductions': self.other_deductions,
            'gross_pay': self.gross_pay,
            'total_deductions': self.total_deductions,
            'net_pay': self.net_pay,
            'status': self.status.value if self.status else None,
            'processed_date': self.processed_date.strftime('%Y-%m-%d %H:%M:%S') if self.processed_date else None,
            'processed_by': self.processed_by,
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'payment_date': self.payment_date.strftime('%Y-%m-%d %H:%M:%S') if self.payment_date else None,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def calculate_totals(self):
        """Calculate gross pay, total deductions, and net pay"""
        # Calculate gross pay
        self.gross_pay = (
            self.basic_salary +
            self.overtime_pay +
            self.allowances +
            self.bonuses +
            self.incentives +
            self.other_earnings
        )
        
        # Calculate total deductions
        self.total_deductions = (
            self.tax +
            self.health_insurance +
            self.pension +
            self.loans +
            self.other_deductions
        )
        
        # Calculate net pay
        self.net_pay = self.gross_pay - self.total_deductions
        
        return self.net_pay

class AdjustmentType(enum.Enum):
    ADDITION = "addition"
    DEDUCTION = "deduction"

class PayrollAdjustment(db.Model):
    """
    Payroll Adjustment model for additional earnings or deductions
    """
    __tablename__ = 'payroll_adjustments'
    
    id = Column(Integer, primary_key=True)
    payroll_record_id = Column(Integer, ForeignKey('payroll_records.id'), nullable=False)
    adjustment_type = Column(Enum(AdjustmentType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(255), nullable=False)
    applied_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)
    created_by = Column(Integer)  # Reference to the user who created
    
    def __repr__(self):
        return f"<PayrollAdjustment {self.id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'payroll_record_id': self.payroll_record_id,
            'adjustment_type': self.adjustment_type.value if self.adjustment_type else None,
            'amount': self.amount,
            'description': self.description,
            'applied_date': self.applied_date.strftime('%Y-%m-%d') if self.applied_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'created_by': self.created_by
        }

class Attendance(db.Model):
    """
    Employee Attendance Records
    """
    __tablename__ = 'attendances'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    date = Column(Date, nullable=False)
    clock_in = Column(DateTime)
    clock_out = Column(DateTime)
    total_hours = Column(Float)
    overtime_hours = Column(Float, default=0.0)
    status = Column(String(20))  # present, absent, leave, holiday
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    employee = relationship("Employee", backref="attendances")
    
    def __repr__(self):
        return f"<Attendance {self.id} - {self.employee_id} on {self.date}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'clock_in': self.clock_in.strftime('%Y-%m-%d %H:%M:%S') if self.clock_in else None,
            'clock_out': self.clock_out.strftime('%Y-%m-%d %H:%M:%S') if self.clock_out else None,
            'total_hours': self.total_hours,
            'overtime_hours': self.overtime_hours,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def calculate_hours(self):
        """Calculate total hours worked based on clock in and clock out"""
        if self.clock_in and self.clock_out:
            time_diff = self.clock_out - self.clock_in
            self.total_hours = time_diff.total_seconds() / 3600  # Convert to hours
            return self.total_hours
        return 0.0

class SalaryComponent(db.Model):
    """
    Salary Component model for defining salary structure components
    """
    __tablename__ = 'salary_components'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    component_type = Column(String(20), nullable=False)  # earnings, deductions
    description = Column(Text)
    is_taxable = Column(Boolean, default=False)
    is_fixed = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<SalaryComponent {self.name}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'component_type': self.component_type,
            'description': self.description,
            'is_taxable': self.is_taxable,
            'is_fixed': self.is_fixed,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class EmployeeSalaryStructure(db.Model):
    """
    Employee Salary Structure to define the salary components for an employee
    """
    __tablename__ = 'employee_salary_structures'
    
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date)
    total_salary = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    employee = relationship("Employee", backref="salary_structures")
    components = relationship("EmployeeSalaryComponent", backref="salary_structure", lazy="dynamic")
    
    def __repr__(self):
        return f"<EmployeeSalaryStructure {self.id} - {self.employee_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'effective_from': self.effective_from.strftime('%Y-%m-%d') if self.effective_from else None,
            'effective_to': self.effective_to.strftime('%Y-%m-%d') if self.effective_to else None,
            'total_salary': self.total_salary,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }

class EmployeeSalaryComponent(db.Model):
    """
    Employee Salary Component to define specific components in an employee's salary structure
    """
    __tablename__ = 'employee_salary_components'
    
    id = Column(Integer, primary_key=True)
    salary_structure_id = Column(Integer, ForeignKey('employee_salary_structures.id'), nullable=False)
    component_id = Column(Integer, ForeignKey('salary_components.id'), nullable=False)
    amount = Column(Float, nullable=False)
    percentage = Column(Float)  # If the component is a percentage of another component
    calculation_base = Column(String(100))  # Base for percentage calculation
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    component = relationship("SalaryComponent", backref="employee_components")
    
    def __repr__(self):
        return f"<EmployeeSalaryComponent {self.id} - {self.component_id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'salary_structure_id': self.salary_structure_id,
            'component_id': self.component_id,
            'amount': self.amount,
            'percentage': self.percentage,
            'calculation_base': self.calculation_base,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }