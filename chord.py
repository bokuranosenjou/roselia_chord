import gensim
import numpy as np
from scipy import spatial

from roselia_songs import roselia_dict


targets = ["Neo-Aspect", "ROZEN_HORIZON"]
num_features = 10

def train_rozen_horizon():
    PATH = "./agematsu/ROZEN_HORIZON.txt"
    with open(PATH, mode="r") as f:
        chord = [s.rstrip() for s in f.readlines()]
        sentences = [c.split() for c in chord]
    model = gensim.models.word2vec.Word2Vec(sentences, vector_size=num_features, min_count=1, window=1)
    for key, value in model.wv.most_similar('C'):
        print("chord : {}, score : {}".format(key, value))
    return model


def train():
    sentences = []
    for composer, dict_ in roselia_dict.items():
        for song, _ in dict_.items():
            if song in targets : 
                continue
            print("song : {}, composer : {}".format(song, composer))
            PATH = "./{}/{}.txt".format(composer, song)
            with open(PATH, mode="r") as f:
                chord = [s.rstrip() for s in f.readlines()]
            sentences = sentences + [c.split() for c in chord]

    model = gensim.models.word2vec.Word2Vec(sentences, vector_size=num_features, min_count=1, window=1)
    return model


def validate(model):
    # 参考 https://qiita.com/yoppe/items/512c7c072d08c64afa7e#%E6%96%87%E7%AB%A0%E3%81%A7%E4%BD%BF%E7%94%A8%E3%81%95%E3%82%8C%E3%81%A6%E3%81%84%E3%82%8B%E5%8D%98%E8%AA%9E%E3%81%AE%E7%89%B9%E5%BE%B4%E3%83%99%E3%82%AF%E3%83%88%E3%83%AB%E3%81%AE%E5%B9%B3%E5%9D%87%E3%82%92%E7%AE%97%E5%87%BA
    def avg_feature_vector(chord, model, num_features=num_features):
        feature_vec = np.zeros((num_features,), dtype="float32") # 特徴ベクトルの入れ物を初期化
        for ichord in chord:
            feature_vec = np.add(feature_vec, model.wv[ichord])
        if len(chord) > 0:
            feature_vec = np.divide(feature_vec, len(chord))
        return feature_vec
    
    # 各曲のベクトルを計算
    song_dict = {}
    song_composer_pair = {}
    for composer, dict_ in roselia_dict.items():
        for song, _ in dict_.items():
            PATH = "./{}/{}.txt".format(composer, song)

            with open(PATH, mode="r") as f:
                chord = [s.rstrip() for s in f.readlines()]
                chord = [c for c in chord if c in model.wv]

            song_dict[song] = avg_feature_vector(chord, model)
            song_composer_pair[song] = composer
    
    def validate_target(targets):
        for target in targets:
            print("=============================================")
            print("target :: {} (composer : {})".format(target, song_composer_pair[target]))
            scores = {
                "fujinaga" : [],
                "agematsu" : [],
            }
            results = []
            for song, vector in song_dict.items():
                if song == target : 
                    continue
                results.append([1 - spatial.distance.cosine(vector, song_dict[target]), song])
            results.sort(reverse=True)
            for val, song in results:
                if song_composer_pair[song] not in scores : continue
                print("song : {}, composer : {}, score : {}".format(song, song_composer_pair[song], val))
                scores[song_composer_pair[song]].append(val)
            
            print()
            for key, value in scores.items():
                print("Average_score", key, np.mean(np.array(value)))

    # Neo-Aspect, ROZEN_HORIZON
    validate_target(targets)


    # Throne_of_Rose
    validate_target(["Throne_of_Rose"])

    print("=============================================")

if __name__ == "__main__":
    train_rozen_horizon()
    model = train()
    validate(model)