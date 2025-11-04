from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.session import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyOut
from typing import List

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("", response_model=CompanyOut)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    exists = db.query(Company).filter(
        or_(
            Company.name == data.name,
            Company.rut == data.rut,
            Company.email == data.email
        )
    ).first()

    if exists:
        raise HTTPException(status_code=400, detail="Company already exists")


    c = Company(**data.model_dump())

    db.add(c)
    db.commit()
    db.refresh(c)
    return c



@router.post("/bulk", response_model=List[CompanyOut])
def create_companies_bulk(
    data: List[CompanyCreate], 
    db: Session = Depends(get_db),
):
    # Validamos duplicados ANTES de crear nada (todo o nada)
    for item in data:
        exists = (
            db.query(Company)
            .filter(
                or_(
                    Company.name == item.name,
                    Company.rut == item.rut,
                    Company.email == item.email,
                )
            )
            .first()
        )
        if exists:
            raise HTTPException(
                status_code=400,
                detail=f"Company already exists with name={item.name} or rut={item.rut} or email={item.email}",
            )

    # Creamos todas las empresas
    companies = [Company(**item.model_dump()) for item in data]
    db.add_all(companies)
    db.commit()
    for c in companies:
        db.refresh(c)

    return companies



@router.get("/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db),):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company




@router.get("", response_model=List[CompanyOut])
def get_all_company(db: Session = Depends(get_db),):
    companies = db.query(Company).all()
    if not companies:
        raise HTTPException(status_code=404, detail="No companies found")
    
    return companies