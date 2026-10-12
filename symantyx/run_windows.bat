@echo off
title Symantyx Path Builder
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Install Python 3.8+ from python.org
    pause & exit /b 1
)
python "%~dp0symantyx_path_builder.py"
if %errorlevel% neq 0 ( echo. & echo Something went wrong. & pause )
