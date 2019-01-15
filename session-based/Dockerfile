FROM ubuntu:16.04

#Enter email and password (only gmail account)
ENV ngsi_address_send email
ENV ngsi_encrypt_pass password_email

ENV S_ASDW_K Encrypt_ITESM_LOGIN
COPY /encrypt /encrypt
RUN apt update 
RUN apt install -y default-jre \
	default-jdk \
	python2.7 \
	python-pip\
	curl; \
	pip install Flask\
	gunicorn\
	pymongo\
	validate_email\
	PyDNS;
EXPOSE 2121
WORKDIR /encrypt
CMD ["gunicorn","--bind","0.0.0.0:2121","wsgi"]


