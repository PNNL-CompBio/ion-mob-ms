AWS/Cloud Command Line Interface
==============
AWS/ Cloud is an excellent method to run your pipeline if you are familiar 
with using a command line interface and have access to an AWS account.
It is recommended to to use an S3 bucket to transfer your data to and from AWS.
The Ion Mobility Dashboard utilizes EC2 instances to process data.



AWS EC2 Instance Specifications 
---------------------------
* Amazon Linux 2 (HVM)
* Kernel 5.10
* SSD Volume Type
* Architecture: 64-bit x86
* Minimum Instance type: t2.large -  Higher CPU/Memory will result in faster processing.
* Storage type: gp2
| Storage depends on user needs:
| SteppedField: we recommend allocating 14 times the storage that the input data takes up. 
| SingleField: we recommend allocating 5 times the storage that the input data takes up. 
| SLIM: Currently Unknown. To be updated by dev.


AWS Commands
---------------------------

**Setup**   

.. code-block::  

   sudo yum install git
   git clone https://github.com/PNNL-CompBio/ion-mob-ms.git
   sudo amazon-linux-extras install docker
   sudo service docker start
   sudo systemctl enable docker
   sudo usermod -a -G docker ec2-user
   cd ion-mob-ms
   pip3 install -r requirements_py3.7_CLI.txt
   
**Run Test Data** 

.. code-block::  
   
   cd User_InterfaceV2
   python3 CLI.py --json sample.json
   
   
   
   
