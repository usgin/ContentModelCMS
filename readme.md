## Make your own settings.py based on the template first!

## libxml2 2.9.0 is required to deal with GML schemas
    sudo apt-get install python-dev gcc make
    
    wget http://xmlsoft.org/sources/libxml2-2.0.0.tar.gz
    tar -vzf libxml2-2.9.0.tar.gz
    cd libxml2-2.9.0/
    ./configure
    make
    sudo make install
    
    sudo apt-get install python-pip libxml2-dev libxslt-dev
    sudo pip install lxml
    
## Python pre-requisites
    pip install mimeparse

## Initialize uriredirect submodule
    git submodule init
    git submodule update