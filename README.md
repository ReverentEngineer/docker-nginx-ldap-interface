# docker-nginx-ldap-interface

This is a Docker image that solely provides and nginx auth to LDAP binding service.

# How to run

 docker run -d -e LDAP_URI=ldap://openldap_host -e LDAP_BIND_TEMPLATE=cn=%s,ou=people,dc=example,dc=org reverentengineer/nginx-ldap-interface
