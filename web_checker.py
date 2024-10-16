import requests
from bs4 import BeautifulSoup
import socket

def get_website_info(url):
    info = {}

    # Get the IP address of the website
    try:
        info['IP Address'] = socket.gethostbyname(url.split("://")[-1])
    except Exception as e:
        info['IP Address'] = f"Error: {e}"

    # Check if the website is up
    try:
        response = requests.get(url)
        info['Status Code'] = response.status_code
    except requests.exceptions.RequestException as e:
        info['Status Code'] = f"Error: {e}"

    # Check for WordPress XML Sitemap
    sitemap_url = url + "/sitemap.xml"
    try:
        sitemap_response = requests.get(sitemap_url)
        if sitemap_response.status_code == 200:
            info['WordPress XML Sitemap'] = "Exists"
        else:
            info['WordPress XML Sitemap'] = "Does not exist"
    except requests.exceptions.RequestException:
        info['WordPress XML Sitemap'] = "Error checking sitemap"

    # Get server information
    info['Server'] = response.headers.get('Server', 'Unknown')

    # Get content type
    info['Content Type'] = response.headers.get('Content-Type', 'Unknown')

    return info

def display_info(info):
    print("\nWebsite Information:\n")
    for key, value in info.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    url = input("Enter the URL (including http:// or https://): ")
    website_info = get_website_info(url)
    display_info(website_info)
