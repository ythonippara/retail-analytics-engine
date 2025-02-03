# retail-analytics-engine
Retail Analytics Engine is a Python-based data processing pipeline designed to extract, clean, and prepare retail data for machine learning and analytics. It automates file extraction, preprocessing, and structuring, enabling seamless data-driven decision-making in retail operations.

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```sh
git clone https://github.com/ythonippara/retail-analytics-engine.git
cd retail-analytics-engine
```


### 2. Create a Virtual Environment

It’s recommended to use a virtual environment to manage dependencies.

For Windows (PowerShell):

    ```sh
    python -m venv venv
    venv\Scripts\Activate
    ```


For macOS/Linux:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```


### 3. Install Dependencies

Once the virtual environment is activated, install the required Python packages:


    ```sh
    pip install -r requirements.txt
    ```


### 4. Configure the Project

Modify the ```config/config.json``` file if necessary to specify paths and parameters.
Example:

    ```sh
    {
        "data_path": "data/",
        "raw_data_path": "data/raw/",
        "clean_data_path": "data/clean/",
        "log_file": "logs/processing.log"
    }
    ```

### 5. Run the Data Pipeline

Execute the full pipeline to download and extract the zipped file into the data/raw/ directory. Then to clean the data and save it in data/clean directory.
Finally, the script will call sales_predictor.py to futher preprocess data, split it into training and test sets, and make a prediction using linear regression model.

    ```sh
    python scripts/pipeline_runner.py
    ```


### 6. Run tests on Functions

Run test on clean_items_data function using command below:

    ```sh
    python -m tests.test_clean_items
    ```


### 7. Use Jupyter Notebooks for Exploraroty Data Analysis (EDA)

To explore and analyze data interactively, launch Jupyter Lab:

    ```sh
    jupyter lab
    ```


### 8. Deactivate Virtual Environment (When Done)

    ```sh
    deactivate
    ```







