create_dirs:
	mkdir -p database
	mkdir -p received_files
	mkdir -p logs

start_frontend:
	streamlit run Home.py --server.port=8501 

start_backend:
	uvicorn app:app --reload --port 8000

start_frontend_locally:
	streamlit run Home.py --server.port=8501 --server.address=0.0.0.0

start_backend_locally:
	uvicorn app:app --reload --port 8000 --host 0.0.0.0

kill_servers:
	-sudo lsof -t -i tcp:8000 | xargs kill -9
	-sudo lsof -t -i tcp:8501 | xargs kill -9

start_servers: create_dirs kill_servers create_dirs start_frontend start_backend
	echo "Servers are started!"

# used for starting servers locally for testing
start_servers_locally: create_dirs kill_servers create_dirs start_frontend_locally start_backend_locally
	echo "Servers are started!"


