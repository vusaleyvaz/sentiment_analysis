FROM python:3.9.0

RUN apt update && apt install -y htop

COPY . src/

RUN /bin/bash -c "cd src && pip install -r requirements.txt"

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]

