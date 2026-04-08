import pandas as pd
import sys

def alpha_cut(tri, a):
    l, m, r = tri
    return l + (m-l)*a, r - (r-m)*a

def load_input_file(path):
    vdf = pd.read_excel(path, sheet_name="Vertices")
    edf = pd.read_excel(path, sheet_name="Edges")

    nodes = {}
    for row in vdf.itertuples(index=False):
        v = str(row.Vertex)
        p = str(row.Parameter)
    
        if v not in nodes:
            nodes[v] = {}
    
        nodes[v][p] = (row.l, row.m, row.r)

    edges = {}
    for row in edf.itertuples(index=False):
        u = str(row.Source)
        v = str(row.Target)
        p = str(row.Parameter)
    
        key = tuple(sorted((u, v)))
    
        if key not in edges:
            edges[key] = {}
    
        edges[key][p] = (row.l, row.m, row.r)

    params = sorted(vdf["Parameter"].astype(str).unique())

    return nodes, edges, params

def compute_critical_alpha(l, m):
    denom = 1 - (m - l)
    if denom <= 0:
        return 1
    return l / denom

def generate_optimal_alphas(nodes, edges):
    alphas = set()

    for v in nodes.values():
        for (l, m, r) in v.values():
            a = compute_critical_alpha(l, m)
            if 0 < a <= 1:
                alphas.add(round(a, 3))

    for e in edges.values():
        for (l, m, r) in e.values():
            a = compute_critical_alpha(l, m)
            if 0 < a <= 1:
                alphas.add(round(a, 3))

    return sorted(alphas)

def analyze(nodes, edges, params, alphas):

    results = []

    for p in params:
        nodes_p = {v: nodes[v][p] for v in nodes if p in nodes[v]}
        edges_p = {(u, v): edges[(u, v)][p] for (u, v) in edges if p in edges[(u, v)]}

        for a in alphas:
            included_v = []
            borderline_v = []

            for v, tri in nodes_p.items():
                lo, hi = alpha_cut(tri, a)

                if lo >= a:
                    included_v.append(v)
                elif lo < a <= hi:
                    borderline_v.append(v)

            included_e = []

            included_v_set = set(included_v)

            for (u, v), tri in edges_p.items():
                lo, hi = alpha_cut(tri, a)

                if lo >= a and u in included_v_set and v in included_v_set:
                    included_e.append((u, v))
                    
            included_v.sort()
            borderline_v.sort()
            included_e.sort()

            results.append({
                "Parameter": p,
                "Alpha": a,
                "Vertices": ", ".join(included_v) if included_v else "None",
                "Edges": ", ".join(f"({u},{v})" for u, v in included_e) if included_e else "None",
                "Borderline Vertices": ", ".join(borderline_v) if borderline_v else "None"
            })

    return pd.DataFrame(results)

if __name__ == "__main__":
    
    EXCEL_FILE = input("\nEnter Excel file path: ").strip()

    if not EXCEL_FILE:
        print("\nNo file selected.")
        sys.exit()

    while True:
        try:
            n = int(input("\nEnter number of alpha-cut values (0 for auto-generation): "))
            if n < 0:
                print("Error! Enter a non-negative integer.")
                continue
            break
        except:
            print("Invalid input. Try again!")
    
    if n == 0:
        ALPHAS = None
    else:
        ALPHAS = []
        for i in range(n):
            while True:
                try:
                    val = float(input(f"Enter alpha {i+1}: "))

                    if not (0 < val <= 1):
                        print("Error! Alpha must be in the range (0, 1]. Try again!")
                        continue

                    ALPHAS.append(val)
                    break

                except:
                    print("Invalid input. Try again!")

    nodes, edges, params = load_input_file(EXCEL_FILE)

    if ALPHAS is None:
        ALPHAS = generate_optimal_alphas(nodes, edges)

    ALPHAS = [a for a in sorted(ALPHAS)]

    print("\nParameters:", params)
    print("Alpha cuts (in ascending order):", ALPHAS)

    df = analyze(nodes, edges, params, ALPHAS)

    print("")
    print(df.to_string(index=False))

    df.to_excel("sfnvfg_results.xlsx", index=False)