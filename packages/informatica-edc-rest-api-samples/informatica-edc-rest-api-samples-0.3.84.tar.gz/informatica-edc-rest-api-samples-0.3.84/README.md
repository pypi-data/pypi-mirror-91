# Informatica EDC REST-API samples using python

Contains examples for connecting to and generating attribute level lineage in EDC via python.

Requirements
------------
* python 3.6+
* Python editors (ide/environments)
  * VS Code - good support for python - free an runs on all platforms  https://code.visualstudio.com/
  * pycharm - https://www.jetbrains.com/pycharm/
  * anaconda - for JupterLab/Notebooks https://www.anaconda.com/ (includes vscode)
  * Eclipse - ide for java/python (python using/installing pydev)
    * Download: http://www.eclipse.org/downloads/eclipse-packages/
* other useful tools
  * rest api clients - for testing syntax/api calls + the good ones generate code for many languages
    * postman - https://www.getpostman.com/
    * insomnia - https://insomnia.rest/

 
Getting Started
---------------
* verify that python is installed - v3.6+
* Create a new VSCode/pycharm/Eclipse Project and import/use the files in the python folder (not the java folder)
* Ensure EDC is running while executing the samples - try/except code will catch & immediately exit
  The property suppress_edc_calls can be set in the config.json to bypass any calls to EDC
* Use a virtual environment with python
  * python3 -m venv venv  
  * and then 
    * source venv/bin/activate (for linux/macos)
    * venv/Scripts/activate.ps1 (for windows powershell)
      Note:  you may need to execute `Set-ExecutionPolicy unrestricted` for powershell (run powershell as administrator to do this)
    * venv/Scripts/activate.bat (windows cmd)
  * after activating
      * execute the following to get the latest version for test purposes
        pip3 install --extra-index-url https://test.pypi.org/simple/ informatica-edc-rest-api-samples
      * execute the following to get a tested version (see coverage overview in htmlcoverage):
        pip3 install informatica-edc-rest-api-samples
  * Run the code (remember to have an activated venv):
    python3 run_edc_lineage.p
    

REST API Authentication
-----------------------
* the EDC rest api supports Basic Authentication only - see https://yourcatalogserver:port/access for details
* we use the python requests module for all http(s) rest calls (very easy to use)
* when making a rest api call - you can pass either the id/password - or a http header with an encoded password
* for all examples here, we initially used the id/pwd method - but have switched to use http headers
* if you are using LDAP authentication - the user must have the security domain and a '\' character prefixed to the user id
  * e.g. `COMPANY_LDAP\user_a`
* use the encodeUser.py script - to create the basic auth encoding for your user, and store in a variable named `INFA_EDC_AUTH`
  * you can set the variable for each session, so it is not stored anywhere
  * if using docker - you can add this variable to an .env file to pass to docker at runtime
  * if using VS Code - you can add and "env" setting for individual environment variables used in the debugger (launch.json)
    * e.g. "env" : {"INFA_EDC_AUTH" : "Basic dXNlcjE6YUNvbXBsIWNAdGVkUGEkM3cwcmQ="}, (works but prefer .env file)
  * Note:  any files inside of .vscode (e.g. launch.json) will be excluded from the git repo (each user has their own local version)
* In this fork setupConnection.py and the functionality to use an .env has been removed


HTTPS/TLS/SSL Connections and certificates
------------------------------------------
* assuming your catalog service is https enabled (it should be, if not so your passwords are send in clear text & set verify=False)
* you will either need to download/copy the certificate (.pem format, not .jks) locally
  * or set flags to disable certificate authentication (not recommended, but possible) 
* if your ssl certificate is self signed (also not recommended), an additional warning will need to be suppressed
  * more information about SSL authentication can be found [https://3.python-requests.org/user/advanced/#ssl-cert-verification](https://3.python-requests.org/user/advanced/#ssl-cert-verification)

 
Sample Programs in the Project
------------------------------

The following samples may no longer work in this fork of the original project. If you want to use them, please use a clone of the original project, not this fork.
* `encodeUser.py`: simple program to prompt for a userid/pwd and optionally a security domain and create a base64 encoded string that can be used for authentication in the http header.  e.g. ```"Basic dXNlcjE6YUNvbXBsIWNAdGVkUGEkM3cwcmQ="```
  * use this script before you call use the other scripts, to get the right format for authenticating & not storing passwords in the .py files
    * an alternate is to prompt for a password within your script & encode the id:password
  * use `encodeUser27.py` for legacy python
* `EDCQuery_template.py`:  a template/skeleton that shows how to connect to the catalog and execute a search using python.  the result-set processing includes handling the paging model.  It also uses the `get_fact_value` method in `edcutils.py` to extract the item name from the facts array
* Utility/Heloer Scripts
  * `edcutils.py`:  utility/helper methods for common tasks - like get an attribute value `get_fact_value(item, attrName)`
  * `edcSessionHelper.py`: EDCSession class helps you configure a requests.session object and also provides command-line args for connecting to the catalog (-c/-edcurl EDC URL, -a/--auth auth credentials (see encodeUser.py), -u username (will prompt for pwd - recommend using -a, -s/--sslcert SSLCERT).  
    * this class also supports using the following environment vars:
      * INFA_EDC_URL - e.g. http://yourcatalogserver:9085 or https://yourcatalogserver:9085
      * INFA_EDC_AUTH - e.g. "Basic dXNlcl9hOnJlYWxseXNlY3VyZXBhc3N3b3Jk" - see `encodeUser.py`
      * INFA_EDC_SSL_PEM - certificate to use to connect (or set to None - to disable ssl verfication)
    * for an example of usage - see `listAndCountCustomAttributes.py`
* `listAndCountCustomAttributes.py`: find all custom attributes (normal and classification) and count the # of times the attribute is used.  writes results to csv file (output folder can be configured)
  * supports command-line parameters and environment vars for accessing the catalog.
  * uses edcSessionHelper.py to get a session reference to any rest queries
* `listCustomAttributes.py`: simple script to print all custom attributes (name, id, type, sortable, facetable)
  * this script will list both regular custom attributes `/2/catalog/models/attributes` and reference 'classification' attributes `/2/catalog/models/referenceAttributes`
* `similarityReport.py`: v10.2.1+ utility to find & export all columns/fields with similar links
  * note:  this script will attempt to query all dataelements, even if similarity profiling was not run.  for a better implementation, use `similarityByResource.py`
* `similarityByResource.py`: utility to find and export column similarity for all resources that similarity profiling was configured.
  * supports command-line parameters and environment vars for accessing the catalog.
  * uses edcSessionHelper.py to get a session reference to any rest queries
* `dbSchemaReplicationLineage.py`: provides the ability to link tables/columns in a database schema that are replicated to other schemas/databases & no scanner exists to automatcially document these relationships.  (e.g. sqoop, scripts/code, goldengate ...)
  * see [dbSchemaReplicationLineage.md](dbSchemaReplicationLineage.md) for more
* `externalDBLinker.py`: script to generate custom lineage for any tables/columns created within an ExternalDatabase/ExternalSchema (often happens with Oracle (dblink) and SQLServer databases (references to databases in views)
  * see [externalDBLinker.md](externalDBLinker.md) for more
* `domainSummary.py` - queries the catalog to find all instances where data domains are used & counts the # of All, Accepted, Inferred, Rejected for all resources and per resource
  * output is an excel workbook (domain_summary.xlxs) with a worksheet for counts across all resources, and a worksheet per resource with individual counts per resource.  optional output to .csv files (per resource) is also possible
  * supports command-line parameters and environment vars for accessing the catalog.
  * uses edcSessionHelper.py to get a session reference to any rest queries
* `xdocAnalyzer.py` - use this script to download xdocs for a resource and analyze the contents (counts # of objects by type, # of attributes) and will analyze all links + connection assignments.  can be useful for troubleshooting (especially for resources that do not yet support reference objects)
  * supports command-line parameters and environment vars for accessing the catalog.
  * uses edcSessionHelper.py to get a session reference to any rest queries
* `setParentFilterValues.py` - use this script to update in bulk relational objects with a custom attribute containing the value of the schema the object belongs to. This will faceting by schema name in search results, as well as creating custom tab pointing to specific database schema within a resource, see [setParentFilterValues.md](setParentFilterValues.md) for more info
