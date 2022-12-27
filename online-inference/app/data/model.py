from pydantic import BaseModel, validator


class HeartRequest(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

    @validator("age")
    def age_validator(cls, v):
        if not 0 <= v <= 100:
            raise ValueError("Age is not correct (must be in range from 0 to 100)")
        return v

    @validator("sex")
    def sex_validator(cls, v):
        if v not in [0, 1]:
            raise ValueError("Sex value is not correct (must be 0 or 1)")
        return v

    @validator("cp")
    def cp_validator(cls, v):
        if not 0 <= v <= 4:
            raise ValueError("Cp value is not correct (must be in range from 0 to 4)")
        return v

    @validator("fbs")
    def fbs_validator(cls, v):
        if v not in [0, 1]:
            raise ValueError("Fbs value is ot correct (must be 0 or 1)")
        return v
