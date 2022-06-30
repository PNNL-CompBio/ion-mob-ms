FROM tobix/pywine:3.9

#WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY pyinstaller_script.py /pyinstaller_script.py
RUN chmod +x /pyinstaller_script.py


ENTRYPOINT ["python", "/pyinstaller_script.py"]