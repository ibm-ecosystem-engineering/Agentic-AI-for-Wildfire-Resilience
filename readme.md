# Agentic AI for Wildfire Resilience

Autonomous Detection, Response & Recovery

Controlled hazard burns are a key bushfire mitigation strategy, involving the deliberate burning of vegetation to lower bushfire risks.
Accurately identifying high-risk areas for these burns remains a challenge. Execution of controlled burns requires careful coordination of resources, including fire crews, trucks, aerial support, and protective equipment. 

This Watsonx.ai and CrewAI based Agentic AI application helps to identify the high-risk areas and to schedule proactively the timing and resources required to conduct the controlled burns to reduce the risk.


#### Architecture

<img src="images/arch.png">

#### Home Page

<img src="images/home.png">


## 1. Installation

#### Prerequisite

Python 3.x should be installed and available.

#### 1.1 Download this repo

1. Download this repo (https://github.com/GandhiCloudLab/BlazeBreakers). 

2. Let's assume the repository has been downloaded, and available in the location `/Users/xyz/BlazeBreakers`.

    Let's call this as a root folder.

    Don't forget to replace the `/Users/xyz/BlazeBreakers` with your folder structure, wherever we refer in this document.

#### 1.2 Create Python virtual environment

1. Open a new command or terminal window.

2. Goto the repository root folder by running the below command.

    **Note:** Don't forget to replace the `/Users/xyz/BlazeBreakers` with your folder structure.

    ```
    cd /Users/xyz/BlazeBreakers
    ```

3. Create python `virtual environment` by running the below command.

    ```
    python -m venv myvenv
    source myvenv/bin/activate
    ```

4. Goto the src root folder by running the below command.

    **Note:** Don't forget to replace the `/Users/xyz/BlazeBreakers/src` with your folder structure.

    ```
    cd /Users/xyz/BlazeBreakers/src
    ```    

5. Install the required python packages by running the below command.
    ```
    python -m pip install -r requirements.txt
    ```

#### 1.3 Create .env file

1. Create `.env` file with the below entries (you should be still in the root folder of the repo /Users/xyz/ai-agent-wildfire-resilience )

```
# Environment variables
LOGLEVEL = INFO

WATSONX_IBMC_AUTH_URL = "https://iam.cloud.ibm.com/identity/token"
WATSONX_CREDENTIALS_URL = "https://us-south.ml.cloud.ibm.com"
WATSONX_API_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
WATSONX_API_KEY = ""
WATSONX_PROJECT_ID = "53302198-522e-49a6-ba45-b445d46db666"
WATSONX_MODEL_ID_TEXT = "ibm/granite-3-8b-instruct"

```

2. Update the `WATSONX_API_KEY` property with your data.

They are weather API URL and key.

#### 1.4 Start the Python app

1. Run the below commands to start the app

    ```
    python main.py
    ```

2. Verify the app is working by opening the url  http://localhost:3001 in your browser.
