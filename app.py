from flask import Flask, render_template, request, jsonify
import networkx as nx

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/route', methods=['POST'])
def get_optimal_route():
    data = request.json
    ambulance_location = (data['ambulance_location']['lat'], data['ambulance_location']['lon'])
    hospital_location = (data['hospital_location']['lat'], data['hospital_location']['lon'])
    traffic_data = data['traffic_data']

    G = nx.Graph()
    for route in traffic_data:
        start = (route['start']['lat'], route['start']['lon'])
        end = (route['end']['lat'], route['end']['lon'])
        G.add_edge(start, end, weight=route['congestion'])
    
    try:
        shortest_path = nx.shortest_path(G, source=ambulance_location, target=hospital_location, weight='weight')
        return jsonify({'optimal_route': shortest_path})
    except nx.NetworkXNoPath:
        return jsonify({'error': 'No available route'}), 400

if __name__ == '__main__':
    app.run(debug=True)
