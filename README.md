# Psyduck

A library for faster development of ML and python projects.

Works with python Python 3.5 and above.

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

Here's how to use `psyduck` in your application:

### Install from nexus
`pip install psyduck`

### Latest install
1. git clone repo
2. `python setup.py install`
