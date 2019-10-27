#!/bin/bash
pip install -r requirements.txt && ( ./start_schedular.sh &  ./start_executor.sh )
$SHELL