# Create the Virtual Environment
export WORKON_HOME=~/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv --python=/usr/bin/python3.10 digitalmap 

# activate the virtual environment
source ~/.virtualenvs/digitalmap/bin/activate

# This will use the same Python version of the virtualenv
pip install Django==3.2.18

#GDAL installation (follow following steps)

Before installing the GDAL Python libraries, you’ll need to install the GDAL development libraries.
sudo apt-get install libgdal-dev

You’ll also need to export a couple of environment variables for the compiler.

export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal

Now you can use pip to install the Python GDAL bindings.
pip install GDAL==3.4.1


Give the path in django setting: This is the optional step
if os.name == 'nt':
    VENV_BASE = os.environ['VIRTUAL_ENV']
    os.environ['PATH'] = os.path.join(VENV_BASE, 'Lib\\python3.10\\site-packages\\osgeo') + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(VENV_BASE, 'Lib\\python3.10\\site-packages\\osgeo\\data\\proj') + ';' + os.environ['PATH']
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



#postgres installation with the postgis

#It is a standard task that we need to update our system prior to the installation
sudo apt update

#Now let’s install PostgreSQL and all its dependency files
sudo apt install postgresql postgresql-contrib

#Let’s start the service
sudo systemctl start postgresql

#Create a new PostgreSQL role and database
sudo -i -u postgres
psql
CREATE USER mappers with password 'mappers123';
CREATE DATABASE digitalmap;


#Now switch to your ubuntu user and enter following command.
#Note: You must install the postgis version associated with installed postgresql
sudo apt-get install postgresql-16-postgis-3

#Connect to the your database you are wanting to install extension
\c digitalmap
GRANT ALL PRIVILEGES ON SCHEMA public TO mappers;
CREATE EXTENSION postgis;


