import numpy as np

def read_input_file(file_path):
    """
    Reads edges from an input file where each line represents an edge
    in the format "source target".
    """
    with open(file_path, 'r') as file:
        edges = [tuple(map(int, line.strip().split())) for line in file]
    return edges

def compute_page_rank(edges, alpha=0.85, tolerance=1e-12, max_iterations=1000):
    """
    Computes the PageRank for the given edges with specified alpha and tolerance.
    """
    # Identify all unique pages
    pages = list(set([edge[0] for edge in edges] + [edge[1] for edge in edges]))
    n = len(pages)
    page_idx = {page: i for i, page in enumerate(pages)}
    
    # Initialize dictionary for H
    H = {page_idx[p]: {} for p in pages}
    for p, q in edges:
        H[page_idx[p]][page_idx[q]] = 1
    
    # Normalize H by each column (outbound links)
    for col in range(n):
        col_sum = sum(H[row].get(col, 0) for row in range(n))
        if col_sum > 0:
            for row in range(n):
                H[row][col] = H[row].get(col, 0) / col_sum
    print(H)
    # Adjust for dangling nodes
    dangling_nodes = [page_idx[p] for p in pages if all(col not in H[row] for row in range(n))]
    dangling_weights = np.ones(n) / n if dangling_nodes else np.zeros(n)
    for col in dangling_nodes:
        for row in range(n):
            H[row][col] = dangling_weights[row]
    
    # Compute the Google matrix G
    G = np.zeros((n, n))
    for row in range(n):
        for col, value in H[row].items():
            G[row, col] = alpha * value + (1 - alpha) / n

    # Initialize PageRank vector I
    I = np.ones(n) / n
    
    # Iteratively compute PageRank
    for _ in range(max_iterations):  # Limit iterations to ensure termination
        I_next = G.dot(I)
        # Check for convergence
        if np.linalg.norm(I_next - I, 1) < tolerance:
            break
        I = I_next

    # Output PageRank values
    return {page: I[page_idx[page]] for page in pages}

def main():
    input_file_path = 'sample_inputa1.txt'  # Update this to your file path
    edges = read_input_file(input_file_path)
    page_ranks = compute_page_rank(edges)

    # Print the PageRank values up to 5 decimal places
    for page, rank in sorted(page_ranks.items()):
        print(f"{page} = {rank:.12f}")

    # Verify the sum of PageRanks is approximately 1
    print(f"s = {sum(page_ranks.values()):.1f}")

if __name__ == "__main__":
    main()
