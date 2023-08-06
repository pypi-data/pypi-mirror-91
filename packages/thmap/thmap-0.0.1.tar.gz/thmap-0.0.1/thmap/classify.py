import os
from abc import ABCMeta, abstractmethod
import warnings
from datetime import datetime

import pickle

import numpy as np

from sklearn.ensemble import RandomForestClassifier as skRandomForestClassifier
from sklearn.mixture import GaussianMixture
from sklearn.tree import tree, DecisionTreeClassifier
from sklearn.base import clone
import deepdish as dd


class Classifier:
    """
    An abstract representation of a classifier
    """
    __metaclass__ = ABCMeta

    def __init__(self, channel_order, theme_index, dtype=np.uint8):
        """
        generic initialization
        :param channel_order: a list of channel name strings indicating the order expected in data
        :param theme_index: a dictionary mapping theme names to their number in the thematic map
        :param dtype: what data type the output thematic map should be
        """
        self.channel_order = channel_order
        self.theme_index = theme_index
        self.is_trained = False
        self.dtype = dtype
        self.check_theme_index_limits()
        self.kind = ''

    # @classmethod
    # def open(cls, path):
    #     """
    #     Given a generic classifier pickle file without knowledge of the kind, determine what kind it is and open it
    #     :param path: where the pickle file is located
    #     :type path: str
    #     :return: a non-abstract classifier object type
    #     """
    #     # TODO: actually write this
    #     raise NotImplementedError("Implement this Marcus")

    @abstractmethod
    def train(self, feature_vectors):
        """
        Fit the classifier to some example data
        :param feature_vectors: a dictionary mapping theme names to numpy array with dimensions (m, k)
            of pixel feature vectors,
            the length k of each features vector should match the size of channel_order
        """
        for theme in self.theme_index:
            if theme not in feature_vectors:
                raise ValueError("{} expected but not found in training pixels".format(theme))
            if feature_vectors[theme].shape[1] != len(self.channel_order):
                raise ValueError("{} channels expected but found {} in training pixels".format(
                    len(self.channel_order), feature_vectors[theme].shape[1]))
        self.is_trained = True

    @abstractmethod
    def load(self, path):
        """
        load the classifier from a file
        :param path: path to load from
        :return: nothing, initializes object
        """
        if not os.path.isfile(path):
            msg = "Cannot load from {} because file does not exist"
            raise OSError(msg.format(path))

    @abstractmethod
    def save(self, path):
        """
        write the classifier out to a file
        :param path: path to save at
        """
        if not os.path.isdir(os.path.dirname(path)):
            msg = "Cannot save to {} because directory does not exist"
            raise OSError(msg.format(path))

    @abstractmethod
    def classify(self, image):
        """
        Classify an image using the classifier
        :param image: an input image numpy array of [naxis1, naxis2, n_channels] size
            where the last axis is ordered according to self.channel_order
        :return: a labeled map of [naxis1, naxis2] size with integers for each class according to self.theme_index
        :rtype: numpy.ndarray
        """
        if not self.is_trained:
            raise RuntimeError("Classifier has not yet been trained.")

    @staticmethod
    def check_channel_order_change(old, new):
        """
        Confirm that the new channel order is reasonable:
            if new channel order is None: throws error
            if order doesn't match: warns
        :param old: old channel order
        :param new: new channel order
        """
        if new is None:
            raise TypeError("The new channel order cannot be None.")
        elif old is None:
            msg = "Channel order has been set to {}"
            warnings.warn(msg.format(new), RuntimeWarning)
        elif old != new:
            msg = "Channel order has changed from {} to {}"
            warnings.warn(msg.format(old, new), RuntimeWarning)

    def check_theme_index_limits(self):
        """
        Insures theme index values fit within the requested data type, otherwise raises error
        """
        if self.theme_index is not None:
            for theme, index in self.theme_index.items():
                if index < np.iinfo(self.dtype).min or index > np.iinfo(self.dtype).max:
                    msg = "Theme {} has index {} which is outside the bounds for {} of ({}, {})"
                    raise ValueError(msg.format(theme, index, self.dtype,
                                                np.iinfo(self.dtype).min, np.iinfo(self.dtype).max))

    @staticmethod
    def check_theme_index_change(old, new):
        """
        Check that changes to theme index are reasonable:
            if new is none: raise error
            if any channels have been added or removed: warn
        :param old: old theme_index dictionary
        :param new: new theme_index dictionary
        """
        if new is None:
            raise TypeError("The new themes cannot be None.")
        elif old is None:
            msg = "Themes has been set to {}"
            warnings.warn(msg.format(new), RuntimeWarning)
        else:  # Both old and new are not None
            for old_theme, old_index in old.items():
                if old_theme not in new:
                    msg = "Theme {} has been removed from classifier with index {}"
                    warnings.warn(msg.format(old_theme, old_index), RuntimeWarning)
                elif old_index != new[old_theme]:
                    msg = "Theme {} has changed index from {} to {}"
                    warnings.warn(msg.format(old_theme, old_index, new[old_theme]))
            for new_theme, new_index in new.items():
                if new_theme not in old:
                    msg = "Theme {} has been added to classifier with index {}"
                    warnings.warn(msg.format(new_theme, new_index), RuntimeWarning)


class MixturesClassifier(Classifier):
    def __init__(self, channel_order, theme_index, num_components=5, weights=None):
        super(MixturesClassifier, self).__init__(channel_order, theme_index)
        self.kind = 'Mixtures'
        self.weights = weights

        # if the weights array is not designated, assume equal weighting
        if self.weights is None:
            self.weights = {theme: 1 for theme in theme_index}

        self.mixtures = dict()
        if isinstance(num_components, dict):
            for theme in num_components:
                if theme not in theme_index:
                    msg = "num_components has {} themes but {} is not in theme_index"
                    raise ValueError(msg.format(num_components.keys(), theme))
            for theme in theme_index:
                if theme not in num_components:
                    msg = "{} is not in num_components but specified in theme_index"
                    raise ValueError(msg.format(theme))
            self.num_components = num_components
        elif isinstance(num_components, int):
            self.num_components = {theme: num_components for theme in theme_index}
        else:
            msg = "num_components was type {} but should either be a dict with keys of themes or an integer"
            raise TypeError(msg.format(type(num_components)))

    def train(self, pixels):
        """
        Fit the classifier to some example data
        :param feature_vectors: a dictionary mapping theme names to numpy array with dimensions (m, k)
            of pixel feature vectors,
            the length k of each features vector should match the size of channel_order
        :return: returns nothing, just sets up classifier with trained values
        """

        super(MixturesClassifier, self).train(pixels)

        for label, data in pixels.items():
            self.mixtures[label] = GaussianMixture(n_components=self.num_components[label])
            self.mixtures[label].fit(data)

    def classify(self, image):
        """
        Classify an image using the classifier
        :param image: an input image numpy array of [naxis1, naxis2, n_channels] size
            where the last axis is ordered according to self.channel_order
        :return: a labeled map of [naxis1, naxis2] size with integers for each class according to self.theme_index
        :rtype: numpy.ndarray
        """

        super(MixturesClassifier, self).classify(image)

        # First, convert the image into a sequence of feature vectors, each entry being the multichannel pixel.
        pixels = image.reshape((image.shape[0] * image.shape[1], image.shape[2]))
        themes = sorted(list(self.theme_index.keys()))
        # Using the mixture model, find the log-likelihood for each theme,
        # and select the theme with the highest log-likelihood.
        scores = np.array([self.weights[theme] * self.mixtures[theme].score_samples(pixels) for theme in themes])
        relabel = np.vectorize(lambda i: self.theme_index[themes[i]])
        choice = relabel(np.argmax(scores, axis=0))

        labeled_map = choice.reshape((image.shape[0], image.shape[1])).astype(np.uint8)
        return labeled_map

    def load(self, path):
        """
        Load the classifier from a pickle file
        :param path: path to load from
        """
        super(MixturesClassifier, self).save(path)
        with open(path, "rb") as f:
            classifier_vars = pickle.load(f)
        self.check_channel_order_change(self.channel_order, classifier_vars['channel_order'])
        self.check_theme_index_change(self.theme_index, classifier_vars['theme_index'])
        for var, value in classifier_vars.items():
            setattr(self, var, value)
        self.check_theme_index_limits()

    def save(self, path):
        """
        Write the classifier out to a pickle file
        :param path: path to save at
        """
        super(MixturesClassifier, self).save(path)
        with open(path, "wb") as f:
            pickle.dump(vars(self), f, protocol=0)


class RiglerClassifier(Classifier):
    def __init__(self, channel_order, theme_index):
        super(RiglerClassifier, self).__init__(channel_order, theme_index)
        self.kind = 'Rigler'
        self.means, self.covariances = dict(), dict()
        self.determinants, self.rho, self.coefficients, self.inverses = dict(), len(channel_order), dict(), dict()

    def train(self, feature_vectors):
        """
        Fit the classifier to some example data
        :param feature_vectors: a dictionary mapping theme names to numpy array with dimensions (m, k)
            of pixel feature vectors,
            the length k of each features vector should match the size of channel_order
        :return: returns nothing, just sets up classifier with trained values
        """
        super(RiglerClassifier, self).train(feature_vectors)
        for label, data in feature_vectors.items():
            mean = np.mean(data, axis=0)
            covariance = np.cov(data, rowvar=False)
            self.means[label], self.covariances[label] = mean, covariance
        self.determinants = {theme: np.linalg.det(covariance) for theme, covariance in self.covariances.items()}
        self.rho = len(self.channel_order)
        self.coefficients = {theme: 1 / (np.sqrt((2 * np.pi) ** self.rho * self.determinants[theme]))
                             for theme in self.covariances}
        self.inverses = {theme: np.linalg.inv(matrix) for theme, matrix in self.covariances.items()}

    def classify(self, image):
        """
        Classify an image using the classifier
        :param image: an input image numpy array of [naxis1, naxis2, n_channels] size
            where the last axis is ordered according to self.channel_order
        :return: a labeled map of [naxis1, naxis2] size with integers for each class according to self.theme_index
        :rtype: numpy.ndarray
        """

        super(RiglerClassifier, self).classify(image)
        probabilities = {}

        for theme in self.means:

            mean = self.means[theme]
            coefficient = self.coefficients[theme]
            inverse = self.inverses[theme]
            probabilities[theme] = np.zeros((image.shape[0], image.shape[1]))

            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    pixel = image[i, j, :]
                    diff = pixel - mean
                    probability = coefficient * np.exp(-0.5 * diff.dot(inverse).dot(diff.transpose()))
                    probabilities[theme][i, j] = probability

        sorted_classes = sorted(self.theme_index, key=lambda theme: self.theme_index[theme])
        sorted_probabilities = np.zeros((image.shape[0], image.shape[1], len(sorted_classes)))

        for i_theme, theme in enumerate(sorted_classes):
            if theme in probabilities:
                sorted_probabilities[:, :, i_theme] = probabilities[theme]

        # If solar labels are not sequential or if they do not start at "0", then the indices must be correctly
        # mapped to the correct number label.
        unmapped_ind = np.argmax(sorted_probabilities, axis=2).astype(np.uint8)
        map_fn = np.vectorize(lambda ind: self.theme_index[sorted_classes[ind]])
        labeled_map = map_fn(unmapped_ind).astype(np.uint8)

        return labeled_map

    def load(self, path):
        """
        Load the classifier from a pickle file
        :param path: path to load from
        """
        super(RiglerClassifier, self).save(path)
        with open(path, "rb") as f:
            classifier_vars = pickle.load(f)
        self.check_channel_order_change(self.channel_order, classifier_vars['channel_order'])
        self.check_theme_index_change(self.theme_index, classifier_vars['theme_index'])
        for var, value in classifier_vars.items():
            setattr(self, var, value)
        self.check_theme_index_limits()

    def save(self, path):
        """
        Write the classifier out to a pickle file
        :param path: path to save at
        """
        super(RiglerClassifier, self).save(path)
        with open(path, "wb") as f:
            pickle.dump(vars(self), f, protocol=0)


class RandomForestClassifier(Classifier):
    """
    A pixel based classifier for thematic maps that uses a random forest as its underlying model
    """

    def __init__(self, channel_order, theme_index,
                 n_trees=20, max_depth=7, min_samples_leaf=100,
                 weights=None,
                 criterion='entropy', n_cores=3, bootstrap=False):
        """
        Initialize
        :param channel_order: a list of channel name strings indicating the order expected in data
        :param theme_index: a dictionary mapping theme names to their number in the thematic map
        :param n_trees: the number of trees in the classifier
        :param max_depth: the maximum depth of any tree in the classifier
        :param criterion: which metric is used for splitting: 'entropy' or 'gini' as defined in sklearn
        :param n_cores: the number of cpu cores to use in fitting
        :param bootstrap: whether bootstrapping should be used as defined in sklearn
        """
        super(RandomForestClassifier, self).__init__(channel_order, theme_index)
        self.kind = 'RandomForest'
        self.weights = weights
        if self.weights is not None:
            self.weights = {theme_index[theme]:weight for theme, weight in self.weights.items()}
        self.sk_object_ = skRandomForestClassifier(bootstrap=bootstrap, n_estimators=n_trees,
                                                   class_weight=self.weights,
                                                   min_samples_leaf=min_samples_leaf, criterion=criterion,
                                                   max_depth=max_depth, n_jobs=n_cores)

    def train(self, feature_vectors):
        """
        Fit the classifier to some example data
        :param feature_vectors: a dictionary mapping theme names to numpy array with dimensions (m, k)
            of pixel feature vectors,
            the length k of each features vector should match the size of channel_order
        :return: returns nothing, just sets up classifier with trained values
        """

        super(RandomForestClassifier, self).train(feature_vectors)
        x = np.concatenate([values for _, values in feature_vectors.items()])
        y = np.concatenate([np.repeat(self.theme_index[theme], values.shape[0]) for theme, values
                            in feature_vectors.items()])
        self.sk_object_.fit(x, y)

    def save(self, path):
        """
        Write the classifier out to h5 file file
        :param path: path to save at
        """
        super(RandomForestClassifier, self).save(path)

        def save_sk_forest(rf):
            excluded_terms = ['base_estimator', 'base_estimator_', 'estimators_']
            contents = {k: v for k, v in vars(rf).items() if k not in excluded_terms}
            contents['base_estimator'] = vars(getattr(rf, excluded_terms[0]))
            base_estimator_vars = list(contents['base_estimator'].keys())
            contents['extra_base_terms'] = {k: v for k, v in vars(rf.estimators_[0]).items()
                                            if k not in base_estimator_vars and k != 'tree_'}

            def get_tree_state(tree):
                state = tree.__getstate__()
                nodes_type = state['nodes'].dtype
                state['nodes'] = np.array(state['nodes'].tolist())
                return state, nodes_type

            contents['trees'] = [get_tree_state(estimator.tree_)[0] for estimator in rf.estimators_]
            contents['node_type'] = get_tree_state(rf.estimators_[0].tree_)[1]
            return contents

        contents = dict()
        contents['sk_object_'] = save_sk_forest(self.sk_object_)
        for k, v in vars(self).items():
            if k != 'sk_object_':
                contents[k] = v
        dd.io.save(path, contents)

    def load(self, path):
        """
        Load from an h5 format
        :param path:
        :return:
        """
        super(RandomForestClassifier, self).load(path)
        full_contents = dd.io.load(path)

        def load_sk_forest(contents):
            rf = skRandomForestClassifier()
            for k, v in contents.items():
                setattr(rf, k, v)
            rf.base_estimator_ = DecisionTreeClassifier()
            for k, v in contents['base_estimator'].items():
                setattr(rf.base_estimator_, k, v)
            rf.base_estimator = clone(rf.base_estimator_)
            rf.estimators_ = [clone(rf.base_estimator) for _ in range(len(contents['trees']))]

            for estimator, tree_values in zip(rf.estimators_, contents['trees']):
                for k, v in contents['extra_base_terms'].items():
                    setattr(estimator, k, v)
                tree_values['nodes'] = np.array([tuple(row) for row in tree_values['nodes']],
                                                dtype=contents['node_type'])
                estimator.tree_ = tree.Tree(contents['extra_base_terms']['n_features_'],
                                            np.zeros(1, dtype=np.intp) + contents['extra_base_terms']['n_classes_'],
                                            contents['extra_base_terms']['n_outputs_'])
                estimator.tree_.__setstate__(tree_values)
            return rf

        self.sk_object_ = load_sk_forest(full_contents['sk_object_'])
        for k, v in full_contents.items():
            if k != 'sk_object_':
                setattr(self, k, v)

    def load_old(self ,path):
        """
        Load the classifier from a pickle file, the old format of loading
        :param path: path to load from
        """
        if not os.path.isfile(path):
            msg = "Cannot load from {} because file does not exist"
            raise OSError(msg.format(path))

        with open(path, "rb") as f:
            classifier_vars = pickle.load(f)
        self.check_channel_order_change(self.channel_order, classifier_vars['channel_order'])
        self.check_theme_index_change(self.theme_index, classifier_vars['theme_index'])
        for var, value in classifier_vars.items():
            setattr(self, var, value)
        self.check_theme_index_limits()

    def classify(self, image):
        """
        Classify an image using the classifier
        :param image: an input image numpy array of [naxis1, naxis2, n_channels] size
            where the last axis is ordered according to self.channel_order
        :return: a labeled map of [naxis1, naxis2] size with integers for each class according to self.theme_index
        :rtype: numpy.ndarray
        """
        super(RandomForestClassifier, self).classify(image)

        feature_vectors = image.reshape((image.shape[0] * image.shape[1], image.shape[2]))
        labels = self.sk_object_.predict(feature_vectors)
        classified_image = labels.reshape((image.shape[0], image.shape[1]))

        return classified_image


class FFNeuralClassifier(Classifier):
    """
    a simple feed forward neural network classifier that looks at the pixel feature vector
    """
    def __init__(self, channel_order, theme_index, epochs=3, batch_size=10000):
        """
        Initialize
        :param channel_order: a list of channel name strings indicating the order expected in data
        :param theme_index: a dictionary mapping theme names to their number in the thematic map
        """
        super(FFNeuralClassifier, self).__init__(channel_order, theme_index)
        self.kind = 'FFNeural'
        self.epochs = epochs
        self.batch_size = batch_size
        self.keras_object_ = None

    def classify(self, image):
        """
        Classify an image using the classifier
        :param image: an input image numpy array of [naxis1, naxis2, n_channels] size
            where the last axis is ordered according to self.channel_order
        :return: a labeled map of [naxis1, naxis2] size with integers for each class according to self.theme_index
        :rtype: numpy.ndarray
        """
        super(FFNeuralClassifier, self).classify(image)
        expanded_image = image.reshape((image.shape[0] * image.shape[1], image.shape[2]))
        predictions = self.keras_object_.predict_classes(expanded_image)
        labeled_map = predictions.reshape((image.shape[0], image.shape[1]))
        return labeled_map

    def save(self, path):
        """
        Write the classifier out to a pickle file
        :param path: path to save at
        """
        super(FFNeuralClassifier, self).save(path)
        with open(path, "wb") as f:
            pickle.dump(vars(self), f, protocol=0)

    def load(self, path):
        """
        Load the classifier from a pickle file
        :param path: path to load from
        """
        super(FFNeuralClassifier, self).save(path)
        with open(path, "rb") as f:
            classifier_vars = pickle.load(f)
        self.check_channel_order_change(self.channel_order, classifier_vars['channel_order'])
        self.check_theme_index_change(self.theme_index, classifier_vars['theme_index'])
        for var, value in classifier_vars.items():
            setattr(self, var, value)
        self.check_theme_index_limits()

    def train(self, pixels):
        """
        Fit the classifier to some example data
        :param feature_vectors: a dictionary mapping theme names to numpy array with dimensions (m, k)
            of pixel feature vectors,
            the length k of each features vector should match the size of channel_order
        :return: returns nothing, just sets up classifier with trained values
        """
        import keras
        super(FFNeuralClassifier, self).train(pixels)
        self._setup()
        print("test")
        data = np.concatenate([np.array(pixels[key]) for key, num in
                               self.theme_index.items() if len(pixels[key]) != 0], axis=0)
        labels = np.concatenate([np.zeros(len(pixels[key])) + num for key, num in self.theme_index.items()], axis=0)
        one_hot_labels = keras.utils.np_utils.to_categorical(labels, num_classes=int(max(list(self.theme_index.values())))+1)
        self.keras_object_.fit(data, one_hot_labels, epochs=self.epochs, batch_size=self.batch_size)

    def _setup(self):
        """ setup the neural network architecture """
        from keras.models import Sequential
        from keras.layers import Dense

        input_dim = len(self.channel_order)
        output_dim = int(max(list(self.theme_index.values())))+1

        self.keras_object_ = Sequential()
        self.keras_object_.add(Dense(16, activation='relu', input_dim=input_dim))
        self.keras_object_.add(Dense(16, activation='relu'))
        self.keras_object_.add(Dense(8, activation='relu'))
        self.keras_object_.add(Dense(output_dim, activation='softmax'))
        self.keras_object_.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
