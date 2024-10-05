import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
import matplotlib.pyplot as plt

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class TopicExtractor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        sentences = sent_tokenize(text)
        tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]
        return [[word for word in sentence if word.isalnum() and word not in self.stop_words]
                for sentence in tokenized_sentences]

    def compute_coherence_values(self, corpus, dictionary, texts, start=2, limit=10, step=1):
        coherence_values = []
        for num_topics in range(start, limit, step):
            model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, 
                             random_state=42, passes=15, alpha='auto', eta='auto')
            coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())
        return coherence_values

    def find_optimal_topics(self, text):
        preprocessed_text = self.preprocess_text(text)
        dictionary = Dictionary(preprocessed_text)
        corpus = [dictionary.doc2bow(text) for text in preprocessed_text]

        coherence_values = self.compute_coherence_values(corpus, dictionary, preprocessed_text)
        
        optimal_num_topics = coherence_values.index(max(coherence_values)) + 2  # +2 because we start from 2
        
        return optimal_num_topics, coherence_values

    def extract_topics(self, text, num_topics):
        preprocessed_text = self.preprocess_text(text)
        dictionary = Dictionary(preprocessed_text)
        corpus = [dictionary.doc2bow(text) for text in preprocessed_text]

        lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, 
                             random_state=42, passes=15, alpha='auto', eta='auto')
        
        topics = []
        for idx, topic in lda_model.print_topics(-1):
            topics.append([word.split('*')[1].strip().strip('"') for word in topic.split('+')])
        
        return topics

    def plot_coherence_values(self, coherence_values):
        x = range(2, len(coherence_values) + 2)
        plt.plot(x, coherence_values)
        plt.xlabel("Number of Topics")
        plt.ylabel("Coherence Score")
        plt.title("Topic Coherence Scores")
        plt.show()

if __name__ == "__main__":
    # Example text for demonstration
    example_text = """
    Machine learning is a method of data analysis that automates analytical model building. 
    It is a branch of artificial intelligence based on the idea that systems can learn from data, 
    identify patterns and make decisions with minimal human intervention.
    
    The process of machine learning is similar to that of data mining. Both look for patterns in data, 
    but machine learning uses those patterns to create predictive models. Machine learning algorithms 
    are often categorized as supervised or unsupervised.
    
    Supervised machine learning algorithms can apply what has been learned in the past to new data. 
    Unsupervised machine learning algorithms can draw inferences from datasets.
    
    Deep learning is a type of machine learning that runs inputs through biologically inspired neural 
    network architectures. The neural networks contain a number of hidden layers through which the data 
    is processed, allowing the machine to go "deep" in its learning, making connections and weighting 
    input for the best results.
    """

    # Create an instance of TopicExtractor
    extractor = TopicExtractor()

    # Find the optimal number of topics
    optimal_num_topics, coherence_values = extractor.find_optimal_topics(example_text)
    print(f"Optimal number of topics: {optimal_num_topics}")

    # Extract topics
    topics = extractor.extract_topics(example_text, optimal_num_topics)

    # Print topics
    print("\nExtracted Topics:")
    for i, topic in enumerate(topics, 1):
        print(f"Topic {i}: {', '.join(topic[:5])}")  # Print top 5 words for each topic

    # Plot coherence values
    extractor.plot_coherence_values(coherence_values)

    # Demonstration of how the number of topics affects the results
    print("\nDemonstration with different numbers of topics:")
    for num_topics in [2, 3, 5]:
        topics = extractor.extract_topics(example_text, num_topics)
        print(f"\nNumber of topics: {num_topics}")
        for i, topic in enumerate(topics, 1):
            print(f"Topic {i}: {', '.join(topic[:5])}")
