# xtapi
xtapi base on FastAPI

## Install

```bash
pip install xtapi
```

## demo

```python
# main.py
from xtapi.main import MainApp

app = MainApp()

if __name__ == '__main__':
    app.run(name='main:app', reload=True)
```

**Run server**

```bash
python main.py
```
