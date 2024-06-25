from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from loguru import logger
from app.database.engine import SessionLocal
from app.service import bitcoin_service


app = FastAPI(title="Challenge BackEnd")


# set the CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # allow the cookie
    allow_methods=["*"],  # allow all http methods
    allow_headers=["*"],  # all all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET /opreturn/${opReturnData}
@app.get("/opreturn/{opReturnData}")
def get_op_return_data(opReturnData: str, db: Session = Depends(get_db)):
    try:
        response = bitcoin_service.get_op_return_data(opReturnData, db)
        logger.info(f"get_op_return_data successfully")
        return response
    except HTTPException as http_exception:
        logger.error(f"get_op_return_data failed with HTTPException: {http_exception}")
        raise http_exception
    except Exception as e:
        logger.error(f"get_op_return_data failed with exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Exception handler
@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )