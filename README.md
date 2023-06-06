# mlplatformutils

<br />

 **mlplatformutils for observability**

## Structure

<br />
.<br />
|-- LICENSE.txt<br />
|-- README.rst<br />
|-- setup.cfg<br />
|-- setup.py<br />
|-- src<br />
|   |-- mlplatformutils<br />
|   |   |-- __init__.py<br />
|   |   |-- core<br />
|   |   |-- |-- __init__.py<br />
|   |   |-- |-- sparkutils.py<br />
|   |   |-- |-- platformutils.py<br />
|   |   |-- |-- pandasutils.py<br />
|   |   |-- |-- lineagegraph.py<br />
|   |   |-- |-- app_insights_logger.py<br />
|-- tests<br />
|   |-- __init__.py<br />
|   |-- core<br />
|   |-- |--__init__.py<br />
|   |-- |-- sparkutils.py<br />
|   |-- |-- platformutils.py<br />
|   |-- |-- pandasutils.py<br />
|   |-- |-- lineagegraph.py<br />
|   |-- |-- app_insights_logger.py<br />
<br />

## Instructions

<br />
 install twine - twine is a utility package that is used for publishing Python packages on PyPI <br />
 
 **python -m pip install twine** <br />
 
 Build Package - create the source distribution of the package <br />
 
 **python setup.py sdist** <br />
 
 Upload Package to PyPI <br />

 ***python -m twine upload dist/* *** <br />

## Description

<br />

**app_insights_logger** - Contains **telemetrylogger** Class with Functions to Manage and Log Telemetry into Azure Application Insights <br />

<br />

**lineagegraph** - Contains **LineageGraph** Class with functions to manage Graph on Azure Cosmos DB enabled with Gremlin <br />

**platformutils** - Contains platform utility functions to check, install depedencies, check Azure ML Compute 

* is_package_installed
* install_pip
* get_environment
* set_environment
* assert_amlcompute
* read_setup_ini

**sparkutils** - Contains functions to read data from sources such as (Azure Data Lake Gen2, Azure Data Explorer (Kusto), Azure Sql Server) and write (Azure Data Lake Gen2)while ensuring integrated Lineage Graph Logging.

* read_from_adls_gen2
* write_to_adls_gen2
* read_from_kusto
* read_from_azsql

**pandasutils** - Contains functions to read data from Azure Data Lake Gen2 (from Delta Format or Parquet Format) into Pandas Dataframe without Spark while ensuring integrated Lineage Graph Logging.

* read_from_delta_as_pandas
* read_from_parquet_as_pandas
* write_pandas_as_parquet_to_adlsgen2

### Examples

<br />

**from mlplatformutils.core.platformutils import is_package_installed** <br />
**print(is_package_installed("pandas"))** <br />
**from mlplatformutils.core.app_insights_logger import telemetrylogger** <br />
**from mlplatformutils.core.lineagegraph import LineageGraph** <br />
**from mlplatformutils.core.sparkutils import write_to_adls_gen2, read_from_adls_gen2** <br />
**import mlplatformutils.core.platformutils as mlpu** <br />
mlpu.__version__ <br />