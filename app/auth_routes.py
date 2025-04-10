import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas import UserCredentials, SignUpRequest, AuthResponse
from model.db.auth import sign_up as db_sign_up, sign_in as db_sign_in, _insert_user_details
from gotrue.errors import AuthApiError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup_endpoint(request: SignUpRequest):
    logger.info(f"Signup attempt for: {request.email}")
    try:
        user_metadata = None
        if request.full_name:
            user_metadata = {"full_name": request.full_name}
            logger.info(f"Including full name '{request.full_name}' in signup metadata.")

        # Call Supabase auth, passing metadata
        auth_result = db_sign_up(request.email, request.password, user_metadata=user_metadata)

        if auth_result and auth_result.user:
            user = auth_result.user
            _insert_user_details(user.id, user.email, request.full_name)

            if user.confirmation_sent_at and not user.email_confirmed_at:
                 return AuthResponse(message=f"Signup successful for {user.email}. Please check your email to verify your account.")
            else:
                 return AuthResponse(
                     message=f"Signup successful for {user.email}. Account created and verified.",
                     user_id=user.id
                 )
        elif auth_result and not auth_result.user:
             logger.warning(f"Signup for {request.email} completed but no user object returned. Possible verification needed. Result: {auth_result}")
             return AuthResponse(message="Signup initiated. Please check your email to verify your account.")
        else:
             logger.error(f"Signup failed for {request.email}. Raw result: {auth_result}")
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signup failed. Please try again.")

    except AuthApiError as e:
        logger.error(f"Supabase Auth API Error during signup for {request.email}: {e}")
        detail = "Signup failed. User might already exist or invalid credentials."
        if "User already registered" in str(e):
            detail = "User already registered. Try logging in or reset password."
        elif "Password should be at least 6 characters" in str(e):
            detail = "Password should be at least 6 characters."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
    except Exception as e:
        logger.error(f"Unexpected error during signup for {request.email}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred during signup.")


@router.post("/signin", response_model=AuthResponse)
def signin_endpoint(request: UserCredentials):
    logger.info(f"Signin attempt for: {request.email}")
    try:
        result = db_sign_in(request.email, request.password)

        if result and result.session:
            logger.info(f"Signin successful for: {request.email}. User ID: {result.user.id}")
            return AuthResponse(
                message="Sign in successful",
                access_token=result.session.access_token,
                refresh_token=result.session.refresh_token,
                user_id=result.user.id
            )
        elif result and result.user and not result.session:
             logger.warning(f"Signin attempt for {request.email}: User authenticated but no session. Email verification needed?")
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication successful, but account setup incomplete (e.g., Email verification required). Please check your email.")
        else:
            logger.warning(f"Signin failed for {request.email}. Validation failed or invalid credentials.")
            error_detail = "Invalid email or password, user not found in our system, or email not verified."
            if result and hasattr(result, 'error') and result.error:
                 if "Invalid login credentials" in result.error.message:
                     error_detail = "Invalid email or password."
                 elif "Email not confirmed" in result.error.message:
                     error_detail = "Email not confirmed. Please check your verification email."

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_detail)

    except AuthApiError as e:
        logger.error(f"Supabase Auth API Error during signin for {request.email}: {e}")
        detail = "Invalid login credentials or communication error."
        if "Invalid login credentials" in str(e):
            detail = "Invalid email or password."
        elif "Email not confirmed" in str(e):
            detail = "Email not confirmed. Please check your verification email."
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    except Exception as e:
        logger.error(f"Unexpected error during signin for {request.email}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred during signin.") 