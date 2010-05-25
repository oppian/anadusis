To setup development environment:

/usr/bin/python2.6 lib/pinax/scripts/pinax-boot.py --development --source=lib/pinax pinax-env
 
source pinax-env/bin/activate
 
pip install --no-deps --requirement lib/pinax/requirements/pinax.txt
 
pip install --no-deps --requirement requirements.txt

python lib/pinax/scripts/pinax-boot.py --development--source=lib/pinax pinax-env


change