# quaternions library

This module provides access to `quaternion` class and mathematical functions for quaternions.

This module was fun to write, so perhaps I wrote too much.

## Python requirements (at `requirements.txt`)

```
pytest
```

## Usage

- `from quaternion import quaternion, qmath`
  - `quaternion`: main class, which represents quaternions.
  - `qmath`: like `cmath` but for quaternions instead of complex values.
- Sample usage in `main.py` and `test_*.py`
- To use tests:
  - Create venv: `$ python -m venv venv`
  - Install python requirements: `$ pip install -r requirements.txt`
  - Run tests: `$ pytest --verbose`
