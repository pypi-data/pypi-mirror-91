from setuptools import find_packages, setup

setup(
    name="MathisonTuring",
    packages=find_packages(),
    version="0.0.4",
    description="Mathison Turing Python SDK",
    author="Daniel David",
    author_email="daniel.david@mathisonturing.com",
    license="GPL",
    install_requires=["Pyrebase", "json", "validict"  ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    long_description=
    
"""
# MathisonTuring

[MathisonTuring](https://mathisonturing.com) is a Python library for submitting tasks in projects created in the [Mathison Turing](https://mathisonturing.com) website.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install mathisonturing
```

## Login

```python
import mathisonturing.tools as mt

project_name = mt.auth(institution, project, token) # returns auth class
```

## Bounding box task

```python
## dict example
dict = {
        "instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "min_width":int,
        "min_height": int,
        "if_not_conclusive": str,
        }

## publish bounding box task
project_name.bounding_box(dict).publish()
```

## Classification task

```python
## dict example
dict = {
        "instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "choices":bool,
        "if_not_conclusive": str,
        }

## publish classification task
project_name.classification(dict).publish()
```

## Cuboid task

```python
## dict example
dict = {
        "instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "if_not_conclusive": str,
        }

## publish classification task
project_name.cuboid(dict).publish()
```

## Splines task

```python
## dict example
dict = {
        "instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "splines":bool,
        "with_labels":bool,
        "if_not_conclusive": str,
        }

## publish classification task
project_name.splines(dict).publish()
```

## Point task

```python
## dict example
dict = {
        "instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "splines":bool,
        "with_labels":bool,
        "if_not_conclusive": str,
        }

## publish classification task
project_name.point(dict).publish()
```

## Polygon task

```python
## dict example
dict = {
        "instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "if_not_conclusive": str,
        }

## publish classification task
project_name.polygon(dict).publish()
```

## Segmentation task

```python
## dict example
dict = {
        "instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "if_not_conclusive": str,
        }

## publish classification task
project_name.segmentation(dict).publish()
```

## Transcription task

```python
## dict example
dict = {
        "instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "if_not_conclusive": str,
        }

## publish classification task
project_name.transcription(dict).publish()
```

## License
[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
""",
    long_description_content_type='text/markdown',
)