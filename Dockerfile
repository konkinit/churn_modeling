FROM python:3.10-slim

COPY . ./churn_modeling

WORKDIR /churn_modeling

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "./src/frontend/Onboarding.py", "--server.port", "8501"]
