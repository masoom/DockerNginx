from flask import Flask, abort, request, make_response, jsonify


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'test1',
    },
    {
        'id': 2,
        'title': u'test2',
    }
]

@app.route('/')
def echo():
    return 'api-2'

@app.route('/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title']
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    return jsonify({'task': task[0]})

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
