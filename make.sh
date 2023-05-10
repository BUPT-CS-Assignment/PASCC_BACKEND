#!/bin/bash

cd ~/Service/PASCC_BACKEND/assets/PASCC/build
cmake .. && make
cd ../bin
chmod 777 PASCC