# app.py
from flask import Flask, jsonify, request, send_from_directory
import numpy as np
from swarm import MosquitoSwarm

app = Flask(__name__, static_folder=".", static_url_path="")

# Global simulation state
bounds = np.array([[-50, -50, -50], [50, 50, 50]])
swarm = MosquitoSwarm(
    N=10000,
    bounds=bounds,
    sigma=0.5,
    attractor=np.zeros(3),
    attractor_strength=0.1,
    repulsion_radius=1.0,
    repulsion_strength=0.05,
)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/init", methods=["POST"])
def init_swarm():
    """Re-initialize the swarm with posted parameters."""
    data = request.json
    global swarm
    swarm = MosquitoSwarm(
        N=data["N"],
        bounds=bounds,
        sigma=data["sigma"],
        attractor=np.array(data.get("attractor", [0,0,0])),
        attractor_strength=data["attractor_strength"],
        repulsion_radius=data["repulsion_radius"],
        repulsion_strength=data["repulsion_strength"],
    )
    return ("", 204)

@app.route("/step")
def step_swarm():
    """Advance the simulation by dt and return flat position list."""
    dt = float(request.args.get("dt", 0.016))
    swarm.step(dt)
    # Return positions as a flat list
    return jsonify(swarm.state().tolist())

@app.route("/step_multi")
def step_multi():
    dt    = float(request.args.get("dt", 0.016))
    steps = int(request.args.get("steps", 1))
    for _ in range(steps):
        swarm.step(dt)
    return jsonify(swarm.state().tolist())


if __name__ == "__main__":
    app.run(port=8000)
