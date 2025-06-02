import numpy as np
from swarm import MosquitoSwarm

if __name__ == "__main__":
    # Headless benchmark test
    swarm = MosquitoSwarm(
        N=10_000,
        bounds=np.array([[-50, -50, -50], [50, 50, 50]]),
        sigma=0.5,
        attractor=np.array([0, 0, 0]),
        attractor_strength=0.1,
        repulsion_radius=1.0,
        repulsion_strength=0.05,
    )
    import time
    dt = 0.016  # ~60 FPS
    start = time.perf_counter()
    for _ in range(600):  # 10 seconds
        swarm.step(dt)
    elapsed = time.perf_counter() - start
    print(f"600 frames in {elapsed:.2f}s → {600/elapsed:.1f} FPS")
