from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.auth import (
    create_access_token,
    decode_access_token,
)

app = FastAPI(title="InsureIQ360 API")


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://insure-iq-360-eight.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# OAuth2
# =========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# =========================================================
# LOGIN
# =========================================================

@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    username = form_data.username
    password = form_data.password


    # Test user
    if username == "admin" and password == "admin123":

        access_token = create_access_token(
            {
                "sub": username,
                "role": "admin"
            }
        )


        return {
            "access_token": access_token,
            "token_type": "bearer",
            "username": username,
            "role": "admin"
        }


    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )



# =========================================================
# CURRENT USER
# =========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    payload = decode_access_token(token)


    if not payload:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )


    return payload




@app.get("/auth/me")
def get_me(
    current_user: dict = Depends(get_current_user)
):

    return {
        "message": "Authentication successful",
        "username": current_user.get("sub"),
        "role": current_user.get("role")
    }



# =========================================================
# CUSTOMER ROUTES
# =========================================================

from api.customers import router as customer_router

app.include_router(customer_router)



# =========================================================
# CLAIMS ROUTES
# =========================================================

from api.claims import router as claims_router

app.include_router(claims_router)



# =========================================================
# POLICY ROUTES
# =========================================================

from api.policies import router as policy_router

app.include_router(policy_router)



# =========================================================
# RESERVE FORECAST ROUTES
# =========================================================

from api.reserve_forecast import router as reserve_forecast_router

app.include_router(reserve_forecast_router)



# =========================================================
# ALERTS ROUTES
# =========================================================

from api.alerts import router as alerts_router

app.include_router(alerts_router)



# =========================================================
# EVENTS ROUTES
# =========================================================

from api.events import router as events_router

app.include_router(events_router)



# =========================================================
# DATA QUALITY ROUTES
# =========================================================

from api.data_quality import router as data_quality_router

app.include_router(data_quality_router)



# =========================================================
# RISK ANALYTICS ROUTES
# =========================================================

from api.risk_analytics import router as risk_analytics_router

app.include_router(risk_analytics_router)

# =========================================================
# FRAUD DETECTION ROUTES
# =========================================================

from api.fd import router as fraud_router

app.include_router(fraud_router)