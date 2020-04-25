# Psyduck

A library for faster development of ML and python projects.

Works with Python 3.5+.

## Project Organization

---

```
    ├── psy                    
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
    ├── README.md              
    │      
    ├── requirements.txt      
    │                             
    └── setup.py               
```


### Install with pip
`pip install psyduck`

### Latest install
1. git clone repo
2. `python setup.py install`
