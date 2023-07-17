from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]
    
    
external_data = {
    'id': 123,
    'signup_ts': '2019-06-01 12:22',
    'tastes': {
        'wine': 9,
        b'cheese': 7,
        'cabbage': '1'
    }
}

# Demo for Validation Successful
user = User(**external_data)

print(user.id)
print(user.model_dump())

# Newline for clarity
print()


# Demo for Validation Error
external_data = {
    'id': 'not an int',
    'taste': {}
}

try:
    User(**external_data)
except ValidationError as e:
    print(e)
    print()
    print(e.errors())