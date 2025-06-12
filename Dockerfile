FROM python:3.11.12-bullseye

WORKDIR /myProjectMerchStore

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p app/core/cert && \
    if [ ! -f app/core/cert/jwt-private.pem ]; then \
        openssl genrsa -out app/core/cert/jwt-private.pem 2048 && \
        openssl rsa -in app/core/cert/jwt-private.pem -outform PEM -pubout -out app/core/cert/jwt-public.pem; \
    fi

RUN chmod +x prestart.sh

ENTRYPOINT ["./prestart.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]