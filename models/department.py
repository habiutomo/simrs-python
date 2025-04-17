import uuid

class Department:
    """Department model for hospital departments"""
    
    def __init__(self, id=None, name=None, code=None, description=None, 
                 location=None, head_doctor_id=None, **kwargs):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.code = code
        self.description = description
        self.location = location
        self.head_doctor_id = head_doctor_id
        
        # Add any additional fields from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def to_dict(self):
        """Convert department object to dictionary"""
        return self.__dict__
