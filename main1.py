def read_input():
    edges = []
    while True:
        try:
            line = input().strip()
            if not line:
                break
            num1, num2 = map(int, line.split())
            edges.append((num1, num2))
        except EOFError:
            break
    return edges

def compute_page_rank(links, alpha=0.85, tolerance=1e-6, max_iterations=1000):
    pages = set()
    for link in links:
        pages.add(link[0])
        pages.add(link[1])
    num_pages = len(pages)
    initial_pr = 1 / num_pages
    page_rank = {page: initial_pr for page in pages}

    for _ in range(max_iterations):
        new_page_rank = {}
        delta = 0
        for page in pages:
            new_rank = (1 - alpha) / num_pages
            for link in links:
                if link[1] == page:
                    new_rank += alpha * page_rank[link[0]] / len([x for x in links if x[0] == link[0]])
            new_page_rank[page] = new_rank
            delta += abs(new_rank - page_rank[page])
        page_rank = new_page_rank
        if delta < tolerance:
            break
    sum_pr = sum(page_rank.values())
    page_rank_normalized = {page: rank / sum_pr for page, rank in page_rank.items()}
    return page_rank_normalized

def print_page_rank_output(page_rank):
    for page, rank in sorted(page_rank.items()):
        print(f"{page} = {rank:.12f}")
    print("s = 1.0")

# Corrected: Use read_input() instead of read_input_file
input_links = read_input()

# Compute PageRank vector
page_rank = compute_page_rank(input_links)

# Print the PageRank output
print_page_rank_output(page_rank)
