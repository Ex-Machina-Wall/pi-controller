#!/bin/bash
# This is a comment
cd /home/pi/repos/all-ex-machina-wall-repos/pi-controller/
rm nohup.out
nohup /home/pi/repos/all-ex-machina-wall-repos/pi-controller/.venv/bin/python /home/pi/repos/all-ex-machina-wall-repos/pi-controller/ex_wall_pi_controller/local_entrypoint.py &
