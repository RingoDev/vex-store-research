import requests
import csv


def search_github_repositories(query, sort="stars", order="desc", per_page=100):
    """
    Search for repositories on GitHub using the GitHub API with pagination.

    :param query: Search query (e.g., "machine learning")
    :param sort: Sort results by "stars", "forks", or "updated"
    :param order: Order results "asc" or "desc"
    :param per_page: Number of results per page (max 100)
    :return: List of all repositories matching the query
    """
    base_url = "https://api.github.com/search/repositories"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "Bearer <github pat>",
        # Replace with your GitHub token
    }
    all_repositories = []
    page = 1

    while True:
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page,
        }

        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            repositories = response.json()["items"]
            all_repositories.extend(repositories)

            # Break if less than the per_page limit is returned (indicating the last page)
            if len(repositories) < per_page or len(all_repositories) >= 1000:
                break
        else:
            raise Exception(f"GitHub API request failed: {response.status_code} - {response.json()}")

        page += 1  # Move to the next page

    return all_repositories


def run_multiple_queries(queries):
    """
    Run multiple queries and deduplicate the results.

    :param queries: List of search queries
    :return: List of unique repositories with the query they were found in
    """
    all_results = {}
    for i, query in enumerate(queries, start=1):
        try:
            print(f"Running query {i}: {query}")
            repositories = search_github_repositories(query)
            print(f"Query {i} found {len(repositories)} results")
            for repo in repositories:
                repo_key = repo["id"]  # Use repository ID as a unique identifier
                if repo_key not in all_results:
                    all_results[repo_key] = {
                        "name": repo["full_name"],
                        "stars": repo["stargazers_count"],
                        "description": repo["description"] or "No description provided",
                        "query_found_in": [i],  # Track which query found the repo
                    }
                else:
                    all_results[repo_key]["query_found_in"].append(i)
        except Exception as e:
            print(f"Error with query {i}: {e}")

    return sorted(all_results.values(), key=lambda x: x["stars"], reverse=True)


def save_results_to_csv(results, filename="repositories-2.csv"):
    """
    Save results to a CSV file.

    :param results: List of repository data
    :param filename: Name of the CSV file
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["query_found_in", "stars", "name", "description" ])
        writer.writeheader()
        for result in results:
            result["query_found_in"] = ",".join(map(str, result["query_found_in"]))  # Convert list to string
            writer.writerow(result)


# Example usage
if __name__ == "__main__":
    queries = [
        "topic:sbom stars:>100",
        "topic:vex stars:>100",
        "sbom in:readme topic:security-tools stars:>100",
    ]
    try:
        deduplicated_results = run_multiple_queries(queries)
        print(f"Found {len(deduplicated_results)} unique repositories.")
        save_results_to_csv(deduplicated_results)
        print("Results saved to 'repositories-2.csv'")
    except Exception as e:
        print(f"Error: {e}")
