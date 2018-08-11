FROM mannickutd/alpine-python3

WORKDIR /

RUN mkdir -p /opt/mannickutd/etc/services/shortened_url

WORKDIR /opt/mannickutd/etc/services/shortened_url

COPY . ./

RUN mkdir logs

COPY ./app_nginx.conf /etc/nginx/conf.d/

RUN pip3 install --no-cache-dir --ignore-installed -r requirements.txt
