import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve

def extract_and_save_images(url, output_folder, entire_website=False):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define user-agent header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send a GET request to the URL with the defined headers
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all image tags
        img_tags = soup.find_all('img')

        for img_tag in img_tags:
            # Extract the source URL of the image
            img_url = img_tag.get('src')

            # If the image URL is relative, convert it to absolute URL
            if img_url and not img_url.startswith('http'):
                img_url = urljoin(url, img_url)

            # Get the filename from the URL
            filename = os.path.basename(urlparse(img_url).path)

            # Download the image and save it to the output folder
            if img_url:
                img_path = os.path.join(output_folder, filename)
                urlretrieve(img_url, img_path)
                print(f"Image '{filename}' saved successfully.")

        if entire_website:
            # Find all anchor tags
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href and href.startswith('http'):
                    extract_and_save_images(href, output_folder)

    else:
        print(f"Failed to retrieve content from {url}")

def main():
    url = input("Enter the URL from which you want to extract images: ")
    output_folder = "output_images"
    entire_website = input("Do you want to scrape the entire website? (yes/no): ").lower() == 'yes'
    extract_and_save_images(url, output_folder, entire_website)

if __name__ == "__main__":
    main()
