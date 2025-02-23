# DataScienceAgent

Steps to Run the Agent API and UI:
Before proceeding with the below steps, Git clone this repo locally to a new folder. VSCode is recommended.

1. Install Docker Desktop (https://www.docker.com/products/docker-desktop/) and pull official MongoDB community server image from Docker Hub by using the following command in the docker desktop terminal:
docker pull mongodb/mongodb-community-server
2. Run the docker image as a container using the below command:
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
3. Install MongoDB compass (https://www.mongodb.com/products/tools/compass) and connect to the MongoDB community server running in Docker using 'mongodb://localhost:27017/' connection string.
4. Once connected to the server, create a new DB 'chatHistory' using compass UI
5. Install Python 3.11.9 (for better compatability) and create a new virtual environment using the below command:
   python3 -m venv .venv
6. Activate the vitual environment using:
   source .venv/bin/activate
7. Then intall the required libraries using:
   pip freeze > requirements.txt
8. Update the credentials with the llm of your choice in the DataScienceReactAgent.py file.
9. Run the 'DataScienceReactAgent.py' using:
   python DataScienceReactAgent.py
10. To run the UI to interact with the Agent:
    streamlit run Streamlit_ui.py

    Here is the Markdown content ready to be copied and pasted directly into your README.md file:
markdown
# DataScienceAgent

## Steps to Run the Agent API and UI

Before proceeding with the below steps, clone this repository locally to a new folder. It is recommended to use VSCode for this project.

1. **Install Docker Desktop and Pull MongoDB Image**  
   Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and pull the official MongoDB community server image from Docker Hub by running the following command in the Docker Desktop terminal:

   ```bash
   docker pull mongodb/mongodb-community-server
Run MongoDB Container
Run the Docker image as a container using the below command:
bash
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest
Install MongoDB Compass and Connect
Install MongoDB Compass and connect to the MongoDB community server running in Docker using the connection string mongodb://localhost:27017/.
Create Database
Once connected to the server, create a new database named chatHistory using the Compass UI.
Install Python and Create Virtual Environment
Install Python 3.11.9 (for better compatibility) and create a new virtual environment using the following command:
bash
python3 -m venv .venv
Activate Virtual Environment
Activate the virtual environment using:
bash
source .venv/bin/activate
Install Required Libraries
Install the required libraries using:
bash
pip install -r requirements.txt
Note: The original instructions mentioned pip freeze > requirements.txt, which is likely a typo. It should be pip install -r requirements.txt to install the dependencies from the requirements.txt file provided in the repository.
Update Credentials
Update the credentials with the LLM (Language Model) of your choice in the DataScienceReactAgent.py file.
Run the Agent Script
Run the DataScienceReactAgent.py script using:
bash
python DataScienceReactAgent.py
Run the UI
To run the UI and interact with the Agent, use:
bash
streamlit run Streamlit_ui.py

You can copy this entire block and paste it directly into your `README.md` file. It’s formatted with clear headings, numbered steps, and code blocks for easy readability and execution.
