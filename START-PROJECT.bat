@echo off
title Subindo Projeto

echo [1/3] Cleaning project...
docker-compose down --remove-orphans -v

echo [2/3] Starting containers...
docker-compose up -d

echo [3/3] Checking status...
docker-compose ps

pause