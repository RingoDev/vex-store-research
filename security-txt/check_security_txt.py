import csv
import requests
import time



# Function to check if security.txt exists
def check_security_txt(domain):
    if domain in ["Not Found", "", None]:
        return False
    url = f"https://{domain}/.well-known/security.txt"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False


# Example usage
if __name__ == "__main__":
    try:
        # Load domains from CSV
        with open("company_domains.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            company_domains = list(reader)
        # Check each domain
        results = []
        for company, domain in company_domains:
            security_txt_exists = check_security_txt(domain)
            results.append((company, domain, "Yes" if security_txt_exists else "No"))
            print(f"{company}: {domain}, security.txt: {'Found' if security_txt_exists else 'Not Found'}")
            time.sleep(2)  # Avoid rate limiting

        # Save results to CSV
        with open("security_txt_results.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Company", "Domain", "security.txt"])
            writer.writerows(results)

        print("\nResults saved to security_txt_results.csv")
    except Exception as e:
        print(f"Error: {e}")
