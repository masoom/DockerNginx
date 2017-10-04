import requests

def test_get():
	r = requests.get('http://localhost/')
	assert r.status_code==200

def test_get_task():
	r = requests.get('http://localhost/api/v1.0/tasks')
	assert r.status_code==200
	
def test_task_id__get():
	r = requests.get('http://localhost/api/v1.0/tasks/1')
	assert r.status_code==200

def test_task_id():
	test_task = {u'title':u'test3'}
	r = requests.post('http://localhost/api/v1.0/tasks', json=test_task)
	assert r.status_code==201

def test_task_id_put():
	test_task = {u'title':u'test2'}
	r = requests.put('http://localhost/api/v1.0/tasks/2', json=test_task)
	assert r.status_code==200

def test_task_id_delete():
	r = requests.delete('http://localhost/api/v1.0/tasks/2')
	assert r.status_code==200
