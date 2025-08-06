from datetime import datetime
from fastapi import APIRouter, Depends, Query, Path
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

import app.models as models
import app.schemas as schemas
from app.core.exceptions import NotFoundException, BadRequestException
from app.api.v1.deps import get_db, verify_token

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get(
    '/policies', 
    response_model=schemas.PaginatedPolicyResponse,
    dependencies=[Depends(verify_token)]
    )
async def get_policies(
    db: db_dependency,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100),
    q: Annotated[str | None, Query(max_length=50)] = None
):
    policies = db.query(models.Policy).filter(models.Policy.deleted_at.is_(None)).offset(skip).limit(limit).all()
    total = db.query(func.count(models.Policy.id)).filter(models.Policy.deleted_at.is_(None)).scalar()
    return schemas.PaginatedPolicyResponse(
        total=total,
        skip=skip,
        limit=limit,
        data=policies
    )

@router.post('/policies', response_model=schemas.Policy)
async def create_policy(policy: schemas.PolicyBase, db: db_dependency):
    existing = db.query(models.Policy).filter(models.Policy.name == policy.name).first()
    if existing:
        raise BadRequestException("Policy already exists")
    db_policy = models.Policy(name=policy.name)
    try:
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
    except IntegrityError:
        db.rollback()
        raise BadRequestException("Policy already exists")
    return db_policy

@router.get('/policies/{policy_id}', response_model=schemas.Policy)
async def get_policy(
    policy_id: Annotated[int, Path(title="ID of the policy to get")],
    db: db_dependency
):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise NotFoundException('Policy')
    return db_policy

@router.put('/policies/{policy_id}', response_model=schemas.Policy)
async def update_policy(policy_id: int, policy: schemas.PolicyBase, db: db_dependency):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise NotFoundException('Policy')
    # Check if another policy with the same name exists
    duplicate = db.query(models.Policy).filter(
        models.Policy.name == policy.name,
        models.Policy.id != policy_id
    ).first()
    if duplicate:
        raise BadRequestException("Policy name is existing")
    db_policy.name = policy.name
    try:
        db.add(db_policy)
        db.commit()
        db.refresh(db_policy)
    except IntegrityError:
        db.rollback()
        raise BadRequestException("Policy name is existing")
    return db_policy

@router.delete('/policies/{policy_id}')
async def delete_policy(policy_id: int, db: db_dependency):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise NotFoundException('Policy')
    db_policy.deleted_at = datetime.now()
    db.commit()
    return {"message": "Policy deleted successfully"}
