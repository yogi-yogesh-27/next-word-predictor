import numpy as np
import operator

class Model(object):
    def __init__(self,
                 vocabulary,
                 tokens,
                 ngrams):

        self.vocabulary = vocabulary
        self.tokens = tokens
        self.ngrams = ngrams
        self.probs = {}
        self.smoothed_probs = {}
        self.log_probs = {}

    def fit_model(self, smoothing_algo):
        """

        :param smoothing_algo:
        :return:
        """
        assert smoothing_algo in ['laplace_smoothing', 'k_n']

        self.probs = self.calculate_bayes_probs(self.ngrams, self.vocabulary)
        self.perform_smoothing(smoothing_algo)
        self.log_prob()

        print(self.vocabulary)
        print(len(self.vocabulary))
        print(self.ngrams)
        print(self.probs)
        print(self.smoothed_probs)
        print(self.log_probs)

    @staticmethod
    def calculate_bayes_probs(grams, voc):
        """
        P(w2 | w1) = count(w1, w2) / count(w1)
        :param ngrams:
        :param tokens:
        :return:
        """
        return dict(map(lambda p: (p, grams[p] / voc[p[0]]), grams))

    def perform_smoothing(self, smoothing_algo):
        """

        :return:
        """
        if smoothing_algo == "laplace_smoothing":

            print("Running Laplace smoothing process..")
            self.smoothed_probs = self.laplace_smoothing()

        elif smoothing_algo == "k_n":

            print("Running Kneser-Ney smoothing process..")
            self.smoothed_probs = self.kneser_ney_smoothing()
        else:
            print("Please choose a valid smoothing method.")

    def laplace_smoothing(self, add_k=1):
        """

        :param add_k: Int.
        :return:
        """
        pl = dict(
            map(lambda c: (c[0], (c[1] + add_k) / (len(self.tokens) + add_k * len(self.vocabulary))),
                self.probs.items()))
        return pl

    def kneser_ney_smoothing(self):
        """

        :return:
        """
        return self.probs

    def log_prob(self):
        """

        :return: a dictionary with n-grams and assigned log probabilities
        """
        log_prob = dict(map(lambda k: (k, - np.log(self.smoothed_probs[k])), self.smoothed_probs))
        self.log_probs = log_prob

    def mle(self, word):
        """

        :param word:
        :return:
        """
        next_words = {}
        for k in self.smoothed_probs.keys():
            if k[0] == word:
                next_words[k[1]] = self.smoothed_probs[k]

        sorted_ngams = sorted(next_words.items(), key=operator.itemgetter(1), reverse=True)

        return sorted_ngams


if __name__ == '__main__':
    tokens = ["<s>", "i", "want", "to", "eat", "chinese", "food", "lunch", "spend", "</s>",
              "<s>", "i", "want", "to", "eat", "chinese", "food", "lunch", "spend", "</s>",
              "<s>", "i", "want", "to", "eat", "chinese", "food", "lunch", "spend", "</s>",
              "<s>", "i", "want", "to", "eat", "</s>"]

    vocabulary_freq = {"i": 4,
                       "want": 4,
                       "to": 4,
                       "eat": 4,
                       "chinese": 3,
                       "food": 3,
                       "lunch": 3,
                       "spend": 3,
                       "<s>": 4,
                       "</s>": 4}

    ngrams = {('<s>', 'i'): 4,
              ('i', 'want'): 4,
              ('want', 'to'): 4,
              ('to', 'eat'): 4,
              ('eat', 'chinese'): 3,
              ('eat', '</s>'): 1,
              ('chinese', 'food'): 3,
              ('food', 'lunch'): 3,
              ('lunch', 'spend'): 3,
              ('spend', '</s>'): 3}

    modelObj = Model(vocabulary_freq,
                     tokens,
                     ngrams)

    modelObj.fit_model("laplace_smoothing")

    mle_dict = modelObj.mle("eat")
    print(mle_dict)
