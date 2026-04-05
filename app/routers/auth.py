"""
Auth Routes — Login, Signup, OTP Verification, and Resend endpoints.

Flow:
  Signup: POST /signup  → sends OTP → POST /verify-otp → JWT issued
  Login:  POST /login   → sends OTP → POST /verify-otp → JWT issued

Email sending is handled asynchronously via BackgroundTasks to avoid blocking.
"""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.base import get_db
from app.utils.security import create_access_token
from app.services.auth_service import (
    create_user,
    authenticate_user,
    create_otp,
    verify_otp,
    check_resend_cooldown,
    reset_password,
)
from app.utils.email_utils import send_otp_email
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    OTPVerifyRequest,
    OTPResendRequest,
    AuthResponse,
    OTPSentResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=OTPSentResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Step 1 of Signup — creates the user account and sends an OTP asynchronously."""
    try:
        await create_user(db=db, username=request.username, email=request.email, password=request.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user.")

    try:
        code = await create_otp(db=db, email=request.email, purpose="signup")
        background_tasks.add_task(send_otp_email, email=request.email, otp_code=code, purpose="signup")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create OTP: {e}")

    return OTPSentResponse(message="Account created. Check your email for the verification code.", email=request.email)


@router.post("/login", response_model=OTPSentResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Step 1 of Login — validates credentials, then sends an OTP asynchronously."""
    try:
        await authenticate_user(db=db, email=request.email, password=request.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error during login.")

    try:
        code = await create_otp(db=db, email=request.email, purpose="login")
        background_tasks.add_task(send_otp_email, email=request.email, otp_code=code, purpose="login")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create OTP: {e}")

    return OTPSentResponse(message="OTP sent to your email. Please verify to complete login.", email=request.email)


@router.post("/verify-otp", response_model=AuthResponse)
async def verify_otp_endpoint(request: OTPVerifyRequest, db: AsyncSession = Depends(get_db)):
    """Step 2 of Login/Signup — verifies the OTP and issues a JWT on success."""
    try:
        await verify_otp(db=db, email=request.email, otp_code=request.otp_code, purpose=request.purpose)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    result = await db.execute(select(User).filter(User.email == request.email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if request.purpose == "signup" and not user.is_verified:
        user.is_verified = True
        await db.commit()
        await db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.user_id)})

    return AuthResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        message="Verified successfully.",
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/resend-otp", response_model=OTPSentResponse)
async def resend_otp(
    request: OTPResendRequest,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Resend a new OTP. Enforces a 60-second cooldown per email+purpose."""
    result = await db.execute(select(User).filter(User.email == request.email))
    if not result.scalars().first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No account found with this email.")

    try:
        await check_resend_cooldown(db=db, email=request.email, purpose=request.purpose)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e))

    try:
        code = await create_otp(db=db, email=request.email, purpose=request.purpose)
        background_tasks.add_task(send_otp_email, email=request.email, otp_code=code, purpose=request.purpose)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create OTP: {e}")

    return OTPSentResponse(message="A new OTP has been sent to your email.", email=request.email)


@router.post("/forgot-password", response_model=OTPSentResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """Step 1 of Password Reset — validates email and sends an OTP asynchronously."""
    result = await db.execute(select(User).filter(User.email == request.email))
    if not result.scalars().first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No account found with this email.")

    try:
        code = await create_otp(db=db, email=request.email, purpose="password_reset")
        background_tasks.add_task(send_otp_email, email=request.email, otp_code=code, purpose="password_reset")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create OTP: {e}")

    return OTPSentResponse(message="OTP sent to your email. Please verify to reset your password.", email=request.email)


@router.post("/reset-password", response_model=OTPSentResponse)
async def reset_password_endpoint(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    """Step 2 of Password Reset — verifies OTP and updates the password."""
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match.")
    if len(request.new_password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long.")

    try:
        await verify_otp(db=db, email=request.email, otp_code=request.otp_code, purpose="password_reset")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    try:
        await reset_password(db=db, email=request.email, new_password=request.new_password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return OTPSentResponse(message="Password reset successfully. Please login with your new password.", email=request.email)
