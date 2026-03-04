# Dockerfile

# השתמש בתדמית בסיס של Python
FROM python:3.9-slim
# הגדר ספריית עבודה באפליקציה
WORKDIR /app

COPY . /app

# התקן את התלויות הנדרשות
RUN pip install --no-cache-dir -r  requirements.txt

# הפורט שעליו Flask מאזין
EXPOSE 5000

# פקודת ההפעלה של Flask
CMD ["python", "app.py"]
