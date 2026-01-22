from fastapi import FastAPI
from .route import router
import uvicorn

app = FastAPI()
app.include_router(router)

@app.on_event('startup')
def init_database():
    print('connecting to database')

if __name__=="__main__":
    uvicorn.run(app,host='0.0.0.0',port=8000)