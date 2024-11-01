#!/bin/bash
export FLASK_APP=flask_ml_app
export FLASK_ENV=development
echo "flask set complete...!!!"
echo "flask run...!!!"
flask run --host=0.0.0.0
