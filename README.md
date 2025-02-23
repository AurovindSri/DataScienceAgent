# DataScienceAgent

## Steps to Run the Agent API and UI

Before proceeding with the below steps, clone this repository locally to a new folder. It is recommended to use VSCode for this project.

1. **Install Docker Desktop and Pull MongoDB Image**<br>
   Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and pull the official MongoDB community server image from Docker Hub by running the following command in the Docker Desktop terminal:
   ```bash
   docker pull mongodb/mongodb-community-server

2. **Run MongoDB Container**<br>
   Run the Docker image as a container using the below command:<br>
   ```bash
   docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest

3. **Install MongoDB Compass and Connect**<br>
   Install [MongoDB Compass](https://www.mongodb.com/products/tools/compass) and connect to the MongoDB community server running in Docker using the connection string ```mongodb://localhost:27017/```.

4. **Create Database**<br>
   Once connected to the server, create a new database named chatHistory using the Compass UI.

5. **Install Python and Create Virtual Environment**<br>
   Install Python 3.11.9 (for better compatibility) and create a new virtual environment using the following command:<br>
   ```bash
   python3 -m venv .venv

6. **Activate Virtual Environment**<br>
   Activate the virtual environment using:<br>
   ```bash
   source .venv/bin/activate

7. **Install Required Libraries**<br>
   Install the required libraries using:<br>
   ```bash
   pip install -r requirements.txt

8. **Update Credentials**<br>
   Update the credentials with the LLM (Language Model) of your choice in the DataScienceReactAgent.py file.

9. **Run the Agent Script**<br>
    Run the DataScienceReactAgent.py script using:<br>
    ```bash
    python DataScienceReactAgent.py

10. **Run the UI**<br>
    To run the UI and interact with the Agent, use:<br>
    ```bash
    streamlit run Streamlit_ui.py
