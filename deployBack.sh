#!/bin/bash

nameEnv="pyRobotsEnv"
ls pyRobotsEnv &> /dev/null
nameExist=$(echo $?)
while [ $nameExist == 0 ]; do
  echo "El nombre para el entorno ya existe!"
  read -n 20 -p "De un nombre para el entorno virtual:" nameEnv
  if [ ! -f $nameEnv ]; then
    nameExist=1
  fi
done
locatePy=$(which python3)
existPy=$(echo $?)
locatePip=$(which pip)
existPip=$(echo $?)
locateVenv=$(which virtualenv)
existVenv=$(echo $?)
if [ $existPy == 1 ] || [ $existVenv == 1 ] || [ $existPip == 1 ]; then
  echo -e "Se requieren:\n[+] python3\n[+] virtualenv\n[+] pip"
  exit 1
fi
virtualenv -p $locatePy $nameEnv 
source $nameEnv/bin/activate
pip install -r requeriments.txt 
uvicorn main:app --reload
exit 0
