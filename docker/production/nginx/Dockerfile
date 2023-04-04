FROM nginx:stable-alpine

# Pass build arguments
ARG NGINX_HOST
ARG SSL_CERTIFICATE
ARG SSL_CERTIFICATE_KEY

# Pass NGINX_HOST as an environment variable
ENV NGINX_HOST=${NGINX_HOST}

# Copy SSL certificate and key
RUN mkdir /etc/nginx/ssl
COPY ${SSL_CERTIFICATE} /etc/nginx/ssl/site-ssl.crt
COPY ${SSL_CERTIFICATE_KEY} /etc/nginx/ssl/site-ssl.key

# Copy nginx configuration
COPY ./docker/production/nginx/nginx.conf /etc/nginx/nginx.conf

# Copy nginx configuration template for mysite
COPY ./docker/production/nginx/mysite.nginx.conf.template /etc/nginx/sites-available/mysite.nginx.conf.template

# Run envsubst to parse environment variables in nginx configuration template
RUN envsubst '$$NGINX_HOST' < /etc/nginx/sites-available/mysite.nginx.conf.template > /etc/nginx/sites-available/mysite.nginx.conf

# Create a symbolic link to the sites-enabled directory
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/mysite.nginx.conf /etc/nginx/sites-enabled/mysite.nginx.conf

# start nginx
CMD ["nginx", "-g", "daemon off;"]