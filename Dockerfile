FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# При запуске в контейнер обязательно указываем через --env-file /<путь до>.env (.env берем у Майкла)
# ENV файл со всеми доступами у Майкла !