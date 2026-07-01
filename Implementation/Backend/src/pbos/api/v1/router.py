from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pbos.api.v1.schemas import (
    AssessmentCreate,
    AssessmentRead,
    BusinessCreate,
    BusinessRead,
    EvidenceRead,
    QuestionCreate,
    QuestionRead,
    ResponseCreate,
    ResponseSubmissionRead,
    UserCreate,
    UserRead,
)
from pbos.infrastructure.database.models import Business, PBHSQuestion, User
from pbos.infrastructure.database.session import get_session
from pbos.infrastructure.repositories.sqlalchemy_repositories import (
    SqlAlchemyBusinessRepository,
    SqlAlchemyEvidenceRepository,
    SqlAlchemyQuestionRepository,
)
from pbos.services.assessment_service import AssessmentService

api_v1_router = APIRouter()


@api_v1_router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: Session = Depends(get_session)) -> User:
    user = User(name=payload.name, email=payload.email)
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=409, detail="user_email_already_exists") from exc
    session.refresh(user)
    return user


@api_v1_router.post("/businesses", response_model=BusinessRead, status_code=status.HTTP_201_CREATED)
def create_business(
    payload: BusinessCreate,
    session: Session = Depends(get_session),
) -> Business:
    if session.get(User, payload.user_id) is None:
        raise HTTPException(status_code=404, detail="user_not_found")

    repository = SqlAlchemyBusinessRepository(session)
    business = Business(**payload.model_dump())
    repository.add(business)
    session.commit()
    session.refresh(business)
    return business


@api_v1_router.get("/businesses/{business_id}", response_model=BusinessRead)
def get_business(business_id: UUID, session: Session = Depends(get_session)) -> Business:
    business = SqlAlchemyBusinessRepository(session).get(business_id)
    if business is None:
        raise HTTPException(status_code=404, detail="business_not_found")
    return business


@api_v1_router.post(
    "/businesses/{business_id}/assessments",
    response_model=AssessmentRead,
    status_code=status.HTTP_201_CREATED,
)
def start_assessment(
    business_id: UUID,
    payload: AssessmentCreate,
    session: Session = Depends(get_session),
):
    try:
        return AssessmentService(session).start_assessment(
            business_id=business_id,
            pbhs_version=payload.pbhs_version,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@api_v1_router.post(
    "/pbhs/questions",
    response_model=QuestionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    payload: QuestionCreate,
    session: Session = Depends(get_session),
) -> PBHSQuestion:
    question = PBHSQuestion(**payload.model_dump(by_alias=True))
    SqlAlchemyQuestionRepository(session).add(question)
    session.commit()
    session.refresh(question)
    return question


@api_v1_router.get("/pbhs/questions", response_model=list[QuestionRead])
def list_active_questions(session: Session = Depends(get_session)) -> list[PBHSQuestion]:
    return SqlAlchemyQuestionRepository(session).list_active()


@api_v1_router.post(
    "/assessments/{assessment_id}/responses",
    response_model=ResponseSubmissionRead,
    status_code=status.HTTP_201_CREATED,
)
def submit_response(
    assessment_id: UUID,
    payload: ResponseCreate,
    session: Session = Depends(get_session),
):
    try:
        response, evidence = AssessmentService(session).submit_response(
            assessment_id=assessment_id,
            question_id=UUID(payload.question_id),
            response_value=payload.response_value,
        )
    except ValueError as exc:
        detail = str(exc)
        status_code = 404 if detail.endswith("_not_found") else 422
        raise HTTPException(status_code=status_code, detail=detail) from exc

    return {"response": response, "evidence": evidence}


@api_v1_router.get("/assessments/{assessment_id}/evidence", response_model=list[EvidenceRead])
def list_assessment_evidence(
    assessment_id: UUID,
    session: Session = Depends(get_session),
):
    return SqlAlchemyEvidenceRepository(session).list_for_assessment(assessment_id)
