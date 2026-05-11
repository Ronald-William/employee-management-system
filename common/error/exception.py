from fastapi import status

class NotFoundException(Exception):
    def __init__(self, employee_id: int):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = f"No record found with ID {employee_id}"
        super().__init__(self.detail)
    
class ConflictException(Exception):
    def __init__(self, field: str, value: str):
        self.status_code = status.HTTP_409_CONFLICT
        self.detail = f"A record with {field} '{value}' already exists"
        super().__init__(self.detail)

class AuthException(Exception):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = detail
        super().__init__(self.detail)

class ForbiddenException(Exception):
    def __init__(self):
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = "You do not have permission to perform this action."
        super().__init__(self.detail)
    
        