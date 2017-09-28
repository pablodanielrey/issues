#!/bin/bash
python3 issues/registrar.py issues_web / issues.econo.unlp.edu.ar:5015 &
python3 issues/registrar.py issues_rest /issues/api issues.econo.unlp.edu.ar:5016
