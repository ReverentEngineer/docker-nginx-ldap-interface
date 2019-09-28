FROM pypy
RUN apt update && \
  apt install -y gcc libldap2-dev libsasl2-dev && \
  pip install flask python-ldap gunicorn
ADD src /opt/app
WORKDIR /opt/app
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0", "app:app"]
