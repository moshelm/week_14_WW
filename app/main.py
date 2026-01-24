from fastapi import FastAPI
from .route import router
from .db import init_database,init_table
import uvicorn

app = FastAPI()
app.include_router(router)

@app.on_event('startup')
def startup_event():
    print('--- Starting System Initializing ---')
    
    # שלב 1: יצירת מסד הנתונים
    db_ok = init_database()
    if db_ok:
        print("Step 1: Database ready.")
    else:
        print("Step 1: Database failed. Check your connection or permissions.")

    # שלב 2: יצירת הטבלה (רק אם מסד הנתונים קיים)
    if db_ok:
        table_ok = init_table()
        if table_ok:
            print("Step 2: Table ready.")
        else:
            print("Step 2: Table creation failed.")
    
    print('--- System Initializing Finished ---')
    
if __name__=="__main__":
    uvicorn.run(app,host='0.0.0.0',port=8000)