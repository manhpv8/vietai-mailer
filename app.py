import uvicorn
from fastapi import FastAPI, File, UploadFile
import pandas as pd
from src.send import send_multiple_emails
import config
from tabulate import tabulate

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



HEADER = """<html>
<head>
<style> 
table, th, td { border: 2px solid rgb(25, 138, 243); border-collapse: collapse; }
th, td { padding: 6px; }
</style>
</head>"""

TEMPLATE = """
<body style="font-size: 14px">
<p>Chào bạn,</p>
<p>Đội ngũ VietAI xin thông báo kết quả điểm toàn khóa của bạn trong khóa Advances in Natural Language Processing - NLP03 như sau:</p>
{}
<br/>


<p>1. Cụ thể, <b>Quiz 40% gồm 12 bài</b>, cụ thể như sau:</p>
{}
<br/>

<p>
<b>Lưu ý:</b><br/> 
&emsp;- Trừ 10% điểm cho mỗi tuần nộp muộn<br/>
&emsp;- Tính điểm làm lần đầu
</p><br/>



<p>2. Bài tập <b>lập trình gồm 2 bài (60%)</b>, cụ thể như sau:</p>
{}
<br/>

<span style="color: red;">=> Thắc mắc về điểm thành phần, vui lòng điền vào feedback form</span> <a href="https://forms.gle/PZapPMQ7DPhyfA8P6">[VietAI] Online Natural Language Processing - NLP03 Feedback điểm toàn khóa</a>
<p><b>Hạn cuối nhận feedback:</b> <span style="color: red;">Trước 23h59p, thứ 3, ngày 13/06/2023.</span></p><br/>

<p>Trân trọng,</p>
<p>VietAI team.</p>
</body>
</html>
"""


QUIZ_LIST = [
    'Quiz 1.1',
    'Quiz 1.2',
    'Quiz 2.1',
    'Quiz 2.2',
    'Quiz 3.1',
    'Quiz 4.1',
    'Quiz 4.2',
    'Quiz 5.1',
    'Quiz 5.2',
    'Quiz 6.1',
    'Quiz 6.2',
    'Quiz 7.1'
    ]

ASSIGMENT_LIST = [
        "assigment_1", "assigment_2"
    ]


def generate_overview_table(email, fullname, quiz_score, assigment_score, attendence_score, overall_score, certificate_level, rank):
    header = ["","","Quiz","Bài tập lập trình", "Chuyên cần", "Tổng kết", "Đạt chứng chỉ","Xếp hạng"]
    row_1 = ["Email", "Họ tên", "0,4",	"0,6", "0,1","1.1",	">= 50%", ""]
    row_2 = [email, fullname, quiz_score, assigment_score, attendence_score, overall_score, certificate_level, rank]
    overview_table = [
        header,
        row_1,
        row_2
    ]
    return tabulate(overview_table, headers='firstrow', tablefmt='unsafehtml', stralign='center', numalign='center')


def generate_quiz_table(email: str, fullname: str, overall_quiz_score: float, quiz_detail: dict):
    quiz_table = []
    try:
        header = ["Email", "Họ tên"]
        header.extend(QUIZ_LIST)
        header.append("Trung bình")

        score_row = [email, fullname]
        score_delay = ["", "delay days"]

        quiz_names =  quiz_detail['quiz_name']
        quiz_scores =  quiz_detail['score']
        delay_dates = quiz_detail['late']

        
        
        for quiz in QUIZ_LIST:
            if quiz in quiz_names:
                score = quiz_scores[quiz_names.index(quiz)]
                delay = delay_dates[quiz_names.index(quiz)]
            else:
                score = 0
                delay = 0

            score_delay.append(delay)
            score_row.append(score)
        
        score_row.append(overall_quiz_score)
        quiz_table = [header, score_row,score_delay]
    except Exception as e:
        print(f"email: {email}")
        range(e)
    return tabulate(quiz_table, headers='firstrow', tablefmt='unsafehtml', stralign='center', numalign='center')

    
def generate_assigment_table(email: str, fullname: str, overall_score: float, assigment_detail: dict):
    assigment_table = []
    header = ["Email", "Họ tên"]
    header.extend(ASSIGMENT_LIST)
    header.append("Trung bình")

    score_row = [email, fullname]
    delay_row = ["", "delay days"]
    
    assigments = assigment_detail.keys()
    for ass in ASSIGMENT_LIST:
        if ass in assigments:
            score = assigment_detail[ass]['score']
            delay = int( assigment_detail[ass]['late_days'])
            
        else:
            score = 0
            delay = 0
        score_row.append(score)
        delay_row.append(delay)
    
    score_row.append(overall_score)
    assigment_table = [header, score_row, delay_row]
    return tabulate(assigment_table, headers='firstrow', tablefmt='unsafehtml', stralign='center', numalign='center')


import json

def generate_html_content(row):

    try:
        email = row['email']
        fullname = row['name']

        attendence_score = round(row['attendence_score'], 3)
        quiz_score = round(row['quiz_score'], 3)
        assigment_score = row['assigment_score']
        certificate_level = row['certificate_level']
        overall_score = round(row['score'], 3)
        ranking = row['ranking']


        overall_table = generate_overview_table(
            email =email, 
            fullname =fullname, 
            quiz_score =quiz_score , 
            assigment_score = assigment_score, 
            attendence_score = attendence_score, 
            overall_score = overall_score, 
            certificate_level = certificate_level, 
            rank = ranking)
        
        
        quiz_detail = row['quiz_detail'] 
        quiz_detail = quiz_detail.replace("'", "\"")
        quiz_detail = json.loads(quiz_detail)

        quiz_table = generate_quiz_table(email = email, 
                        fullname = fullname,
                        overall_quiz_score = quiz_score, 
                        quiz_detail = quiz_detail
                        )
        

        assigment_detail = row['ass_detail'] 
        assigment_detail = assigment_detail.replace("'", "\"")
        assigment_detail = json.loads(assigment_detail)
        ass_table = generate_assigment_table(
            email = email, 
                fullname = fullname,
                overall_score=assigment_score,
                assigment_detail = assigment_detail
            )
    except Exception as e:
        print(quiz_detail)
        raise e
    return HEADER+TEMPLATE.format(overall_table, quiz_table, ass_table)

    

@app.post("/send_score_ranking_v2")
def notify_ranking_v1(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)
    df['html_content'] = df.apply(lambda x: generate_html_content(x), axis = 1)
    
    # send email

    results = send_multiple_emails(subject = "[VIETAI - ĐÍNH CHÍNH] THÔNG BÁO ĐIỂM TOÀN KHÓA ADVANCES IN NATURAL LANGUAGE PROCESSING - NLP03", data_df = df)
    file.file.close()
    
    return {
        "results": results,
        "Status": "Success!!!"}



TEMP_INVITE = '''
<body style="font-size: 14px">
<p>Dear {}</p>

<p>Congratulations! We are excited to inform you that you’ve been selected to collaborate with VietAI Research. This is a significant achievement and a reflection of your hard work. 

<p> Here’s what this collaboration entails:<p>
<p>🧠 Challenges: You will participate in challenges that aim to solve impactful research problems.<p>
<p>🚀 Potential selection: Stand out in these challenges and you could be chosen to join the VietAI core research group, a prestigious team focused on groundbreaking AI research. <p>
<p>🔗 Messenger group: Please join the Messenger group for discussions, updates, and collaboration with fellow participants: https://m.me/j/AbY1LDsjoueaEe2T/<p>
<p>👨‍🏫 Mentors: You’ll have the guidance of experienced mentors including Mr. Thang and Mr. Duong, along with other core research team members. They will offer their expertise and are available for any support you need.<p>

<p>Your involvement in this collaboration is invaluable. We encourage you to actively participate, share your insights, and don’t hesitate to seek assistance if needed. <p>

<p>Warm regards,</p>
<p>VietAI.</p>


</body>
</html>

'''


def generate_html_content_v1(row):
    full_name = row['name']
    return TEMP_INVITE.format(full_name)
    

@app.post("/send_invite_reseach")
def notify_ranking_v1(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)
    df['html_content'] = df.apply(lambda x: generate_html_content_v1(x), axis = 1)
    
    # send email
    results = send_multiple_emails( subject = "🌟 Congrats! Welcome to Collaboration with VietAI Research 🚀", data_df = df)
    file.file.close()
    
    return {
        "results": results,
        "Status": "Success!!!"}

if __name__ == "__main__":
    uvicorn.run(app, host=config.host, port=config.port)