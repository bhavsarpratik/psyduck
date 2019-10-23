# Psyduck

A library for faster development of ML and python projects.

Works with python Python 3.5 and above.

## Project Organization

---

```
    ├── psy                    <- Source code for use in this project
    │   │      
    │   └──utilities          
    |   |   └──helpers         <- Common helper functions
    |   |   └──loggers         <- Logging classes
    |   |   └──aws             <- For interacting with AWS
    │   └──ml                  
    |       └──metrics         <- For generating metrics
    |       └──plotting        <- For plotting functions
    |       └──imbalance       <- For dealing with imbalanced dataset
    |       └──preprocessors   <- For preprocessing data
    │      
    ├── README.md              <- The top-level README for developers using this project
    │      
    ├── requirements.txt       <- The requirements file for reproducing the development environment, e.g.
    │                             generated with `pip freeze > requirements.txt`
    └── setup.py               <- makes project pip installable (pip install -e .) so msmlkit can be imported
```

Here's how to use `psyduck` in your application:

### Install from nexus
`pip install psyduck`

### Latest install
1. git clone repo
2. `python setup.py install`
