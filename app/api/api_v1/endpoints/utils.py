from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api import deps
from app.models.user import User
from app.schemas.msg import Msg
from app.utils.email import send_test_email

router = APIRouter()


@router.post("/test-email/", response_model=Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Test emails. (Admin only)
    """
    send_test_email(
        email_to=email_to,
        subject="Test email",
        html_content="<p>This is a test email</p>",
    )
    return {"msg": "Test email sent"}
