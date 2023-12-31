from typing import List, Optional
from pydantic import BaseModel

class Foo(BaseModel):
    count: int 
    size: Optional[float] = None
    
class Bar(BaseModel):
    apple: str = 'x'
    banana: str = 'y'
    
class Spam(BaseModel):
    foo: Foo
    bars: List[Bar]
    
m = Spam(foo = {'count': 4}, 
         bars = [
             {'apple': 'x1'}, 
             {'apple': 'x2'}
             ])

print(m)
print()
print(m.model_dump())

