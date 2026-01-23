# ansible-scripts

## Install
- Ansible
- sshpass
```
brew install hudochenkov/sshpass/sshpass 
```

## Run
- Skip to check host

```
export ANSIBLE_HOST_KEY_CHECKING=False 

```

- Run playbook

```
ansible-playbook -i hosts -l host0 playbooks/apache.yml
```

### Including: 

- hosts: File hosts contain config server
- host0: Hostname that you want to run
- playbooks/apache.yml: Playbook you want to run


## Structure

```
├── files
│   ├── id_rsa
│   └── id_rsa.pub
├── playbook.yml
├── readme.md
└── vars
    └── default.yml
```

### Including:
- files: File template
- playbook.yml: main playbook
- vars: variables. Before run scripts please edit this file

