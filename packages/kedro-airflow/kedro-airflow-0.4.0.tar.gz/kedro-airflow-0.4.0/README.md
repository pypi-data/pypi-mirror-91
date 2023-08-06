# Kedro-Airflow
| `develop`                                                                                                                                                                | `master`                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [![CircleCI](https://circleci.com/gh/quantumblacklabs/kedro-airflow/tree/develop.svg?style=shield)](https://circleci.com/gh/quantumblacklabs/kedro-airflow/tree/develop) | [![CircleCI](https://circleci.com/gh/quantumblacklabs/kedro-airflow/tree/master.svg?style=shield)](https://circleci.com/gh/quantumblacklabs/kedro-airflow/tree/master) |

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg)](https://pypi.org/project/kedro-airflow/)
[![PyPI Version](https://badge.fury.io/py/kedro-airflow.svg)](https://pypi.org/project/kedro-airflow/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)

[Apache Airflow](https://github.com/apache/airflow) is a tool for orchestrating complex workflows and data processing pipelines. The Kedro-Airflow plugin can be used for:
- Rapid pipeline creation in the prototyping phase. You can write Python functions in Kedro without worrying about schedulers, daemons, services or having to recreate the Airflow DAG file.
- Automatic dependency resolution in Kedro. This allows you to bypass Airflow's need to specify the order of your tasks.
- Distributing Kedro tasks across many workers. You can also enable monitoring and scheduling of the tasks' runtimes.

## Installation

`kedro-airflow` is a Python plugin. To install it:

```bash
pip install kedro-airflow
```

## Usage

You can use `kedro-airflow` to deploy a Kedro pipeline as an Airflow DAG by following these steps:

### Step 1: Generate the DAG file

At the root directory of the Kedro project, run:

```bash
kedro airflow create
```

This command will generate an Airflow DAG file located in the `airflow_dags/` directory in your project.
You can pass a `--pipeline` flag to generate the DAG file for a specific Kedro pipeline and an `--env` flag to generate the DAG file for a specific Kedro environment.

### Step 2: Copy the DAG file to the Airflow DAGs folder.

For more information about the DAGs folder, please visit [Airflow documentation](https://airflow.apache.org/docs/stable/concepts.html#dags).

### Step 3: Package and install the Kedro pipeline in the Airflow executor's environment

After generating and deploying the DAG file, you will then need to package and install the Kedro pipeline into the Airflow executor's environment.
Please visit the guide to [deploy Kedro as a Python package](https://kedro.readthedocs.io/en/latest/10_deployment/01_single_machine.html#package-based) for more details.
