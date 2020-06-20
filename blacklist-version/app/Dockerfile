FROM python:3-onbuild
COPY . /usr/src/app
COPY run.sh /
RUN chmod a+x run.sh
CMD ["./run.sh"]