from pydantic import BaseModel


class TestCreate(BaseModel):
    test: int



class TestResponse(BaseModel):
    id: int
    test: int
