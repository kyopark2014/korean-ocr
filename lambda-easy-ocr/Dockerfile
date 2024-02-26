FROM amazon/aws-lambda-python:3.11
WORKDIR /var/task/lambda-chat

COPY lambda_function.py /var/task/
COPY test.py /var/task/   
COPY . ..

RUN /var/lang/bin/python3.11 -m pip install --upgrade pip
RUN /var/lang/bin/python3 -m pip install easyocr Pillow numpy

CMD ["lambda_function.lambda_handler"]


# FROM public.ecr.aws/lambda/python:3.8
# RUN yum -y install gcc python3-devel zlib-devel libjpeg-devel
# RUN pip install easyocr Pillow numpy
# COPY index.py ./
# CMD ["index.lambda_handler"]
