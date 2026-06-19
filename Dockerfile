FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /uygulama

COPY requirements.txt /uygulama/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /uygulama

RUN chmod +x /uygulama/Backend/giris_noktasi.sh

EXPOSE 8000

CMD ["/uygulama/Backend/giris_noktasi.sh"]
