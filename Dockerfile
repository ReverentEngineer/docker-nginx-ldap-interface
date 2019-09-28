FROM pypy
ADD src /opt/app
WORKDIR /opt/app
RUN apt update && \ 
  apt install -y gcc libldap2-dev libsasl2-dev && \
  pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0", "app:app"]
