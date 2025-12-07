from pydantic import BaseModel, Field


class Employee(BaseModel):
    name: str = Field(alias="Nome")
    surname: str = Field(alias="Sobrenome")
    email: str = Field(alias="Email")
    phone: str = Field(alias="Telefone")
    address: str = Field(alias="Endereço")
    job: str = Field(alias="Cargo")
    company: str = Field(alias="Empresa")
