# InsightAI

Website: https://getaiinsights.com/
AI that can quickly summarize and allow Q&amp;A on PDFs, Docs, Images and Youtube videos.

Tech used:
1. FastAPI - for backend APIs
2. Streamlit - for frontend
3. Langchain - for backend logic
4. GPT-4 and GPT-3.5-turbo API calls
5. Prompt Engineering for different types of AI responses, and also to stop Prompt Injection Attacks
6. Activeloop as vector database
7. Retrieval augmented generation for QA
8. Detectron2 + Tesseract for text in image parsing
9. Some HTML and CSS for frontend customization
10. Google Analytics integrated
11. Traefik as reverse proxy for ssl connection (https)
12. Lets encrypt for ssl certificates
13. Docker and Docker compose for running everything
    
### How to run locally

Prerequisite: Install docker

1. Clone the repository
2. Uncomment the last line (`CMD` line) in Dockerfile and comment the 3rd last `CMD` line
3. `docker build -t localrun:latest .`
4. Create `.env` file with your own `OPENAI_API_KEY` and `ACTIVELOOP_TOKEN` at the root location of the project. Each can be obtained after creating account on `OpenAI` and `Activeloop` websites. You will be charged by OpenAI. The format of `.env` is as following:
   ```
   OPENAI_API_KEY=YOURKEY
   ACTIVELOOP_TOKEN=YOURKEY
   ```
5. `docker run -p 8501:8501 --env-file .env -v YOUR_LOCAL_PATH:/textassistant/received_files -v YOUR_LOCAL_PATH:/textassistant/logs --name test localrun:latest`
6. Open any browser and go to `127.0.0.1:8501` to see the project

Use `./kill_all_containers.sh` to stop the servers

If you want to run in production without SSL, then same above commands will work on ec2 and you can go to the ip of ec2 in chrome to see the project. If domain name is obtained and setup is done on AWS Route 53 with ip given to `A` type record, then you can even use domain name for checking it on browser.

### How to run in production with reverse proxy and SSL

Prerequisites: Needs instance with more than 2GB RAM, Install docker and docker compose

1. Clone the repo
2. `cd` to repo
3. `sudo ACTIVELOOP_TOKEN=YOURKEY OPENAI_API_KEY=YOURKEY docker-compose -f production.yml up`

### Videos

#### PDF Summary

https://user-images.githubusercontent.com/51148252/235320657-b371756f-e74f-4eba-abe5-70b7ce8c3ab8.mp4

#### PDF Q&A

https://user-images.githubusercontent.com/51148252/235320677-7c076c4b-3261-4bf5-b8c6-5cad157d56be.mp4

#### Youtube Video Summary and Q&A

https://user-images.githubusercontent.com/51148252/235320693-6aca9ce2-32d2-4d15-a897-f8c9aac45a93.mp4
