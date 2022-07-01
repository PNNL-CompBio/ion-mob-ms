FROM tobix/pywine:3.9

#WORKDIR /usr/src/app



RUN echo "hi"

RUN bash -c 'ls'


RUN echo $INPUT_spec_file
RUN echo $spec


RUN bash -c "(set -o posix ; set)"

RUN apt-get update && apt-get install -y python3-pip

# COPY ../../requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt


ENV PORT 80
WORKDIR dist
COPY . dist
RUN bash -c 'ls dist'
RUN bash -c 'pwd'
RUN bash -c "ls"
RUN bash -c "ls /usr/src/apps"

COPY ../../requirements.txt /requirements.txt

RUN chmod +x /pyinstaller_script.py


ENTRYPOINT ["python", "/pyinstaller_script.py"]
