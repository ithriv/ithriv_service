FROM python:3.7.3-stretch
LABEL maintainer="rkc7h@virginia.edu"
ENV APP_LOC /ithriv_service
RUN mkdir -p /etc/private/ithriv
RUN mkdir -p $APP_LOC
WORKDIR $APP_LOC
ADD ./requirements.txt .
RUN pip3 install -r requirements.txt
EXPOSE 5000
RUN apt-get update
RUN apt-get install -y libmagic-dev
RUN apt-get install -y nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN apt-get install -y supervisor
ENV FLASK_APP app/__init__.py
ENV FLASK_DEBUG 0
ADD ./nginx_app.conf /etc/nginx/sites-available/default
ADD ./supervisor_app.conf /etc/supervisor/conf.d/supervisor_app.conf
ADD ./supervisor_app.conf /etc/supervisor/supervisord.conf
ADD ./. .
VOLUME ["/etc/private/ithriv","~/.aws"]
WORKDIR /home/
RUN ln -sf ~/.aws .
CMD ["supervisord"]
