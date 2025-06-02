import numpy as np

class MosquitoSwarm:
    def __init__(
        self,
        N: int,
        bounds: np.ndarray,
        sigma: float = 1.0,
        attractor: np.ndarray = None,
        attractor_strength: float = 0.0,
        repulsion_radius: float = 1.0,
        repulsion_strength: float = 0.1,
    ):
        """
        N: number of mosquitoes
        bounds: array [[xmin,ymin,zmin],[xmax,ymax,zmax]]
        sigma: std dev of random-walk noise per step
        attractor: 3-vector for external cue (e.g. swarm center)
        attractor_strength: how strongly mosquitoes bias toward attractor
        repulsion_radius: distance under which mosquitoes repel each other
        repulsion_strength: magnitude of repulsive kick
        """
        self.N = N
        self.bounds = bounds
        self.sigma = sigma
        self.attractor = attractor
        self.astr = attractor_strength
        self.rrad = repulsion_radius
        self.rstr = repulsion_strength

        # State arrays
        self.pos = np.random.uniform(bounds[0], bounds[1], size=(N, 3))
        self.vel = np.zeros((N, 3), dtype=float)

    def step(self, dt: float):
        # 1) Random-walk noise
        noise = np.random.normal(0, self.sigma, size=(self.N, 3))
        self.vel += noise

        # 2) Attractor pull
        if self.attractor is not None and self.astr > 0:
            dir_to_attr = (self.attractor - self.pos)
            dist_attr = np.linalg.norm(dir_to_attr, axis=1, keepdims=True) + 1e-6
            self.vel += self.astr * (dir_to_attr / dist_attr)

        # 3) Pairwise repulsion (vectorized approximate)
        k = min(20, self.N - 1)
        idx = np.random.randint(0, self.N, size=(self.N, k))
        peers = self.pos[idx]                     # (N, k, 3)
        disp = self.pos[:, None, :] - peers       # (N, k, 3)
        dist = np.linalg.norm(disp, axis=2)       # (N, k)

        mask = dist < self.rrad                   # (N, k)

        # compute repulsive kicks (N, k, 3)
        kicks = (disp / (dist[..., None] + 1e-6)) * (self.rstr / (dist[..., None] + 1e-6))

        # zero out kicks beyond the repulsion radius
        kicks = np.where(mask[..., None], kicks, 0.0)

        # sum kicks and apply
        self.vel += kicks.sum(axis=1)

        # 4) Update positions
        self.pos += self.vel * dt

        # 5) Keep inside bounds (wrap-around)
        low, high = self.bounds
        span = high - low
        self.pos = (self.pos - low) % span + low

    def state(self):
        """Return current positions as a flat Float32 array for rendering."""
        return self.pos.astype(np.float32).ravel()