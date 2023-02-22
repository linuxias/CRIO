# CRIO (Clone Repositories In Organization)
This repository is to clone repositories in specific organization


### Usage
You can use this tool to clone all repositories in Organization you are joined already.
Github Token is essential to use this tool.

#### 1. Please input your github token in the file 'crio_cfg.ini'

```
[DEFAULT]
Token = input_your_github_token
```

#### 2. Run script with arguments
```bash
$python crio.py -o org_name
```
