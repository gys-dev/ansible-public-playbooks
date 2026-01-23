#!/bin/bash
source /home/{{ app_user }}/venvs/pgenv/bin/activate

/usr/bin/python3 /home/{{ app_user }}/venvs/pgenv/lib/python{{ python_version }}/site-packages/pgadmin4/setup.py
