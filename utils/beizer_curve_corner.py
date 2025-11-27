# GPT generated, just used this to make a corner of the fins curvy

# Round ONE corner of a freeform fin by inserting a short smooth arc.
# Units: centimeters (cm)
# poly: list of (x,y) in order around the fin (CW or CCW is fine)
# corner_idx: index (0..N-1) of the corner you want to round
# frac: how far from the corner to start/end the round as a fraction of adjacent edge lengths (0.1–0.3 is typical)
# n_arc: number of points to insert along the rounded corner (5–12 is typical)

def round_corner_bezier(poly, corner_idx, frac=0.2, n_arc=8):
    import math
    n = len(poly)
    i0 = (corner_idx - 1) % n
    i1 = corner_idx
    i2 = (corner_idx + 1) % n

    def dist(a,b): 
        return math.hypot(b[0]-a[0], b[1]-a[1])

    P0 = poly[i0]
    P1 = poly[i1]  # the corner to round
    P2 = poly[i2]

    # Offsets along each edge toward the corner (localizes the curve)
    L0 = dist(P0, P1); L1 = dist(P1, P2)
    t0 = max(1e-6, frac*L0); t1 = max(1e-6, frac*L1)

    # Points a short distance from the corner along each edge
    P0p = (P1[0] + (P0[0]-P1[0]) * (t0/L0),
           P1[1] + (P0[1]-P1[1]) * (t0/L0))
    P2p = (P1[0] + (P2[0]-P1[0]) * (t1/L1),
           P1[1] + (P2[1]-P1[1]) * (t1/L1))

    # Quadratic Bézier with control at the original corner
    def bezier(t):
        u = 1.0 - t
        x = u*u*P0p[0] + 2*u*t*P1[0] + t*t*P2p[0]
        y = u*u*P0p[1] + 2*u*t*P1[1] + t*t*P2p[1]
        return (x, y)

    arc_pts = [bezier(t) for t in [k/n_arc for k in range(n_arc+1)]]

    # Build new polygon: replace P1 with [P0p, arc(1..n-1), P2p]
    newpoly = []
    for k in range(n):
        if k == i1:
            # Insert rounded corner points
            newpoly.append(P0p)
            newpoly.extend(arc_pts[1:-1])  # interior points of the arc
            newpoly.append(P2p)
        else:
            newpoly.append(poly[k])
    return newpoly

# ---- Example (cm) ----
if __name__ == "__main__":
    fin_cm = [(0,0), (2.7,5.03), (7.9,5.03), (6.16,-1.61)]   # replace with your 4 points in cm
    corner_to_round = 1  # e.g., the (8,4) corner
    out = round_corner_bezier(fin_cm, corner_to_round, frac=0.2, n_arc=10)
    print("x,y")
    for x,y in out:
        print(f"{x:.3f},{y:.3f}")