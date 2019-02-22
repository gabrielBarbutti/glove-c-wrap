import cooccur
import glove as glv
import shuffle
import vocab_count
import numpy as np

class glove:
    def __init__(self, verbose=0, memory=4.0, threads=8.0, stderr_to_file=True):
        self.verbose = verbose
        self.memory = memory
        self.threads = threads

    def cooccur(self, symmetric=True, window_size=15, vocab_file='vocab.txt',
                max_product=0, overflow_length=0, overflow_file='overflow',
                distance_weighting=True, corpus_file='corpus.txt',
                cooccurrence_file='cooccurrence.bin'):
        # Adjust boolean variables for C
        if symmetric: symmetric = 1
        else: symetric = 0
        if distance_weighting: distance_weighting = 1
        else: symetric = 0
        # Define argumments
        args = [
            'cooccur',
            corpus_file, cooccurrence_file,
            '-verbose', str(self.verbose),
            '-symmetric', str(symmetric),
            '-window-size', str(window_size),
            '-vocab-file', vocab_file,
            '-memory', str(self.memory),
            '-overflow-file', overflow_file,
            '-distance-weighting', str(distance_weighting)
        ]
        # Call C code
        cooccur.cooccur_wrap(args)

    def glove(self, write_header=False, vector_size=50, itera=25, eta=0.05,
            alpha=0.75, x_max=100.0, binary=0, model=2,
            input_file='cooccurrence.shuf.bin', vocab_file='vocab.txt',
            save_file='vectors', gradsq_file='gradsq', save_gradsq=False,
            checkpoint_every=0):
        # Adjust boolean variables
        if write_header: write_header = 1
        else: write_header = 0
        if save_gradsq: save_gradsq = 1
        else: save_gradsq = 0
        # Define arguments
        args = [
            'glove',
            '-verbose', str(self.verbose),
	        '-write-header', str(write_header),
	        '-vector-size', str(vector_size),
	        '-threads', str(self.threads),
	        '-iter', str(itera),
	        '-eta', str(eta),
	        '-alpha', str(alpha),
	        '-x-max', str(x_max),
	        '-binary', str(binary),
	        '-model', str(model),
	        '-input-file', input_file,
	        '-vocab-file', vocab_file,
	        '-save-file', save_file,
	        '-save-gradsq', str(save_gradsq),
            '-checkpoint-every', str(checkpoint_every)
        ]
        # Check override variable
        if gradsq_file != 'gradsq':
            args.append('-gradsq-file')
            args.append(gradsq_file)
        # Call C code
        glv.glove_wrap(args)

    def load(self, vocab_file='vocab.txt', vectors_file='vectors.txt',
            normalize=True):
        with open(vocab_file, 'r') as f:
            words = [x.rstrip().split(' ')[0] for x in f.readlines()]
        with open(vectors_file, 'r') as f:
            vectors = {}
            for line in f:
                vals = line.rstrip().split(' ')
                vectors[vals[0]] = [float(x) for x in vals[1:]]

        vocab_size = len(words)
        vocab = {w: idx for idx, w in enumerate(words)}
        ivocab = {idx: w for idx, w in enumerate(words)}

        vector_dim = len(vectors[ivocab[0]])
        W = np.zeros((vocab_size, vector_dim))
        for word, v in vectors.items():
            if word == '<unk>':
                continue
            W[vocab[word], :] = v

        if normalize:
            W_norm = np.zeros(W.shape)
            d = (np.sum(W ** 2, 1) ** (0.5))
            W_norm = (W.T / d).T
            W = W_norm
        return vocab, W

    def shuffle(self, array_size=0, temp_file='temp_shuffle',
            cooccurrence_file='cooccurrence.bin',
            cooccurrence_shuf_file='cooccurrence.shuf.bin'):
        # Define arguments
        args = [
            'shuffle',
            cooccurrence_file, cooccurrence_shuf_file,
            '-verbose', str(self.verbose),
            '-memory', str(self.memory),
            '-temp-file', temp_file
        ]
        # Call C code
        shuffle.shuffle_wrap(args)

    def vocab_count(self, max_vocab=0, min_count=1, vocab_file='vocab.txt',
                    corpus_file='corpus.txt'):
        # Define arguments
        args = [
            'vocab_count',
            corpus_file, vocab_file,
            '-verbose', str(self.verbose),
            '-max-vocab', str(max_vocab),
            '-min-count', str(min_count)
        ]
        #call C code
        vocab_count.vocab_count_wrap(args)
