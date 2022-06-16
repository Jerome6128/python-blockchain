**Activate the virtual environment**
```
source blockchain-env/bin/activate   
```

**Install all packages**
```
pip3 install -r requirements.txt
```

**Run the test**
Make sure to activate the virtual ennvironment
```
pytest backend/tests 
```

**Run the application and API**
Make sure to activate the virtual ennvironment
```
python3 -m backend.app 
```

**Run a peeer instance**
Make sure to activate the virtual ennvironment
```
export PEER=True && python3 -m backend.app
```