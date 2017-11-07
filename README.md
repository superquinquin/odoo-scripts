Odoo Scripts
==========================

Script used to interact with odoo
## Requirements

### Repository
Just clone the repo where you want

```shell
mkdir sqq
cd sqq
git clone https://github.com/superquinquin/odoo-scripts.git 
cd odoo-scripts
```

### Virtualenv
You need to have python3. Package requirements are handled using pip. To install them do :

```shell
virtualenv -p python3 ~/venv/sqq
source ~/venv/sqq/bin/activate
pip install -r requirements.txt
```

### Odoo configuration
You need to edit ~/.odoo.conf and add a section related to the odoo instance.
Eg:

```shell
[sqq-prod]
protocol=jsonrpc+ssl
port=443
url=urlofthesite.toto.fr
version=9.0
db=superquinquin
user=youuser
password=yourpassword
```

## Dev dependencies
Dependencies are managed with pip-compile. Install install with 
```shell
pip install -r requirements.dev.txt
```
To add a dependency, add it to `requirements.in` and execute pip-compile.
```
vim requirements.in
pip-compile requirements.in
pip install -r requirements.txt
```
