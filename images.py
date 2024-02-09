import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

# Ensure NLTK resources are downloaded
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def load_images_from_json(file_path='unsplash_images.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            images = json.load(file)
        return images
    except FileNotFoundError:
        st.error("File not found. Please make sure the unsplash_images.json file exists.")
        return []

def preprocess_text(text):
    """Preprocess the text for clustering."""
    stop_words = set(stopwords.words('english'))
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    # Tokenize and remove stopwords
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words and word.isalnum()]
    return ' '.join(filtered_tokens)

def cluster_images(images, n_clusters=5):
    """Cluster images based on their descriptions."""
    descriptions = [preprocess_text(image.get('description', '')) for image in images]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(descriptions)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X)
    return clusters

def display_clustered_images(images, clusters):
    """Display images grouped by their cluster."""
    clustered_images = sorted(zip(images, clusters), key=lambda ic: ic[1])
    for cluster_id in range(max(clusters) + 1):
        st.subheader(f"Cluster {cluster_id + 1}")
        for image, cluster in [ic for ic in clustered_images if ic[1] == cluster_id]:
            description = image.get("description", "No description available")
            st.image(image["image_url"], caption=description, width=300)
            st.text("Description: " + description)
            st.write("---")  # Adds a separator line

def main():
    st.title("Clustered Unsplash Images Product Viewer")

    images = load_images_from_json()
    if images:
        clusters = cluster_images(images)
        display_clustered_images(images, clusters)
    else:
        st.warning("No images to display. Check if the unsplash_images.json file is populated.")

if __name__ == "__main__":
    main()
