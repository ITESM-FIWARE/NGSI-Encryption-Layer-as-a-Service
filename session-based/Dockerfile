FROM ubuntu:16.04
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
#Password mail gmail 
ENV P_SADEWDA_E password_mail
ENV S_ASDW_K Encrypt_ITESM_LOGIN


