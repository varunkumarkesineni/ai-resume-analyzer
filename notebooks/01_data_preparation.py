import pandas as pd
import numpy as np
import os

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

np.random.seed(42)

resumes = [
    {"resume_id": "R001", "candidate_name": "Arjun Sharma", "email": "arjun@gmail.com",
     "experience_years": 3, "education": "B.Tech Computer Science",
     "resume_text": "Python developer with 3 years experience. Skilled in Python, Pandas, NumPy, Machine Learning, scikit-learn, SQL, MySQL. Built data pipelines and dashboards using Power BI and Tableau. Experience with ETL workflows, data cleaning, and visualization. Worked on NLP projects using TF-IDF and cosine similarity. Strong knowledge of Data Structures, Algorithms, OOP. Familiar with AWS S3, Git, GitHub, REST APIs."},
    {"resume_id": "R002", "candidate_name": "Priya Reddy", "email": "priya@gmail.com",
     "experience_years": 2, "education": "B.Tech Information Technology",
     "resume_text": "Data analyst with expertise in SQL, Excel, and Power BI. Proficient in Python Pandas for data manipulation and cleaning. Experience in creating dashboards and KPI reports. Knowledge of MySQL database design and query optimization. Worked with ETL pipelines and data transformation. Basic machine learning with scikit-learn. Certifications in Data Analytics from Coursera."},
    {"resume_id": "R003", "candidate_name": "Rahul Verma", "email": "rahul@gmail.com",
     "experience_years": 1, "education": "BCA",
     "resume_text": "Fresher with knowledge of Java and Python basics. Completed projects in HTML CSS JavaScript web development. Basic SQL queries and database management. Knowledge of OOP concepts and data structures. Completed Python certification from Cisco. Interested in software development and web applications."},
    {"resume_id": "R004", "candidate_name": "Sneha Patel", "email": "sneha@gmail.com",
     "experience_years": 4, "education": "M.Tech Data Science",
     "resume_text": "Senior data scientist with 4 years experience in machine learning and NLP. Expert in Python scikit-learn TensorFlow deep learning neural networks. Advanced SQL query optimization MySQL PostgreSQL database design. Built NLP models using TF-IDF Word2Vec BERT for text classification. Power BI Tableau dashboard development and data visualization. AWS GCP cloud platforms S3 BigQuery data engineering ETL pipelines."},
    {"resume_id": "R005", "candidate_name": "Karthik Nair", "email": "karthik@gmail.com",
     "experience_years": 2, "education": "B.Tech ECE",
     "resume_text": "Python programmer with focus on automation and scripting. Data analysis using Pandas NumPy Matplotlib Seaborn visualization. SQL MySQL basic database queries joins group by. Machine learning basics logistic regression random forest. Git GitHub version control collaborative projects. REST API integration JSON data processing."},
    {"resume_id": "R006", "candidate_name": "Divya Menon", "email": "divya@gmail.com",
     "experience_years": 3, "education": "B.Tech Computer Science",
     "resume_text": "Full stack developer Python Django REST API backend. JavaScript React frontend web development HTML CSS. MySQL PostgreSQL database design normalization. Docker AWS deployment cloud infrastructure. Git version control agile scrum methodology. Basic data analysis Pandas Excel reporting."},
    {"resume_id": "R007", "candidate_name": "Aditya Kumar", "email": "aditya@gmail.com",
     "experience_years": 5, "education": "MBA + B.Tech",
     "resume_text": "Business analyst with strong SQL and Excel skills. Power BI Tableau advanced dashboard creation DAX measures. Data cleaning transformation ETL pipeline design. Python Pandas data manipulation statistical analysis. MySQL database queries optimization reporting. Stakeholder communication requirements gathering agile methodology."},
    {"resume_id": "R008", "candidate_name": "Meera Iyer", "email": "meera@gmail.com",
     "experience_years": 1, "education": "B.Sc Statistics",
     "resume_text": "Statistics graduate with Python R programming skills. Pandas NumPy data analysis statistical modeling. Machine learning scikit-learn classification regression clustering. Data visualization Matplotlib Seaborn ggplot. SQL basic queries data extraction MySQL. Excel pivot tables VLOOKUP statistical functions."},
    {"resume_id": "R009", "candidate_name": "Suresh Babu", "email": "suresh@gmail.com",
     "experience_years": 0, "education": "B.Tech CSE Final Year",
     "resume_text": "Computer science student with academic projects in Python. Basic Java programming OOP concepts. HTML CSS web design fundamentals. Participated in coding competitions LeetCode HackerRank. Knowledge of DBMS operating systems computer networks. Completed internship in web development."},
    {"resume_id": "R010", "candidate_name": "Lakshmi Devi", "email": "lakshmi@gmail.com",
     "experience_years": 6, "education": "M.Tech Computer Science",
     "resume_text": "Senior ML engineer Python TensorFlow PyTorch deep learning. NLP expert BERT GPT transformer models text classification NER. TF-IDF vectorization cosine similarity information retrieval. SQL MySQL PostgreSQL advanced database design indexing optimization. AWS SageMaker model deployment MLOps pipeline automation. Power BI dashboards KPI reporting business intelligence."},
]

skills_pool = [
    "Python Pandas NumPy SQL MySQL data analysis",
    "Machine Learning scikit-learn TensorFlow deep learning",
    "Power BI Tableau data visualization dashboard KPI",
    "Java Spring Boot REST API backend development",
    "JavaScript React Node.js HTML CSS frontend",
    "ETL pipeline data cleaning transformation processing",
    "NLP TF-IDF text processing NLTK cosine similarity",
    "AWS GCP cloud computing S3 BigQuery deployment",
    "Git GitHub version control agile scrum methodology",
    "Excel VLOOKUP pivot tables reporting analytics",
]
names = ["Amit", "Rohit", "Pooja", "Ravi", "Anita", "Vijay", "Sunita", "Manoj", "Kavya", "Deepak"]
surnames = ["Singh", "Kumar", "Sharma", "Verma", "Reddy", "Nair", "Patel", "Iyer", "Joshi", "Rao"]
educations = ["B.Tech CSE", "B.Tech IT", "BCA", "B.Sc CS", "M.Tech"]

for i in range(10, 210):
    name = f"{np.random.choice(names)} {np.random.choice(surnames)}"
    exp = np.random.randint(0, 7)
    skills = " ".join(np.random.choice(skills_pool, size=np.random.randint(2, 5), replace=False))
    resumes.append({
        "resume_id": f"R{i+1:03d}",
        "candidate_name": name,
        "email": f"candidate{i+1}@email.com",
        "experience_years": exp,
        "education": np.random.choice(educations),
        "resume_text": f"Professional with {exp} years experience. Skills: {skills}. Strong analytical problem solving communication skills.",
    })

jobs = [
    {"job_id": "J001", "job_title": "Data Analyst", "company": "TCS", "location": "Hyderabad", "experience_required": 2,
     "job_description": "Looking for Data Analyst with strong Python and SQL skills. Required: Python Pandas NumPy data analysis ETL pipeline. Required: SQL MySQL database queries joins optimization. Required: Power BI Tableau dashboard creation KPI reporting. Required: Excel pivot tables VLOOKUP. Nice to have: Machine learning scikit-learn AWS cloud platforms."},
    {"job_id": "J002", "job_title": "ML Engineer", "company": "Infosys", "location": "Bangalore", "experience_required": 3,
     "job_description": "Seeking ML Engineer with NLP and deep learning experience. Required: Python scikit-learn TensorFlow machine learning model building. Required: NLP TF-IDF text classification cosine similarity NLTK. Required: SQL database design MySQL PostgreSQL. Required: Git GitHub version control. Nice to have: AWS SageMaker MLOps Power BI visualization."},
    {"job_id": "J003", "job_title": "BI Developer", "company": "Wipro", "location": "Hyderabad", "experience_required": 2,
     "job_description": "BI Developer needed for dashboard and reporting. Required: Power BI Tableau advanced dashboard DAX measures KPI. Required: SQL MySQL complex queries ETL transformation. Required: Excel advanced pivot tables VLOOKUP. Required: Python Pandas data cleaning. Domain experience in BFSI retail healthcare analytics preferred."},
    {"job_id": "J004", "job_title": "Python Developer", "company": "HCL", "location": "Chennai", "experience_required": 1,
     "job_description": "Python Developer for backend development. Required: Python programming OOP data structures algorithms. Required: REST API development JSON. Required: SQL MySQL database queries. Required: Git GitHub agile scrum. Nice to have: Django Flask AWS Docker containerization."},
    {"job_id": "J005", "job_title": "Data Science Intern", "company": "Deloitte", "location": "Hyderabad", "experience_required": 0,
     "job_description": "Data Science Intern for analytics and ML projects. Required: Python Pandas NumPy data analysis basic ML. Required: scikit-learn classification regression. Required: SQL basic queries MySQL. Required: Matplotlib Seaborn visualization. Nice to have: NLP TF-IDF Power BI Tableau dashboard."},
]

pd.DataFrame(resumes).to_csv(f"{RAW_DIR}/resumes.csv", index=False)
pd.DataFrame(jobs).to_csv(f"{RAW_DIR}/job_descriptions.csv", index=False)
print(f"Generated {len(resumes)} resumes and {len(jobs)} job descriptions.")
