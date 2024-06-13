import numpy as np

def read_input():
    edges = []
    while True:
        try:

            line = input().strip()
            
            # Break the loop if no more lines are left
            if not line:
                break
            
            # Split the line into two integers
            num1, num2 = map(int, line.split())
            edges.append([num1, num2])
        except EOFError:
            # Break the loop if EOF (end of file) is reached
            break

    # inp = [int(x) for x in input().split()]

    # n = len(inp)
    # for i in range(0, n, 2):
    #     edges.append([inp[i], inp[i+1]])
    return edges

def compute_page_rank(edges, alpha=0.85, tolerance=1e-9):
    """
    Computes the PageRank for the given edges with specified alpha and tolerance
    using sparse matrix representation.
    """
    # Identify all unique pages
    pages = list(set([edge[0] for edge in edges] + [edge[1] for edge in edges]))
    n = len(pages)
    page_idx = {page: i for i, page in enumerate(pages)}

    # Initialize hyperlink matrix H as a sparse matrix
    H_sparse = {}
    outbound_links = np.zeros(n)
    for p, q in edges:
        i, j = page_idx[q], page_idx[p]
        H_sparse[(i, j)] = H_sparse.get((i, j), 0) + 1
        outbound_links[j] += 1

    # Normalize H_sparse
    for key, value in H_sparse.items():
        i, j = key
        H_sparse[key] = value / outbound_links[j]
        
    # Identify dangling nodes
    dangling_nodes = np.where(outbound_links == 0)[0]

    # Compute the Google matrix G using sparse matrix operations
    I = np.ones(n) / n
    for iteration in range(10000):
        I_next = np.zeros(n)
        for (i, j), hij in H_sparse.items():
            I_next[i] += alpha * hij * I[j]
        # Adjust for dangling nodes
        I_next += (1 - alpha) / n
        I_next += alpha * sum(I[dangling_nodes]) / n
        # Check for convergence
        if np.linalg.norm(I_next - I, 1) < tolerance:
            break
        I = I_next

    return {page: I[page_idx[page]] for page in pages}


def main():
    edges = read_input()
    page_ranks = compute_page_rank(edges)

    # Print the PageRank values in the desired format
    for page, rank in sorted(page_ranks.items()):
        print(f"{page} = {rank:.12f}")

    # Verify the sum of PageRanks is approximately 1
    print(f"s = {sum(page_ranks.values()):.1f}")

if __name__ == "__main__":
    main()
