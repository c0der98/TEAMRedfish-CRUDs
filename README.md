WORKLOAD DISTRIBUTION
---------------------

- FADHLI: SKU && MetricPollers
- FUNG LOON: OBMS AND RACKHD ROLES
- HAKIM: IPMI POLLER & IBMS
- SERENA: RACKHD ACCOUNTS
- WEI YANG: NODES, TAGS, HOOKS

######################TEAM REDFISH README##############

######################FADHLI's#########################

Fadhli [SKU && MetricPollers]

============Rack-HD Token============================

GET-TOKEN:

curl http://localhost:5000/rackhd/login -d '{"username":"admin","password":"admin123"}' -H "Content-Type: application/json" -X POST | python -m json.tool

============SKUs=====================================

SKU-CREATE:

curl http://localhost:5000/rackhd/skus/create -d '{"name":"Intel 32GB RAM","path":"dmi.Base Board Information.Manufacturer","contains":"Intel","discoveryGraphName":"Graph.InstallCoreOS","path2":"ohai.dmi.memory.total","equals":"32946864kB","username":"testuser","password":"hello","hostname":"mycoreos"}' -H "Content-type: application/json" -X POST -H 'token:' | python -m json.tool

SKU-READ:

curl http://localhost:5000/rackhd/skus/read -X GET -H 'token:' | python -m json.tool

SKU-UPDATE:

curl http://localhost:5000/rackhd/skus/update -d '{"skuId":"","field":"password","data":"testpassword"}' -H "Content-type: application/json" -X PATCH -H 'token:' | python -m json.tool

SKU-DELETE:

curl http://localhost:5000/rackhd/skus/delete -d '{"skuId":""}' -H "Content-type: application/json" -X DELETE -H 'token:' | python -m json.tool

============METRIC POLLERS============================

METRICPOLLER-READ:

curl http://localhost:5000/rackhd/metricpollers/read -X GET -H 'token:' | python -m json.tool

METRICPOLLER-CREATE:

curl http://localhost:5000/rackhd/metricpollers/create -d '{"type":"snmp","node":"54daadd764f1a8f1088fdc42","metric":"snmp-interface-bandwidth-poller"}' -H "Content-type: application/json" -X POST -H 'token:' | python -m json.tool

METRICPOLLER-UPDATE:

curl http://localhost:5000/rackhd/metricpollers/update -d '{"pollerId":"", "paused":"true", "pollInterval":"1000", "type":"snmp"}' -H "Content-type: application/json" -X PATCH -H 'token:' -u admin:python | python -m json.tool

METRICPOLLER-DELETE:

curl http://localhost:5000/rackhd/metricpollers/delete -d '{"pollerId":""}' -H "Content-type: application/json" -X DELETE -H 'token:' | python -m json.tool

######################END################################

######################WEI YANG's#########################

#  HAROLD'S README FOR REDFISH FLASK

   CRUDs: NODES, TAGS, HOOKS
   HTTPAuth credentials: sti:sti
   Redfish admin credentials: admin:admin123

## GETTING STARTED
	Run the program using ./<filename>.py

###  NOTE: "content-type: application/json" must be included in header whenever sending json data. 
       Pipe output to python -m json.tool to view the data in a better format. (e.g. curl xxxxxx.com | python -m json.tool)

#### CRUDs
---------------------------------
	     LOGIN
---------------------------------
Description:
Login to obtain auth_token to carry out CRUD operation on rackhd/redfish

Operation: POST

Path: /rackhd/login

Parameters:
"username","password" -  username and password of an account to authenticate with, enter in json format.

Curl command example:
curl -X POST "http://localhost:5000/rackhd/login" -H  "content-type: application/json" -d '{ "username": "admin",  "password": "admin123"}' -u sti:sti


----------------------------------
	  CREATE NODES
----------------------------------
Description:
Create a new node

Operation: POST

Path: /rackhd/nodes

Parameters:
"token" - auth_token, enter in the header.
"name","typ" - name and type of the switch respectively, enter in json format.

Curl command:
curl -X POST "http://localhost:5000/rackhd/nodes" -H  "token: <Enter auth_token here>" -H  "content-type: application/json" -d '{ "name": "<Enter name here>",  "typ": "<Enter type here>"}'


----------------------------------
	    READ NODES
----------------------------------
Description:
Get a list of all the nodes

Operation: GET

Path: /rackhd/nodes

Parameters:
"token" - auth_token, enter in header

Curl command:
curl -X GET "http://localhost:5000/rackhd/nodes" -H  "token: <enter auth_token here>" -u sti:sti | python -m json.tool


----------------------------------
	    UPDATE NODES
----------------------------------
Description:
Update a data of a specific node

Operation: PATCH

Path: /rackhd/nodes

Parameters:
"token" - auth_token, enter in header
"ids" - ID of the node to update, URL Query String
"field" - Specific field to update(e.g. type/autoDiscover), enter as json data
"data" - New data to update the field with, enter as json data.

Curl command:
curl -X PATCH "http://localhost:5000/rackhd/nodes?ids=<Enter node ID here>" -H  "token: <enter auth_token here>" -H "content-type:application/json" -d '{"field":"<enter field to update>","data":"<enter data>"}' -u sti:sti


----------------------------------
	    DELETE NODES
----------------------------------
Description:
Delete a specific node

Operation: DELETE

Path: /rackhd/nodes

Parameters:
"token" - auth_token, enter in header
"ids" - ID of the node to delete, URL Query String

***NOTE***: WHEN CURL DELETE COMMAND IS RUN AN ERROR 400 WILL BE PRODUCED, BUT THE NODE IS ACTUALLY DELETED SUCCESSFULLY, ITS A BUG 

Curl command:
curl -X DELETE "http://localhost:5000/rackhd/nodes?ids=<Enter node ID>" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
	  CREATE TAGS
----------------------------------
Description:
Create a new tag

Operation: POST

Path: /rackhd/tags/create

Parameters:
"token" - auth_token, enter in the header.
"name" - name of the new tag, enter in json format.
"cpath" - Path into the catalog to validate against. For "contains", json data.
"contains" - A string that the value should contain, json data.
"epath" - Path into the catalog to validate against. For "equals", json data.
"equals" - Exact value to match against. Json data.

Curl command with sample data:
curl -X POST "http://localhost:5000/rackhd/tags/create" -u sti:sti -H  "token: <enter auth_token here>" -H  "content-type: application/json" -d '{  "name": "AMD 32GB RAM",  "cpath": "dmi.Base Board Information.Manufacturer",  "contains": "Intel",  "epath": "dmi.memory.total",  "equals": "329483092KB"}"'


----------------------------------
	  READ TAGS
----------------------------------
Description:
Get a list of tags

Operation: GET

Path: /rackhd/tags/read

Parameters:
"token" - auth_token, enter in the header.

Curl command:
curl -X GET "http://localhost:5000/rackhd/tags/read" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
	  UPDATE TAGS
----------------------------------
Description:
Add the TAG onto a node by patching the /tags path of a node

Operation: PATCH

Path: /rackhd/tags/update

Parameters:
"token" - auth_token, enter in the header.
"id" - ID of the node to update, URL Query string
"tags" - name of tags to add, json data

Curl command:
curl -X PATCH "http://localhost:5000/rackhd/tags/update?id=<Enter Node ID here>" -H  "token: <Enter auth_token here>" -H "content-type:application/json" -d '{"tags":"<Enter tags here>"}' -u sti:sti

----------------------------------
	  DELETE TAGS
----------------------------------
Description:
Delete a specific tag

Operation: DELETE

Path: /rackhd/tags/update

Parameters:
"token" - auth_token, enter in the header.
"name" - name of tags to delete, URL query string

Curl command:
curl -X DELETE "http://localhost:5000/rackhd/tags/delete?name=<Enter tag name here>" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
	READ TAGS OF A NODE
----------------------------------
Description:
Get a list of tags assigned to a specific node

Operation: GET

Path: /rackhd/nodes/readtag

Parameters:
"token" - auth_token, enter in the header.
"nodeid" - ID of the node to read, URL query string

Curl command:
curl -X GET "http://localhost:5000/rackhd/nodes/readtag?nodeid=<Enter node ID here>" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
     DELETE TAGS FROM A NODE
----------------------------------
Description:
Delete a specific tag from a specific node

Operation: DELETE

Path: /rackhd/nodes/deletetag

Parameters:
"token" - auth_token, enter in the header.
"nodeid" - ID of the node to delete the tag from, URL query string
"tagname" - name of tags to delete, URL query string

Curl command:
curl -X DELETE "http://localhost:5000/rackhd/nodes/deletetag?nodeid=<Enter Node ID here>&tagname=<Enter tag name here>" -H  "token: <Enter auth_token here>" -u sti:sti


----------------------------------
	 CREATE HOOKS
----------------------------------
Description:
Create a new hook

Operation: POST

Path: /rackhd/hook

Parameters:
"token" - auth_token, enter in the header.
"url" - url of the new hook, json data

Curl command:
curl -X POST "http://localhost:5000/rackhd/hook" -H  "token: <Enter auth_token here>" -H  "content-type: application/json" -d '{ "url": "<enter URL here>"}' -u sti:sti


----------------------------------
	 READ HOOKS
----------------------------------
Description:
Get the list of hooks

Operation: GET

Path: /rackhd/hook

Parameters:
"token" - auth_token, enter in the header.

Curl command:
curl -X GET "http://localhost:5000/rackhd/hook" -H  "token: <Enter token here>" -u sti:sti


----------------------------------
	UPDATE HOOKS
----------------------------------
Description:
Update data of hooks

Operation: PATCH

Path: /rackhd/hook

Parameters:
"token" - auth_token, enter in the header.
"hook_id" - ID of the hook to be updated, URL query string
"field" - Field to update, json data
"data" -  data to update, json data

Curl command:
curl -X PATCH "http://localhost:5000/rackhd/hook?hook_id=<Enter Hook ID here>" -H  "token: <Enter token here>" -H "content-type:application/json" -d '{"field":"<enter field to update>","data":"<enter data to update>"}' -u sti:sti


----------------------------------
	DELETE HOOKS
----------------------------------
Description:
Delete a specific hook

Operation: DELETE

Path: /rackhd/hook

Parameters:
"token" - auth_token, enter in the header.
"hook_id" - ID of the hook to be deleted, URL query string

Curl command:
curl -X DELETE "http://localhost:5000/rackhd/hook?hook_id=<Enter Hook ID here>" -H  "token: <Enter token here>" -u sti:sti

######################END################################

######################HAKIM'S############################

Hakim Razalee [IPMI Poller && IBMS]

============Rack-HD Token============================

GET-TOKEN:

curl -u admin:admin http://localhost:5000/rackhd/login -d '{"username":"admin","password":"admin123"}' -H "Content-Type: application/json" -X POST | python -m json.tool

=====================IPMI POLLER============================

IPMI CREATE:

curl -u admin:admin http://localhost:5000/rackhd/ipmipollers/create -d '{"type":"ipmi","node":"54daadd764f1a8f1088fdc42","command":"power"}' -H "Content-type: application/json" -X POST -H 'token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTgwMTY2NDAsImV4cCI6MTQ5ODEwMzA0MH0.CRCsEGp4Hb_mFYykWgmsN6CuaCtfBbzgOUv09C-_HLA ' | python -m json.tool

IPMI READ:

curl -u admin:admin http://localhost:5000/rackhd/ipmipollers/read -X GET -H 'token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTgwMTY2NDAsImV4cCI6MTQ5ODEwMzA0MH0.CRCsEGp4Hb_mFYykWgmsN6CuaCtfBbzgOUv09C-_HLA ' | python -m json.tool

IPMI UPDATE:

curl -u admin:admin http://localhost:5000/rackhd/ipmipollers/update -d '{"pid":"59495d5004a9f71405c06eec", "paused":"true","pollInterval":"10000"}' -H "Content-type: application/json" -X PATCH -H 'token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTgwMTY2NDAsImV4cCI6MTQ5ODEwMzA0MH0.CRCsEGp4Hb_mFYykWgmsN6CuaCtfBbzgOUv09C-_HLA ' | python -m json.tool

IPMI DELETE:

curl -u admin:admin http://localhost:5000/rackhd/ipmipollers/delete -d '{"pid":" "}' -X DELETE -H "Content-type: application/json" -H 'token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTgwMTY2NDAsImV4cCI6MTQ5ODEwMzA0MH0.CRCsEGp4Hb_mFYykWgmsN6CuaCtfBbzgOUv09C-_HLA '

============IBMS============================

IBMS CREATE:

curl -u admin:admin http://localhost:5000/rackhd/ibms/create -d '{"id":"591c569c087752c67428e4b3","nodeId":"590cbcbf29ba9e40471c9f3c","service":"snmp-ibm-service","community":"public","host":"172.31.128.2"}' -H "Content-type: application/json" -X PUT -H 'token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc5Nzg0MDQsImV4cCI6MTQ5ODA2NDgwNH0.TVxOtIbMwyQfkAaOnVPcoLCQopoM2tC3fcS7LbHJuGg' | python -m json.tool

IBMS READ:

curl -u admin:admin http://localhost:5000/rackhd/ibms/read -X GET -H 'token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc5Nzg0MDQsImV4cCI6MTQ5ODA2NDgwNH0.TVxOtIbMwyQfkAaOnVPcoLCQopoM2tC3fcS7LbHJuGg' | python -m json.tool

IBMS UPDATE:

curl -u admin:admin http://localhost:5000/rackhd/ibms/update -d '{"id":"5949f7f604a9f71405c06ef5","service":"snmp-ibm-service","community":"public","host":"172.31.128.198"}' -H "Content-type: application/json" -X PATCH -H 'token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc5Nzg0MDQsImV4cCI6MTQ5ODA2NDgwNH0.TVxOtIbMwyQfkAaOnVPcoLCQopoM2tC3fcS7LbHJuGg' | python -m json.tool

IBMS DELETE:

curl -u admin:admin http://localhost:5000/rackhd/ibms/delete -d '{"id":”5949f7f604a9f71405c06ef5"}' -X DELETE -H "Content-type: application/json" -H 'token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc5Nzg0MDQsImV4cCI6MTQ5ODA2NDgwNH0.TVxOtIbMwyQfkAaOnVPcoLCQopoM2tC3fcS7LbHJuGg'

######################END################################

######################SERENA'S###########################

RackHD Accounts appcrud.py Version 1.0 20/06/2017

USAGE NOTES
------------

- Change directory to the todo-api by typing cd todo-api

- Run the program in RackHD using ./appcrud.py

- Get a authentication token first.

- "content-type: application/json" must be included in header whenever sending json data.

- Pipe output to python -m json.tool to view the data in a better format.(e.g. curl -X GET | python -m json.tool)


LOGIN
------

- Login to obtain auth_token to carry out CRUD operation on RackHD.

- Administrator Credentials: 
admin:admin123

- Get a authentication token first by typing:

- CURL Command: 
curl http://localhost:5000/users/login -X POST -H "Content-Type:application/json" -d '{"username":"admin", "password":"admin123", "role": "Administrator" }'


=========================================================================================================================================

CREATE ACCOUNT
--------------

- CURL Command: 
curl http://localhost:5000/users/create -H "Content-Type: application/json" -X POST -d '{"username":"<username>", "password":"<password>", "role":"<role>"}'


READ ACCOUNT(S)
---------------

- CURL Command: 
curl http://localhost:5000/users/read | python -m json.tool


UPDATE ACCOUNT
--------------

- CURL Command:
curl http://localhost:5000/users/update -X DELETE -H "Content-Type:application/json" -d '{"username":"<username>", "password":"<password>", "role": "<role>" }'


DELETE ACCOUNT
--------------

- CURL Command:
curl -i http://localhost:5000/users/delete -X DELETE -H "Content-Type:application/json" -d '{"username":"<username>"}'

######################END################################

######################FUNG LOON'S###########################

STI Redfish

RESTful Redfish/RackHD API rewrite with Flask. Written in Python & Flask.

Prerequisites

Required tools: curl

Getting authentication token

Location: http://locahost:5000/rackhd/login

Method: POST

Flask credentials (username, password): admin, flask

Body (username, password): admin, admin123

Example command:

curl -X POST -H "Content-Type: application/json"  http://localhost:5000/rackhd/login -u admin:flask -d '{"username":"admin","password":"admin123"}'
OBMS Management

Create

Location: http://locahost:5000/rackhd/obms/create

Authorization Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE

Method: PUT

Flask credentials (username, password): admin, flask

Body (nodeId, service, username, password, host): node1, ipmi-obm-service, user1, password123, 192.171.5.1

Example command:

curl -X PUT -H "Content-Type: application/json"  http://localhost:5000/rackhd/obms/create -u admin:flask -d '{'{"nodeId":"node1", "service":"ipmi-obm-service", "username":"user1", "password":"password123", "host":"192.171.5.1"}'}' -H "Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE"
Read

Location: http://locahost:5000/rackhd/obms/read

Authorization Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE

Method: GET

Flask credentials (username, password): admin, flask

Example command:

curl -X GET -H "Content-Type: application/json"  http://localhost:5000/rackhd/obms/read -u admin:flask -H "Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE"
Update

Location: http://locahost:5000/rackhd/obms/update

Authorization Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE

Method: PATCH

Flask credentials (username, password): admin, flask

Body (nodeId, service, username, password, host): 59415a8bb77ff267c0a9c68d7, ipmi-obm-service, user2, password1234, 192.171.5.2

Example command:

curl -X PATCH -H "Content-Type: application/json"  http://localhost:5000/rackhd/obms/update -u admin:flask -d '{"nodeId":"59415a8bb77ff267c0a9c68d7", "service":"ipmi-obm-service", "username":"user2", "password":"password1234", "host":"192.171.5.2"}' -H "Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE"
Delete

Location: http://locahost:5000/rackhd/obms/create

Authorization Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE

Method: DELETE

Flask credentials (username, password): admin, flask

Body (nodeId): 59415a8bb77ff267c0a9c68d7

Example command:

curl -X DELETE -H "Content-Type: application/json"  http://localhost:5000/rackhd/obms/delete -u admin:flask -d '{"nodeId":"59415a8bb77ff267c0a9c68d7"}' -H "Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE"
Role Management

Create

Location: http://locahost:5000/rackhd/role/create

Authorization Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE

Method: POST

Flask credentials (username, password): admin, flask

Body (privileges, role): [Read, Write], ReadWrite

Example command:

curl -X POST -H "Content-Type: application/json"  http://localhost:5000/rackhd/role/delete -u admin:flask -d '{"privileges":["Read", "Write"], "role":"ReadWrite"}' -H "Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE"
Read

Location: http://locahost:5000/rackhd/role/read

Authorization Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE

Method: GET

Flask credentials (username, password): admin, flask

Example command:

curl -X GET -H "Content-Type: application/json"  http://localhost:5000/rackhd/role/read -u admin:flask -H "Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE"
Update

Location: http://locahost:5000/rackhd/role/update

Authorization Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE

Method: UPDATE

Flask credentials (username, password): admin, flask

Example command:

curl -X UPDATE -H "Content-Type: application/json"  http://localhost:5000/rackhd/role/update -u admin:flask -d '{"privileges":["Read"], "role":"ReadWrite"}' -H "Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE"
Delete

Location: http://locahost:5000/rackhd/role/delete

Authorization Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE

Method: DELETE

Flask credentials (username, password): admin, flask

Example command:

curl -X DELETE -H "Content-Type: application/json"  http://localhost:5000/rackhd/role/delete -u admin:flask -d '{"role":"ReadWrite"}' -H "Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0NTU2MTI5MzMsImV4cCI6MTQ1NTY5OTMzM30.glW-IvWYDBCfDZ6cS_6APoty22PE_Ir5L1mO-YqO3eE"

######################END################################
