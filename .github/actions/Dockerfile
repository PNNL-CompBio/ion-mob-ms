FROM tobix/pywine:3.9

#WORKDIR /usr/src/app


RUN bash -c /bin/echo -e "hi"

RUN bash -c 'ls *'
RUN bash -c /bin/echo -e "$spec_file"
RUN bash -c /bin/echo -e "$spec"



COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pyinstaller_script.py /pyinstaller_script.py
RUN chmod +x /pyinstaller_script.py


ENTRYPOINT ["python", "/pyinstaller_script.py"]