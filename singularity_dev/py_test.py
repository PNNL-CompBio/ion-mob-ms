#!/usr/bin/python3
import sys
import os

print("hello this is python")


os.system("""echo 'sudo python3 /vagrant/dev_dockerized/drf/pipeline.py' > /Pipe/mypipe""")
