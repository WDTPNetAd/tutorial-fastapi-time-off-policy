from datetime import datetime
from fastapi import APIRouter, Depends, Query, Path
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyResponse, PaginatedPolicyResponse

import app.models as models
from app.core.exceptions import NotFoundException, BadRequestException
from app.api.v1.deps import get_db, verify_token

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get(
    '/policies', 
    response_model=PaginatedPolicyResponse,
    dependencies=[Depends(verify_token)]
    )
def get_policies(
    db: db_dependency,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100),
    q: Annotated[str | None, Query(max_length=50)] = None
):
    policies = db.query(models.Policy).filter(models.Policy.deleted_at.is_(None)).offset(skip).limit(limit).all()
    total = db.query(func.count(models.Policy.id)).filter(models.Policy.deleted_at.is_(None)).scalar()
    return PaginatedPolicyResponse(
        total=total,
        skip=skip,
        limit=limit,
        data=policies
    )

@router.post('/policies', response_model=PolicyResponse)
def create_policy(policy: PolicyCreate, db: db_dependency):
    policy_data = policy.dict(exclude_unset=True)

    existing = db.query(models.Policy).filter(models.Policy.name == policy.name).first()
    if existing:
        raise BadRequestException("Policy already exists")

    db_policy = models.Policy(**policy_data)
    try:
        db.add(db_policy)
        db.flush()  # Assigns ID to db_policy without committing

        #create an entry to policy history for tracking
        create_policy_history(db_policy, db)

        db.commit()
        db.refresh(db_policy)
    except IntegrityError:
        db.rollback()
        raise BadRequestException("Bad request on policy")

    return db_policy

@router.get('/policies/{policy_id}', response_model=PolicyResponse)
def get_policy(
    policy_id: Annotated[int, Path(title="ID of the policy to get")],
    db: db_dependency
):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise NotFoundException('Policy')
    return db_policy

@router.put('/policies/{policy_id}', response_model=PolicyResponse)
def update_policy(policy_id: int, policy: PolicyUpdate, db: db_dependency):
    # Retrieve existing policy
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise NotFoundException("Policy")

    # Check for duplicate name (excluding current)
    if policy.name:
        duplicate = db.query(models.Policy).filter(
            models.Policy.name == policy.name,
            models.Policy.id != policy_id
        ).first()
        if duplicate:
            raise BadRequestException("Policy name already exists")

    # Apply partial updates, avoid overwriting with None
    update_data = policy.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_policy, key, value)
        
    try:
        #create an entry to policy history for tracking
        create_policy_history(db_policy, db)
        db.commit()
        db.refresh(db_policy)
    except IntegrityError:
        db.rollback()
        raise BadRequestException("Database integrity error")

    return db_policy

@router.delete('/policies/{policy_id}')
def delete_policy(policy_id: int, db: db_dependency):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise NotFoundException('Policy')
    db_policy.deleted_at = datetime.now()
    db.commit()
    return {"message": "Policy deleted successfully"}

@router.get('/policies/{policy_id}/duplicate', response_model=PolicyResponse)
def duplicate_policy(policy_id: int, db: db_dependency):
    db_policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not db_policy:
        raise NotFoundException('Policy')
    # Create copy of policy
    new_policy = models.Policy(
        **{
            k: v
            for k, v in db_policy.__dict__.items()
            if not k.startswith('_') and k != 'id'
        }
    )
    new_policy.name = f"{new_policy.name} (Copy)"

    try:
        db.add(new_policy)
        db.flush()
        create_policy_history(new_policy, db)
        db.commit()
        db.refresh(new_policy)
    except IntegrityError:
        db.rollback()
        raise BadRequestException("Could not duplicate policy due to a database error")
    return new_policy

def create_policy_history(policy: models.Policy, db: db_dependency):

    policy_history = models.PolicyHistory(
        policy_id=policy.id,
        name=policy.name,
        days_allowed=policy.days_allowed,
        policy_type=policy.policy_type
    )

    db.add(policy_history)
    db.commit()
    db.refresh(policy_history)

    return policy_history

