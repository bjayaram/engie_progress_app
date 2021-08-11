# engie_progress_app

## Installation

First, make sure that the version of `python3` you have is 3.6 or higher:
`$ python3 --version`

If not, upgrade your Python interpreter.

It is probably best to run the programs in this tutorial in a virtual environment so that your system wide Python interpreter is not affected, though this is not a requirement.
The following commands create a directory for this tutorial, then create a virtual environment named jp and activate it and finally install JustPy and its dependencies:

```
$ mkdir progressapp
$ cd progressapp
$ python3 -m venv jp
$ source jp/bin/activate
(jp) $ pip install justpy
```

On Microsoft Windows, the activation command for the virtual environment is `jp\Scripts\activate` instead of the source command above.

You will also need to have the MySQL server running locally.

Now, copy the files main.py and sql.py into the progressapp folder.

Change the following line in sql.py to fill in the variables in upper case

```
    db_connection_str = 'mysql+pymysql://USERNAME:PASSWORD@localhost/DATABASE_NAME'
```

## Running the Program

To run the program execute the following command:

```
$ python3 main.py
```

Then, direct your browser to http://127.0.0.1:8000 or http://localhost:8000/ 

This refers to port 8000 on the local machine and should work in most environments. 

# Deployment to a cloud service (Google, AWS, Digital Ocean etc.)

If you need a public URL to access this app,
Launch a Linux Virtual Machine on your preferred cloud service.

If you are not a superuser, become one. 

Update your machine and install pip3:

```
apt update
apt install python3-pip
```

This will prepare your VM to run your JustPY program.

Then, set the `HOST` parameter in the configuration file justpy.env to the public IP address of the VM or to '0.0.0.0' (one should work). If you want to use the default port, set the `PORT` parameter to 80 (otherwise port 8000 will be used). In some cloud services only port 80 is supported by default. In some cloud services, if you are not logged in as root by default, you will need to run the program with sudo.

For example you may add the following two lines to justpy.env:
```python
HOST = '0.0.0.0'
PORT = 80
```

Alternatively, you can use the `host` and `port` parameter in the `justpy` command.

Now, point your browser to your VM using the IP address and port and you should be good to go. If your VM is assigned a domain name, you can use that. 
