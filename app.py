import uvicorn
from fastapi import FastAPI, File, UploadFile
import pandas as pd
from src.send import send_multiple_emails
import config

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/send_score_ranking")
def notify_ranking(file: UploadFile = File(...)):

    template_location_path = "table_score_template.html"
    df = pd.read_csv(file.file)
    
    print(df)
    # TODO constaints data input
    
    # send email
    results = send_multiple_emails(template_location_path = template_location_path, data_df = df)
    file.file.close()
    
    return {
        "results": results,
        "Status": "Success!!!"}

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)