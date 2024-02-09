import requests
import json

def fetch_unsplash_images(access_key, page=1, per_page=10):
    """Fetch images from Unsplash.

    Args:
        access_key (str): Your Unsplash Access Key.
        page (int): Page number of the results.
        per_page (int): Number of items per page.

    Returns:
        list: A list of images with URLs and descriptions.
    """
    url = f"https://api.unsplash.com/photos?page={page}&per_page={per_page}"
    headers = {
        "Authorization": f"Client-ID {access_key}"
    }
    response = requests.get(url, headers=headers)
    images = []

    if response.status_code == 200:
        data = response.json()
        for item in data:
            images.append({
                "id": item["id"],
                "description": item["description"] or item["alt_description"],
                "image_url": item["urls"]["regular"]
            })

    return images

if __name__ == "__main__":
    access_key = "47cCAy88vq_Bjxv37pxN1doto3ux4SL8PmuCwdL3Eqo"  # Replace YOUR_ACCESS_KEY with your actual Unsplash Access Key
    images = fetch_unsplash_images(access_key)
    with open('unsplash_images.json', 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=4)

    print("Images fetched and saved to unsplash_images.json")
