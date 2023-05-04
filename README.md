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


### Important steps and links

1. `-` can be used in makefile to continue executing next commands even if error occurs in one of the commands
2. `-j2` can be used in makefile to return the control to terminal when an app starts. If we don't use `-j2` when calling the makefile and if we want to run two servers, then when one server starts, it doesn't transfer the control to makefile again. So the next commands are not executed. `-j2` transfers the control to makefile.
3. Get elastic ip for the ec2 instance. Elastic ips are fixed ips. 
4. Purchase a domain name on GoDaddy. Create hosted zone on `AWS Route 53` with the obtained domain name. Replace the `NameServers` (NS) on GoDaddy with the 4 NameServers obtained after creating hosted zone on route 53. The following message will then appear on GoDadday dashboard:
    `We can't display your DNS information because your nameservers aren't managed by us.`
This means you have successfully transfered the NameServers to AWS.
5. Add Type `A` record to route 53 with the public ip of the ec2 instance.
6. Now run the server on the instance and try to check if domain works. Currently, it will be http. 
7. Use streamlit docker + traefik docker + let's encrypt for getting ssl certificate. 
    Forum: https://discuss.streamlit.io/t/deploying-streamlit-with-traefik-and-docker/27100
    GitHub link: https://github.com/joeychrys/streamlit_deployment
8. While doing above, the streamlit and backend host should be kept default and not `0.0.0.0`. There is a `host address` difference between running the docker locally, and running the dockers with docker-compose. Check `Makefile`, compare `start_frontend_locally` and `start_frontend` for host difference
9. For google analytics, create `property` on Google Analytics dashboard. Provide domain name and give permissions. After this, google provides and script to add to all page files of the domain/website. 
10. For streamlit apps, only the `index.html` file needs to be updated with the above script. 
11. The index.html can be found at this location: `/home/admin/anaconda3/envs/beast/lib/python3.10/site-packages/streamlit/static/index.html`. Here, `beast` is my env name. It will be different for you.
12. Copy this file to the project directory. Add the Google Analytics script to the copied file and then copy the file to dockerfile using `COPY` command at the location `/opt/conda/lib/python3.10/site-packages/streamlit/static/index.html` inside the container. This location is avaiable because I used `continuumio/miniconda3` base image. It might differ for your base image. 
13. To find the location of the file, run the docker with `print(st.__file__)` inside one of the streamlit python files to print the location of the index.html file. Then use `docker exec -it {container_name} /bin/bash` to go inside the docker and verify the location. Use this location in the DockerFile to COPY the index.html from local to docker. 
14. No need of AWS Certificate Manager, AWS CloudFront, AWS LoadBalancer, etc. for SSL. 
15. Traefik is reverse proxy and loadbalancer. It is competitor on Nginx and much easier to setup.
16. Contact form integrated inside app using FormSubmit. Link: https://formsubmit.co/
17. Following links for adding social media handles to streamlit:
Linkedin Profile: https://www.youtube.com/watch?v=R361fvf3Cic
Twitter follow button: https://publish.twitter.com/?buttonType=FollowButton&query=https%3A%2F%2Ftwitter.com%2FTwitterDev&widget=Button
18. Different types of retrieval: https://blog.langchain.dev/retrieval/#:~:text=The%20main%20way%20most%20people,for%20storing%20and%20querying%20vectors).
19. ngrok can also be used for https, reverse-proxy
20. ToDO: Add Stripe Checkout page to enable Apple Pay and Google Pay: https://stripe.com/docs/checkout/quickstart?lang=python

#### How I ran in development

1. Build image locally using `docker build -t ghcr.io/virajbagal/text:latest .`
2. Push to GCR: `docker push ghcr.io/virajbagal/text:latest`
3. ssh into ec2 instance
4. Pull the image: `docker pull ghcr.io/virajbagal/text:latest`
5. `sudo ACTIVELOOP_TOKEN=YOURKEY OPENAI_API_KEY=YOURKEY docker-compose -f production.yml up`

Before pushing and pulling we need to setup credentials using github token. Process can be found here:
https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry


### Pytube error

We need to use `video = YouTube(url, use_oauth=True, allow_oauth_cache=True)`. Start the server, you will get a link for authentication. Allow permissions by clicking on the link. Next time onwards, it won't ask for authentication. This authentication expires sometimes, so repeat the process.

Run the `test.py` (`/home/admin/textassisstant/textassistant/test.py`) file locally to do the above process. A `token.json` is generated at `/home/admin/anaconda3/envs/beast/lib/python3.10/site-packages/pytube/__cache__/tokens.json`. Copy that file to this project dir. This will allow docker to copy this token.json in the image and use in on server 