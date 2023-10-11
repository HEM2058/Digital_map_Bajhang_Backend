# Create the Virtual Environment
export WORKON_HOME=~/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
mkvirtualenv --python=/usr/bin/python3.10 geowild  

# activate the virtual environment
source ~/.virtualenvs/geowild/bin/activate

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


Give the path in django setting
if os.name == 'nt':
    VENV_BASE = os.environ['VIRTUAL_ENV']
    os.environ['PATH'] = os.path.join(VENV_BASE, 'Lib\\python3.10\\site-packages\\osgeo') + ';' + os.environ['PATH']
    os.environ['PROJ_LIB'] = os.path.join(VENV_BASE, 'Lib\\python3.10\\site-packages\\osgeo\\data\\proj') + ';' + os.environ['PATH']
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
