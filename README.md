### Installation Serveur identity:

```bash
$pip install fask
$pip install tankerdk-indentity
```

### Installation Client App:

```bash
$python3 -m venv .venv
$source .venv/bin/activate
$python -m pip install --upgrade pip
$python -m pip install tankersdk \
   --extra-index-url https://gitlab.com/api/v4/projects/20920099/packages/pypi/simple
```

[Tanker Documentation]([Core &ndash; Python - Tanker documentation](https://docs.tanker.io/latest/api/core/python/))



### Usage Serveur:

```bash
FLASK_DEBUG=1 FLASK_APP=identity-server.py flask run
```

### Usage Client:

```bash
python main.py
```



### Note:

A tanker account is neccessary:

[Tanker Dashbord](https://dashboard.tanker.io/)



The configuration file of your Tanker application must be called `config-app.json`.

It contains:

- app_id

- app_secret

- auth_token



These information are available on the dashbord of your application.


