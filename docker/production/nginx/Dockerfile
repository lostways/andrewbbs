FROM nginx:latest

# Copy SSL certificate and key
COPY ./docker/production/nginx/ssl/${SSL_CERT} /etc/nginx/ssl/site-ssl.crt
COPY ./docker/production/nginx/ssl/${SSL_KEY} /etc/nginx/ssl/site-ssl.key

# Copy nginx configuration
COPY ./docker/production/nginx/nginx.conf /etc/nginx/nginx.conf

# Copy nginx configuration for mysite
COPY ./docker/production/nginx/mysite.nginx.conf /etc/nginx/sites-available/mysite.nginx.conf

# Create a symbolic link to the sites-enabled directory
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/mysite.nginx.conf /etc/nginx/sites-enabled/mysite.nginx.conf

# start nginx
CMD ["nginx", "-g", "daemon off;"]