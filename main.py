import flask
import urllib3, json
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
CORS(app)



@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/graph')
def get_graph():
    http_client = urllib3.PoolManager()
    res = http_client.request('GET', 'https://jsonplaceholder.typicode.com/albums')
    data = json.loads(res.data.decode())
    graph = create_graph(data)
    # print(graph)
    return flask.jsonify(graph)

# {
#   "node":[
#           {"id":1, "group":1},
#
#       ],"links":[
#           "source":, "target":, "value":
#       ]
# }

def create_graph(json_data):
    last_user = 'A'
    graph = {
        "nodes":[],
        "links":[]
    }
    for item in json_data:
        if last_user == chr(64+item['userId']):
            graph['nodes'].append({"id":last_user, "group":item['userId']})
            graph['nodes'].append({"id":item['id'], "group":item['userId']})
            graph['links'].append({"source":last_user, "target":item['id']})

        else:
            graph['nodes'].append({"id":chr(64+item['userId']), "group":item['userId']})
            graph['nodes'].append({"id":item['id'], "group":item['userId']})
            graph['links'].append({"source":chr(64+item['userId']), "target":item['id']})
            graph['links'].append({"source":chr(64+item['userId']), "target":last_user})
            last_user = chr(64+item['userId'])

    return graph


if __name__ == "__main__":
    app.run(port=5001, debug=True)