FROM nginx:1.15.8

# This is the Dockerfile for the nginx image. It replaces the default conf file
# with the one provided here. That one reads in the project.conf file, where our
# app-specific configurations reside.

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/
EXPOSE 80