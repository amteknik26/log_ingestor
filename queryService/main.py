from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# db con
DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#HTML rendering
templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_logs(
    request: Request,
    level: str = None,
    message: str = None,
    resourceId: str = None,
    start_date: str = None,  
    end_date: str = None,   
    traceId: str = None,
    spanId: str = None,
    commit: str = None,
    parentResourceId: str = None,
):
    try:
        # Check if both start date and end date are provided, or neither
        if (start_date is None and end_date is not None) or (start_date is not None and end_date is None):
            raise HTTPException(status_code=400, detail="Both start date and end date must be provided.")

        # Construct the query based on the provided filters
        query_params = {
            "level": level,
            "message": message,
            "resourceId": resourceId,
            "start_date": start_date,  
            "end_date": end_date,     
            "traceId": traceId,
            "spanId": spanId,
            "commit": commit,
            "parentResourceId": parentResourceId,
        }

        # Remove out None and empty 
        query_params = {key: value for key, value in query_params.items() if value is not None and value != ""}

        # Construct the date range condition
        date_range_condition = ""
        if start_date and end_date:
            date_range_condition = f"timestamp BETWEEN '{start_date}T00:00:00Z' AND '{end_date}T23:59:59Z'"

        filter_conditions = " AND ".join([f"{key} = :{key}" for key in query_params if key not in ['start_date', 'end_date']])
        
        # Combine filter conditions and date range condition
        if filter_conditions and date_range_condition:
            filter_conditions += f" AND {date_range_condition}"
        elif date_range_condition:
            filter_conditions = date_range_condition

        query = text(f"SELECT * FROM logs WHERE {filter_conditions}") if filter_conditions else text("SELECT * FROM logs")

        # Execute the query
        with SessionLocal() as db:
            result = db.execute(query, query_params).fetchall()

        # Render the HTML template with the query result
        return templates.TemplateResponse("logs.html", {"request": request, "logs": result, "error_message": None})

    except HTTPException as e:
        return templates.TemplateResponse("logs.html", {"request": request, "logs": None, "error_message": e.detail})

    except Exception as e:
        return templates.TemplateResponse("logs.html", {"request": request, "logs": None, "error_message": str(e)})

#For terminal coloring
import colorama
import uvicorn
colorama.init()

if __name__ == "__main__":
    uvicorn.run("main:app", port=3003, log_level="info")






























































# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import IntegrityError

# app = FastAPI()

# # Database setup
# DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Templates configuration for HTML rendering
# templates = Jinja2Templates(directory="templates")


# @app.get("/")
# def read_logs(
#     request: Request,
#     level: str = None,
#     message: str = None,
#     resourceId: str = None,
#     timestamp: str = None,
#     traceId: str = None,
#     spanId: str = None,
#     commit: str = None,
#     parentResourceId: str = None,
# ):
#     # Construct the query based on the provided filters
#     query_params = {
#         "level": level,
#         "message": message,
#         "resourceId": resourceId,
#         "timestamp": timestamp,
#         "traceId": traceId,
#         "spanId": spanId,
#         "commit": commit,
#         "parentResourceId": parentResourceId,
#     }

#     # Filter out None or empty string values
#     query_params = {key: value for key, value in query_params.items() if value is not None and value != ""}

#     filter_conditions = " AND ".join([f"{key} = :{key}" for key in query_params])
#     query = text(f"SELECT * FROM logs WHERE {filter_conditions}") if filter_conditions else text("SELECT * FROM logs")

#     # Execute the query
#     with SessionLocal() as db:
#         try:
#             result = db.execute(query, query_params).fetchall()
#         except IntegrityError as e:
#             result = []
#             print(f"Error executing query: {e}")

#     # Render the HTML template with the query result
#     return templates.TemplateResponse("logs.html", {"request": request, "logs": result})

# import colorama
# import uvicorn
# colorama.init()

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=3003, log_level="info")
