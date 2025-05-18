Forked from: **[EmbeddingSearch](https://github.com/nadzmi27/EmbeddingSearch)** by **[Nadzmi](https://github.com/nadzmi27)**
# Background
This project is my attempt at leveraging the power of **sentence embedding** (e.g. BERT). I decided to use sentence embedding to design a search engine. The project is divided into two main components:
1. Using **textual information** provided in the **[MyAnimeList](https://myanimelist.net/)** such as **synopsis, genre, demographic, and etc.** and transforming them into **vector representation** and storing them into **[vector database](https://www.pinecone.io/learn/vector-database/)** (since the size of the data will be small, we will store them as Numpy file). 
2. Take in **query** by the user and convert them into **vector representation** and match them to **top k** anime in the **vector database** using **Bi-Encoder** (explanation below) then we will narrow down the matches using **Cross-Encoder**. The ranking of the matches is decided with the combination of **score, popularity and favourites** using **[geometric mean](https://en.wikipedia.org/wiki/Geometric_mean)**.

# Architecture

- **Bi-Encoder:** `all-distilroberta-v1`
- **Cross-Encoder:** `ms-marco-MiniLM-L-6-v2`
- **Summarizer:** Few texts are shortened in the preprocessing step (c) `Falconsai/text_summarization` to ensure the input is under the context-length limit of the Bi-Encoder and the Cross-Encoder.
- **Vector Database:** `Numpy`


# Use Cases
What I've explored is **not limited to textual data**, we can also use them for **images, audio, and even the combination of different data types** here are a few ways we can use the same concept:
1. **Multimedia (text, audio, image) Retrieval:** Match query (text) to text, audio, image. Or even match image/audio to text, audio, image. You get the point.
2. **Question Answering:** Provide accurate answers to user queries based on document content.
3. **Recommendation Systems:** Suggest items based on user preferences and similar items.
4. **Content Personalization:** Tailor content recommendations based on user interests and behaviour.
5. **Duplicate Detection:** Find similar or duplicate documents within a dataset.
6. **Anything that involves matching**: Literally anything or at least the majority of tasks that involve the matching process can be done using encoding and vector database.

### TODO:
Streamlit:
- [x] Format displayed df 
- [ ] Change theme
- [ ] Provide a better description
- [x] Improve the UI

