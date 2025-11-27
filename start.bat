@echo off
echo Starting Backend Server...
cd backend
call venv\Scripts\activate
start cmd /k python main.py
cd ..

timeout /t 3

echo Starting Frontend Server...
cd frontend
start cmd /k npm run dev
cd ..

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
