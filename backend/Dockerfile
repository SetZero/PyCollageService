FROM tiangolo/uwsgi-nginx-flask:python3.10
# RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY ./src/requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt