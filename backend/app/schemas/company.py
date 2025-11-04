from pydantic import BaseModel, ConfigDict

class CompanyCreate(BaseModel):
    name: str
    razon_social: str
    rut: str
    giro: str
    direccion: str
    ciudad: str
    telefono: str
    email: str 

    
class CompanyOut(BaseModel):
    id: int
    name: str
    razon_social: str
    rut: str
    giro: str
    direccion: str
    ciudad: str
    telefono: str
    email: str 
    model_config = ConfigDict(from_attributes=True)
