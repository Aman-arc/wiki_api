from flask import request, jsonify
from collections import Counter

from project import app

search_history = []
import unittest
import requests



class WikiAPITestCase(unittest.TestCase):
    def test_word_frequency_analysis(self):
        response = requests.get('http://127.0.0.1:5000/word_frequency_analysis?topic=Python&n=5')
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('topic', data)
        self.assertIn('top_words', data)

    def test_search_history_endpoint(self):
        response = requests.get('http://127.0.0.1:5000/search_history')
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_word_frequency_analysis_invalid_input(self):
        response = requests.get('http://127.0.0.1:5000/word_frequency_analysis')
        self.assertEqual(response.status_code, 400)

    def test_word_frequency_analysis_nonexistent_topic(self):
        response = requests.get('http://127.0.0.1:5000/word_frequency_analysis?topic=NonexistentTopic&n=5')
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['topic'], 'NonexistentTopic')
        self.assertEqual(data['top_words'], [])

@app.route('/word_frequency_analysis', methods=['GET'])
def word_frequency_analysis():
    topic = request.args.get('topic')
    n = int(request.args.get('n', 10))  # Default to top 10 words if n is not provided

    # Fetch Wikipedia article
    wikipedia_url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&titles={topic}&prop=extracts&exintro=1'
    response = requests.get(wikipedia_url)
    data = response.json()

    # Extract text from Wikipedia response
    page = next(iter(data['query']['pages'].values()))
    text = page['extract'] if 'extract' in page else ''

    # Tokenize and count word frequency
    words = text.lower().split()
    word_counts = Counter(words)

    # Get the top n frequent words
    top_n_words = word_counts.most_common(n)

    # Add the search to the history
    search_history.append({'topic': topic, 'top_words': top_n_words})

    return jsonify({'topic': topic, 'top_words': top_n_words})

@app.route('/search_history', methods=['GET'])
def search_history_endpoint():
    print('hello')
    return jsonify(search_history)

