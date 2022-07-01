FROM tobix/pywine:3.9

#WORKDIR /usr/src/app



RUN echo "hi"

RUN bash -c 'ls'


RUN echo $INPUT_spec_file
RUN echo $spec

RUN apt-get update && apt-get install -y python3-pip

RUN bash -c "(set -o posix ; set)"


COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pyinstaller_script.py /pyinstaller_script.py
RUN bash -c "ls"
RUN bash -c "ls /usr/src/apps"


RUN chmod +x /pyinstaller_script.py


ENTRYPOINT ["python", "/pyinstaller_script.py"]
