import uuid
from datetime import datetime

class BillingRecord:
    """Billing Record model for patient billing information"""
    
    def __init__(self, id=None, patient_id=None, visit_id=None, visit_type=None, 
                 items=None, total_amount=0, insurance_covered=0, patient_responsibility=0, 
                 status=None, issued_date=None, due_date=None, paid_date=None, 
                 payment_method=None, notes=None, created_at=None, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.patient_id = patient_id
        self.visit_id = visit_id  # ID of appointment or medical record
        self.visit_type = visit_type  # outpatient, inpatient, emergency, pharmacy, lab, etc.
        self.items = items or []
        self.total_amount = total_amount
        self.insurance_covered = insurance_covered
        self.patient_responsibility = patient_responsibility
        self.status = status or "pending"  # pending, paid, partially paid, cancelled
        self.issued_date = issued_date or datetime.now().isoformat()
        self.due_date = due_date
        self.paid_date = paid_date
        self.payment_method = payment_method
        self.notes = notes
        self.created_at = created_at or datetime.now().isoformat()
        
        # Add any additional fields from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def add_item(self, description, quantity, unit_price, item_type=None):
        """Add a billing item"""
        item = {
            "description": description,
            "quantity": quantity,
            "unit_price": unit_price,
            "total": quantity * unit_price,
            "item_type": item_type or "service"  # service, medication, lab, etc.
        }
        self.items.append(item)
        
        # Recalculate total amount
        self.calculate_totals()
    
    def calculate_totals(self):
        """Calculate billing totals"""
        self.total_amount = sum(item["total"] for item in self.items)
        
        # If there's insurance coverage, recalculate patient responsibility
        if self.insurance_covered > 0:
            self.patient_responsibility = max(0, self.total_amount - self.insurance_covered)
        else:
            self.patient_responsibility = self.total_amount
    
    def record_payment(self, amount, method):
        """Record a payment for this bill"""
        if not self.paid_date and amount >= self.patient_responsibility:
            self.status = "paid"
            self.paid_date = datetime.now().isoformat()
        elif amount > 0:
            self.status = "partially paid"
            
        self.payment_method = method
    
    def to_dict(self):
        """Convert billing record object to dictionary"""
        return self.__dict__
