start_frontend:
	streamlit run frontend.py

start_backend:
	uvicorn app:app --reload --port 8000

kill_servers:
	-sudo lsof -t -i tcp:8000 | xargs kill -9
	-sudo lsof -t -i tcp:8501 | xargs kill -9

start_servers: kill_servers start_frontend start_backend
	echo "Servers are started!"


