from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, tours, bookings, payments
from .routers import recommend  # router recommendation

app = FastAPI(title="Travel Booking API")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(auth.router)
app.include_router(tours.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(recommend.router)

# ✅ Route test
@app.get("/")
def root():
    return {"msg": "✅ Travel API is running! Visit /docs for API documentation."}
