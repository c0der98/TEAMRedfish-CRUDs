#!flask/bin/python


from flask import Flask, jsonify, request, abort, make_response
from flask_httpauth import HTTPBasicAuth
import requests

auth = HTTPBasicAuth()
app = Flask(__name__)

@auth.get_password
def get_password(username):
        if username == 'sti':
                return 'sti'
        return None
######################### error handler ##################
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': 'Unauthorized access'}), 401)
@app.errorhandler(400)
def bad_request(error):
        return make_response(jsonify({'error':'Bad request'}), 400)
        
@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'Error 4O4':'Not found'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
        return make_response(jsonify({'Error 405':'Method not allowed'}), 405)

@app.errorhandler(409)
def duplicatefound(error):
        return make_response(jsonify({'error':'DUplicate item found'}), 405)

##################### LOGIN, SESSIONS,ETC #########################
@app.route('/rackhd/login', methods=['POST'])
@auth.login_required
def rackhd_login():
	#if not request.json or not 'username' in request.json:
	#	abort(400)

	user =  request.json['username']
	pw = request.json['password']
	
	url = "https://localhost:8443/login"
	payload = '{"username" : "' + user + '", "password" : "' + pw +'"}'
	headers= {"Content-Type": "application/json"}
	r = requests.post(url, headers=headers, data=payload, verify=False)
	return r.text

@app.route('/redfish/login',methods=['POST'])
@auth.login_required
def redfish_login():
	user =  request.json['username']
        pw = request.json['password']

        url = "https://localhost:8443/redfish/v1/SessionService/Sessions"
        payload = '{"UserName" : "' + user + '", "Password" : "' + pw +'"}'
        headers= {"Content-Type": "application/json"}
        r = requests.post(url, headers=headers, data=payload, verify=False)
        return r.text

@app.route('/redfish/readsessions', methods=['GET'])
@auth.login_required
def redfish_session():
	url = "https://localhost:8443/redfish/v1/SessionService/Sessions/"
	headers = {"content-type":"application/json"}
	
	r = requests.get(url, headers=headers, auth=('admin','admin123'), verify=False)
	return r.text

@app.route('/redfish/deletesessions', methods=['DELETE'])
@auth.login_required
def redfish_delsession():
	sid = request.args.get('id')
	url = "https://localhost:8443/redfish/v1/SessionService/Sessions/%s" % sid
	r = requests.delete(url, auth=('admin','admin123'), verify=False)
	return r.text


#######################################################################
          HAROLD'S CRUD: NODES, TAGS, HOOKS
  #######################################################################
				#NODES
   #####################################################################


	
@app.route('/rackhd/nodes', methods=['GET'])
@auth.login_required
def readnode():
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes"
	headers = {"Content-Type":"application/json", "Authorization":"JWT "+token
	}
	r = requests.get(url, headers=headers, verify=False)

	return r.text

@app.route('/rackhd/nodes', methods=['POST'])
@auth.login_required
def createnode():

	name = request.json['name']
	typ = request.json['typ']
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes"

	payload = '{"name":"%s","type":"%s","autoDiscover":false}' % (name,typ)

	headers= {"Content-Type": "application/json", "Authorization": "JWT "+token}

	r = requests.post(url, headers=headers, data=payload, verify=False)
	return payload

##### *****NOTE: ONCE DELETED AN ERROR 400 WILL BE PRODUCED, BUT THE NODE IS ACTUALLY DELETED SUCCESSFULLY, ITS A BUG #############
@app.route('/rackhd/nodes', methods=['DELETE'])
@auth.login_required
def deletenode():
	ids = request.args.get('ids')
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/nodes/%s" % ids
	headers= {"Content-Type":"application/json",
"Authorization":"JWT "+token}

	r = requests.delete(url, headers=headers, verify=False)
	return r.text
	
@app.route('/rackhd/nodes',methods=['PATCH'])
@auth.login_required
def updatenode():
	token = request.headers.get('token')
	ids = request.args.get('ids')
	field = request.json['field']
	data = request.json['data']
	
	url = "https://localhost:8443/api/current/nodes/%s" % ids
	payload = '{"%s": "%s"}' %(field,data)
	headers= {"Content-Type":"application/json",
"Authorization":"JWT "+token}
	r = requests.patch(url, headers=headers, data=payload, verify=False)
	return r.text


	#############################     TAGS   ########################################  

@app.route('/rackhd/tags/create',methods=['POST'])
@auth.login_required
def createtag():
        token = request.headers.get('token')
        name = request.json['name']
        cpath = request.json['cpath']
        contains = request.json['contains']
	epath = request.json['epath']
	equals = request.json['equals']

        url = "https://localhost:8443/api/current/tags"
        payload = '{"name":"%s", "rules": [{"path":"%s", "contains":"%s"}, {"path":"%s", "equals":"%s"}]}'% (name,cpath,contains,epath,equals)

        headers= {"Content-Type":"application/json",
"Authorization":"JWT "+token}
        r = requests.post(url, headers=headers, data=payload, verify=False)
        return r.text

@app.route('/rackhd/tags/read', methods=['GET'])
@auth.login_required
def readtag():
	token = request.headers.get('token')
	url = "https://localhost:8443/api/current/tags/"
	headers= {"Content-Type":"application/json", "Authorization":"JWT "+token}	
	r = requests.get(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/tags/update', methods=['PATCH'])
#**add tags to NODE**
@auth.login_required
def updatetag():
	token = request.headers.get('token')
	node_id = request.args.get('id')
	tags = request.json['tags']
	url = "https://localhost:8443/api/current/nodes/%s/tags" % node_id
	
	headers= {"Content-Type":"application/json", "Authorization":"JWT "+token}
	payload = '{"tags":["%s"]}' % tags

	r = requests.patch(url, headers=headers, data=payload, verify=False)
	return r.text

@app.route('/rackhd/tags/delete', methods=['DELETE'])
@auth.login_required
def deletetag():
	token = request.headers.get('token')
	tag_name = request.args.get('name')
	url = "https://localhost:8443/api/current/tags/%s" % tag_name
	headers = {"content-type":"application/json", "Authorization":"JWT "+token}
	r = requests.delete(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/nodes/readtag', methods=['GET'])
@auth.login_required
def readnodetag():
	token = request.headers.get('token')
	node_id = request.args.get('nodeid')
	url = "https://localhost:8443/api/current/nodes/%s/tags" % node_id
	headers = {"content-type":"application/json", "Authorization":"JWT "+token}

	r = requests.get(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/nodes/deletetag', methods=['DELETE'])
@auth.login_required
def deletetagfromnode():
	token = request.headers.get('token')
	node_id = request.args.get('nodeid')
	tag_name = request.args.get('tagname')
	
	url = "https://localhost:8443/api/current/nodes/%s/tags/%s" % (node_id,tag_name)
	headers = {"content-type":"application/json", "Authorization":"JWT "+token}
	r = requests.delete(url, headers=headers, verify=False)
	return r.text

     #############################   HOOOK ###############################

@app.route('/rackhd/hook', methods=['POST'])
@auth.login_required
def createhook():
	token = request.headers.get('token')
	link = request.json['url']
	url = "https://localhost:8443/api/2.0/hooks"
	payload = '{"url":"%s"}' % link
	headers = {"content-type":"application/json","Authorization":"JWT " +token}
	
	r = requests.post(url, headers=headers, data=payload, verify=False)
	return r.text

@app.route('/rackhd/hook', methods=['GET'])
@auth.login_required
def readhook():
	token = request.headers.get('token')
	url = "https://localhost:8443/api/2.0/hooks"
	headers = {"content-type":"application/json", "Authorization":"JWT "+ token}
	r = requests.get(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/hook', methods=['PATCH'])
@auth.login_required
def updatehook():
	token = request.headers.get('token')
	hook_id = request.args.get('hook_id')
	field = request.json['field']
	data = request.json['data']
	#name = request.json['name']
	url = "https://localhost:8443/api/2.0/hooks/%s" % hook_id
	
	payload = '{"%s":"%s"}' % (field,data)
	headers = {"content-type":"application/json", "Authorization": "JWT "+token}
	
	r = requests.patch(url, headers=headers, data=payload, verify=False)
	return r.text

@app.route('/rackhd/hook', methods=['DELETE'])
@auth.login_required
def deletehook():
	token = request.headers.get('token')
	hook_id = request.args.get('hook_id')
	url = "https://localhost:8443/api/2.0/hooks/%s" % hook_id
	headers = {"content-type":"application/json", "Authorization":"JWT "+token}
	
	r = requests.delete(url, headers=headers, verify=False)
	return r.text
#########################################################################
            FUNG LOON'S OBMS AND RACKHD ROLES CRUD 
#########################################################################
@app.route('/rackhd/obms/create', methods=['PUT'])
@auth.login_required
def create_obms():
	url = "https://localhost:8443/api/current/obms"

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	nodeId = request.json['nodeId']
	service = request.json['service']
	user = request.json['user']
	password = request.json['password']
	host = request.json['host']

	payload = '{"nodeId": "' + nodeId + '", "service":"' + service + '", "config":{"user":"' + user + '", "password":"' + password + '", "host":"' + host + '"}}'

	response = requests.put(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/obms/read', methods=['GET'])
@auth.login_required
def read_obms():
	url = "https://localhost:8443/api/current/obms"

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.get(url, headers=headers, verify=False)

	return response.text

@app.route('/rackhd/obms/read/<string:nodeId>', methods=['GET'])
@auth.login_required
def read_obms_by_id(nodeId):
	base_url = "https://localhost:8443/api/current/obms"

	url = base_url + "/" + nodeId

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.get(url, headers=headers, verify=False)

	return response.text

@app.route('/rackhd/obms/update', methods=['PATCH'])
@auth.login_required
def update_obms():
	base_url = "https://localhost:8443/api/current/obms"

	nodeId = request.json['nodeId']

	url = base_url + "/" + nodeId

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	service = request.json['service']
	user = request.json['user']
	password = request.json['password']
	host = request.json['host']

	payload = '{"nodeId":"' + nodeId +'", "service":"' + service + '", "config":{"user":"' + user +'", "password":"' + password + '", "host":"' + host + '"}}'

	response = requests.patch(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/obms/delete', methods=['DELETE'])
@auth.login_required
def delete_obms():
	base_url = "https://localhost:8443/api/current/obms"

	nodeId = request.json['nodeId']

	url = base_url + "/" + nodeId

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

@app.route('/rackhd/role/create', methods=['POST'])
@auth.login_required
def create_role():
	url = "https://localhost:8443/api/current/roles"

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	privileges = request.json['privileges']

	privileges2 = list()

	for permission in privileges:
		privileges2.append(str(permission))

	privileges2 = str(privileges2)
	privileges2 = privileges2.replace("'",'"')

	role = request.json['role']

	payload = '{"privileges": ' + privileges2 + ', "role": "' + role + '"}'
	response = requests.post(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/role/read', methods=['GET'])
@auth.login_required
def read_role():

	url = "https://localhost:8443/api/current/roles"

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.get(url, headers=headers, verify=False)
	return response.text

@app.route('/rackhd/role/read/<string:role>', methods=['GET'])
@auth.login_required
def read_role_by_role(role):

	base_url = "https://localhost:8443/api/current/roles"

	url = base_url + "/" + role

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.get(url, headers=headers, verify=False)
	return response.text

@app.route('/rackhd/role/update', methods=['PATCH'])
@auth.login_required
def update_role():

	base_url = "https://localhost:8443/api/current/roles"

	role = request.json['role']

	url = base_url + "/" + role

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	privileges = request.json['privileges']

	privileges2 = list()

	for permission in privileges:
		privileges2.append(str(permission))

	privileges2 = str(privileges2)
	privileges2 = privileges2.replace("'",'"')

	payload = '{"privileges": ' + privileges2 + '}'
	response = requests.patch(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/role/delete', methods=['DELETE'])
@auth.login_required
def delete_role():

	base_url = "https://localhost:8443/api/current/roles"

	role = request.json['role']

	url = base_url + "/" + role

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text

@app.route('/rackhd/account/create', methods=['POST'])
@auth.login_required
def create_account():

	base_url = "https://localhost:8443/api/current/users?auth_token="

	token = request.headers.get['Token']

	url = base_url + token

	username = request.json['username']
	password = request.json['password']
	role = request.json['role']

	payload = '{"username":"' + username + '", "password":"' + password +'", "role":"' + role + '"}'

	headers = {
		"Content-Type": "application/json"
	}

	response = requests.post(url, headers=headers, data=payload, verify=False)
	return response.text
  
  
 ###############################################################################
                  Serena's CRUD: RACKHD ACCOUNTS
################################################################################

@app.route('/')
@auth.login_required
def index():
	return "Hello, %s!" % auth.username()

@app.route('/users/login', methods=['POST'])
def users_login():
	if not request.json or not 'username' in request.json:
        	abort(400)

	username = request.json['username']
        password = request.json['password']

        url = "https://localhost:8443/login"

        payload = '{"username" : "' + username + '", "password" : "' + password +'"}'

        headers = {
                "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response.text


@app.route('/users/create', methods=['POST'])
def create_users():

        username = request.json['username']
      	password = request.json['password']
	role = request.json['role']	
	url = "https://localhost:8443/api/2.0/users"

	payload = '{"username":"%s","password":"%s","role":"%s"}' % (username,password,role)

	headers = {
                "Content-Type": "application/json",
		"Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc5NDM2MTksImV4cCI6MTQ5ODAzMDAxOX0.NzjGL4hgvchyvQw3ORQ4AQiTlcmRKmnLz4oz-SBCLJI"
	}

        response = requests.post(url, headers=headers, data=payload, verify=False)
        return payload

@app.route('/users/read', methods=['GET'])
def get_users():
	
	url = "https://localhost:8443/api/2.0/users"	

	headers = {
                "Content-Type": "application/json",
		"Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc5NDM2MTksImV4cCI6MTQ5ODAzMDAxOX0.NzjGL4hgvchyvQw3ORQ4AQiTlcmRKmnLz4oz-SBCLJI"
	}
	
	response = requests.get(url, headers=headers, verify=False)
	return response.text

@app.route('/users/update', methods=['DELETE','POST'])
def update_users():

        username = request.json['username']
        url = "https://localhost:8443/api/2.0/users" + "/" + username

        headers = {
                "Content-Type": "application/json",
                "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc5NDM2MTksImV4cCI6MTQ5ODAzMDAxOX0.NzjGL4hgvchyvQw3ORQ4AQiTlcmRKmnLz4oz-SBCLJI"
        }

        responsedel = requests.delete(url, headers=headers, verify=False)
        
        username = request.json['username']
        password = request.json['password']
        role = request.json['role']
        url = "https://localhost:8443/api/2.0/users"

        payload = '{"username":"%s","password":"%s","role":"%s"}' % (username,password,role)

	response = requests.post(url, headers=headers, data=payload, verify=False)

	return response.text


@app.route('/users/delete', methods=['DELETE'])
def del_users():
  
	username = request.json['username']
	url = "https://localhost:8443/api/2.0/users" + "/" + username

        headers = {
                "Content-Type": "application/json",
                "Authorization": "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE0OTc5NDM2MTksImV4cCI6MTQ5ODAzMDAxOX0.NzjGL4hgvchyvQw3ORQ4AQiTlcmRKmnLz4oz-SBCLJI"
        }

        response = requests.delete(url, headers=headers, verify=False)
        return response.text
        
###############################################################################
              Fadhli's CRUD: MERTRIC POLLERS & SKUs
###############################################################################

@app.route('/rackhd/skus/read', methods=['GET'])
@auth.login_required
def read_skus():
	url = "https://localhost:8443/api/current/skus"

	token = "JWT " + request.headers.get('token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	r = requests.get(url, headers=headers, verify=False)
	return r.text

@app.route('/rackhd/skus/update', methods=['PATCH'])
@auth.login_required
def update_skus():
	base_url = "https://localhost:8443/api/current/skus"

	skuId = request.json['skuId']

	url = base_url + "/" + skuId

	token = "JWT " + request.headers.get('token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	field = request.json['field']
	data = request.json['data']
	
	payload = '{"%s":"%s"}' % (field,data)	
	
	r = requests.patch(url, headers=headers, data=payload, verify=False)

	return r.text

@app.route('/rackhd/skus/create', methods=['POST'])
@auth.login_required
def create_skus():
        url = "https://localhost:8443/api/current/skus"

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
        }

        name = request.json['name']
        path = request.json['path']
        path2 = request.json['path2']
	contains = request.json['contains']
	equals = request.json['equals']
        discoveryGraphName = request.json['discoveryGraphName']
        username = request.json['username']
	password = request.json['password']
        hostname = request.json['hostname']

        payload = '{"name":"' + name + '", "rules": [{"path":"' + path + '", "contains": "' + contains + '"},{"path":"' + path2 + '", "equals":"' + equals +'"}], "discoveryGraphName": "' + discoveryGraphName + '", "discoveryGraphOptions": {"username":"' + username + '", "password":"' + password + '", "hostname":"' + hostname + '"}}'

        r = requests.post(url, headers=headers, data=payload, verify=False)
        return r.text


@app.route('/rackhd/skus/delete', methods=['DELETE'])
@auth.login_required
def delete_skus():

        base_url = "https://localhost:8443/api/current/skus"

	skuId = request.json['skuId']

	url = base_url + "/" + skuId
	
        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
       	}

        r = requests.delete(url, headers=headers, verify=False)
        return r.text

@app.route('/rackhd/metricpollers/read', methods=['GET'])
@auth.login_required
def read_metricpollers():
        url = "https://localhost:8443/api/current/pollers"

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
        }

        r = requests.get(url, headers=headers, verify=False)
        return r.text

@app.route('/rackhd/metricpollers/create', methods=['POST'])
@auth.login_required
def create_metricpollers():
        url = "https://localhost:8443/api/current/pollers"

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
        }

        type = request.json['type']
	node = request.json['node']
	metric = request.json['metric']

	payload = '{"type":"' + type + '", "pollInterval":1000, "node":"' + node + '", "config": {"metric":"' + metric +'"}}'

        r = requests.post(url, headers=headers, data=payload, verify=False)
        return r.text

@app.route('/rackhd/metricpollers/update', methods=['PATCH'])
@auth.login_required
def update_metricpollers():
        base_url = "https://localhost:8443/api/current/pollers"

        pollerId = request.json['pollerId']

        url = base_url + "/" + pollerId

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
        }

        #field = request.json['field']
        #data = request.json['data']
	#str(data)
	paused = request.json['paused']
	pollInterval = request.json['pollInterval']
	type = request.json['type']

        #payload = '{"%s":"%s"}' % (field,data)
	payload = '{"type":"' + type + '","pollInterval":' + str(pollInterval) + ', "paused":' + str(paused) + '}'	

        r = requests.patch(url, headers=headers, data=payload, verify=False)

        return r.text

@app.route('/rackhd/metricpollers/delete', methods=['DELETE'])
@auth.login_required
def delete_metricpollers():

        base_url = "https://localhost:8443/api/current/pollers"

        pollerId = request.json['pollerId']

        url = base_url + "/" + pollerId

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
        }

        r = requests.delete(url, headers=headers, verify=False)
        return r.text
#########################################################################
                    HAKIM'S CRUD: IPMI POLLER & IBMS
#########################################################################

@app.route('/rackhd/ipmipollers/read', methods=['GET'])
@auth.login_required
def read_ipmipollers():
        url = "https://localhost:8443/api/current/pollers"

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
        }

        r = requests.get(url, headers=headers, verify=False)
        return r.text

@app.route('/rackhd/ipmipollers/create', methods=['POST'])
@auth.login_required
def create_ipmipollers():
        url = "https://localhost:8443/api/current/pollers"

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
        }

        type = request.json['type']
	node = request.json['node']
	command = request.json['command']

	payload = '{"type":"' + type + '", "pollInterval":10000, "node":"' + node + '", "config": {"command":"' + command + '"}}'

        r = requests.post(url, headers=headers, data=payload, verify=False)
        return r.text

@app.route('/rackhd/ipmipollers/update', methods=['PATCH'])
@auth.login_required
def update_ipmipollers():
        
	base_url = "https://localhost:8443/api/current/pollers"

        pid = request.json['pid']

        url = base_url + "/" + pid

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type": "application/json",
                "Authorization": token
        }

        paused = request.json['paused']
	pollInterval = request.json['pollInterval']

	payload = '{"paused":' + str(paused) + ', "pollInterval":' + str(pollInterval) + '}'

	r = requests.patch(url, headers=headers, data=payload, verify=False)

        return r.text

@app.route('/rackhd/ipmipollers/delete', methods=['DELETE'])
@auth.login_required
def delete_ipmipollers():

        base_url = "https://localhost:8443/api/current/pollers"

	pid = request.json['pid']

        url = base_url + "/" + pid

        token = "JWT " + request.headers.get('token')

        headers = {
                "Content-Type":"application/json",
                "Authorization": token
        }

        r = requests.delete(url, headers=headers, verify=False)
	return r.text


#IBMS

@app.route('/rackhd/ibms/create', methods=['PUT'])
@auth.login_required
def create_ibms():
	url = "https://localhost:8443/api/current/ibms"

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	nodeId = request.json['nodeId']
	service = request.json['service']
	community = request.json['community']
	host = request.json['host']

	payload = '{"nodeId": "' + nodeId + '", "service":"' + service + '", "config":{"community":"' + community + '", "host":"' + host + '"}}'

	response = requests.put(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/ibms/read', methods=['GET'])
@auth.login_required
def read_ibms():
	url = "https://localhost:8443/api/current/ibms"

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.get(url, headers=headers, verify=False)

	return response.text

@app.route('/rackhd/ibms/update', methods=['PATCH'])
@auth.login_required
def update_ibms():
	base_url = "https://localhost:8443/api/current/ibms"

	id = request.json['id']

	url = base_url + "/" + id

	token = "JWT " + request.headers.get('Token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	service = request.json['service']
	community = request.json['community']
	host = request.json['host']

	payload = '{"service":"' + service + '", "config":{"community":"' + community + '", "host":"' + host + '"}}'

	response = requests.patch(url, headers=headers, data=payload, verify=False)

	return response.text

@app.route('/rackhd/ibms/delete', methods=['DELETE'])
@auth.login_required
def delete_ibms():
	base_url = "https://localhost:8443/api/current/ibms"

	id = request.json['id']

	url = base_url + "/" + id

	token = "JWT " + request.headers.get('token')

	headers = {
		"Content-Type": "application/json",
		"Authorization": token
	}

	response = requests.delete(url, headers=headers, verify=False)

	return response.text


if __name__ == '__main__':
	app.run(debug=True)
 
 
