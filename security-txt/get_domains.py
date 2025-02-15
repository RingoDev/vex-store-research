import csv
import re
import time
from googlesearch import search

# Function to get domain name from Google search
def get_domain(company):
    query = f"{company} official site"
    try:
        for url in search(query):
            match = re.search(r"https?://([^/]+)", url)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error searching for {company}: {e}")
    return "Not Found"

# Example usage
if __name__ == "__main__":
    try:
# List of companies to find domains for
        companies = [
            "CIRCL", "Cryptsoft Pty Ltd.", "Carnegie Mellon University", "EclecticIQ",
            "Electric Power Research Institute (EPRI)", "Siemens AG", "Oracle", "Microsoft",
            "NIST", "TIBCO Software Inc.", "sFractal Consulting LLC", "Arista Networks",
            "Hitachi, Ltd.", "McAfee", "Red Hat", "Cisco Systems", "Mitre Corporation",
            "AT&T", "Accenture", "Federal Office for Information Security (BSI) Germany",
            "Huawei Technologies Co., Ltd.", "Dell"
        ]
        # Process each company and save results
        results = []
        for company in companies:
            domain = get_domain(company)
            results.append((company, domain))
            print(f"{company} -> {domain}")
            time.sleep(2)  # Avoid rate limiting

        # Save to CSV file
        with open("company_domains.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Company", "Domain"])
            writer.writerows(results)

        print("\nDomains saved to company_domains.csv")
    except Exception as e:
        print(f"Error: {e}")
