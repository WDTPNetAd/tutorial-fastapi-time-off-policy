from datetime import date, datetime
from fastapi import APIRouter, Depends, Query
from typing import Annotated, List, Union
from sqlalchemy.orm import Session, joinedload  
from app.schemas.time_off_request import TimeOffRequestCreate, TimeOffRequestUpdate, TimeOffRequestResponse, TimeOffStatusResponse
from sqlalchemy.exc import IntegrityError
import app.models as models
from app.core.exceptions import NotFoundException, BadRequestException
from app.api.v1.deps import get_db

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/time_off_requests', response_model=List[TimeOffRequestResponse])
def get_time_off_requests(
    db: db_dependency,
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
):
    query = db.query(models.TimeOffRequest)

    if start_date:
        query = query.filter(models.TimeOffRequest.start_date >= start_date)

    if end_date:
        query = query.filter(models.TimeOffRequest.end_date <= end_date)

    time_off_requests = query.all()
    return time_off_requests



@router.post('/time_off_requests', response_model=TimeOffRequestResponse)
def create_time_off_request(time_off_request: TimeOffRequestCreate, db: db_dependency):

    validate_time_off_request(time_off_request, db)
    
    time_off_request_data = time_off_request.dict(exclude_unset=True)
    db_time_off_request = models.TimeOffRequest(**time_off_request_data, status="Pending")
    try:
        db.add(db_time_off_request)
        db.commit()
        db.refresh(db_time_off_request)
    except IntegrityError:
        db.rollback()
        raise BadRequestException("Bad request on time off request")
    return db_time_off_request

@router.get('/time_off_requests/{time_off_request_id}/status', response_model=TimeOffStatusResponse)
def get_time_off_request_status(time_off_request_id: int, db: db_dependency):
    time_off_request = db.query(models.TimeOffRequest) \
    .options(joinedload(models.TimeOffRequest.employee), joinedload(models.TimeOffRequest.policy)) \
    .filter(models.TimeOffRequest.id == time_off_request_id) \
    .first()

    if not time_off_request:
        raise NotFoundException('Time Off Request')

    today = date.today()

    total_days = (time_off_request.end_date - time_off_request.start_date).days + 1
    remaining_days = 0
    is_ongoing = False

    if time_off_request.start_date <= today <= time_off_request.end_date:
        # Ongoing request (started and not ended)
        remaining_days = (time_off_request.end_date - today).days + 1
        is_ongoing = True
    elif today < time_off_request.start_date:
        # Upcoming request (not started yet)
        remaining_days = total_days
    # else: Past request (ended); remaining_days stays 0

    return {
        'id': time_off_request.id,
        'employee_name': time_off_request.employee.name,
        'policy_name': time_off_request.policy.name,
        'start_date': time_off_request.start_date,
        'end_date': time_off_request.end_date,
        'total_days': total_days,
        'remaining_days': remaining_days,
        'is_ongoing': is_ongoing
    }


@router.get('/time_off_requests/{time_off_request_id}', response_model=TimeOffRequestResponse)
def get_time_off_request(time_off_request_id: int, db: db_dependency):
    time_off_request = db.query(models.TimeOffRequest).filter(models.TimeOffRequest.id == time_off_request_id).first()
    if not time_off_request:
        raise NotFoundException('Time Off Request')
    return time_off_request
    
@router.put('/time_off_requests/{time_off_request_id}', response_model=TimeOffRequestResponse)
def update_time_off_request(time_off_request_id: int, time_off_request: TimeOffRequestUpdate, db: db_dependency):

    db_existing_time_off_request = db.query(models.TimeOffRequest).filter(models.TimeOffRequest.id == time_off_request_id).first()

    validate_time_off_request(time_off_request, db, db_existing_time_off_request)

    update_data = time_off_request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_existing_time_off_request, key, value)
    db.add(db_existing_time_off_request)
    db.commit()
    db.refresh(db_existing_time_off_request)
    return db_existing_time_off_request
    
@router.delete('/time_off_requests/{time_off_request_id}')
def delete_time_off_request(time_off_request_id: int, db: db_dependency):
    db_time_off_request = db.query(models.TimeOffRequest).filter(models.TimeOffRequest.id == time_off_request_id).first()
    if not db_time_off_request:
        raise NotFoundException('Time Off Request')
    db_time_off_request.deleted_at = datetime.now()
    db.commit()
    return {"message": "Time Off Request deleted successfully"}

def validate_time_off_request(
    time_off_request: Union[TimeOffRequestCreate, TimeOffRequestUpdate],
    db: db_dependency,
    existing_request: models.TimeOffRequest | None = None,
) -> bool:
    data = time_off_request.dict(exclude_unset=True)

    # should handle even if start_date or end_date is not passed on TimeOffRequestUpdate
    employee_id = data.get("employee_id") or getattr(existing_request, "employee_id", None)
    policy_id = data.get("policy_id") or getattr(existing_request, "policy_id", None)
    start_date = data.get("start_date") or getattr(existing_request, "start_date", None)
    end_date = data.get("end_date") or getattr(existing_request, "end_date", None)

    # Validate employee
    if employee_id:
        employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
        if not employee:
            raise NotFoundException("Employee")

    # Validate policy
    policy = None
    if policy_id:
        policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
        if not policy:
            raise NotFoundException("Policy")

    # Validate requested days only if all required fields are available
    if start_date and end_date and policy:
        requested_days = (end_date - start_date).days
        if requested_days > policy.days_allowed:
            raise BadRequestException(
                f"Days requested ({requested_days}) exceed policy limit ({policy.days_allowed})"
            )

    return True
