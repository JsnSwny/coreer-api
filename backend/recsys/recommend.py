from accounts.models import CustomUser, Follow
from recsys.models import Recommendation
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import redis
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer#
import random
import time
from datetime import datetime, timezone
import math

def base_recommend(user_id, id_dict):
    vec = TfidfVectorizer(strip_accents="unicode", stop_words="english", min_df=3)
    clean_input = []
    users = CustomUser.objects.all()[0:10000]
    for idx, i in enumerate(users):
        user_input = ""
        if i.bio:
            print(i.bio)
            user_input += i.bio
        for language in i.languages.values_list('name', flat=True):
            user_input += f" {language}"
        # if len(i.interests.all()) > 0:
        #     for interest in i.interests.all():
        #         user_input += f" {interest.name}"
        print(idx)
        clean_input.append(user_input)
        
    tfidf_matrix = vec.fit_transform(clean_input)
    



def similarities(user_id, id_dict, weight=1):    
    r = redis.Redis(host='localhost', port=6379, db=0)

    if r.exists('tfidf_matrix_data'):
        tfidf_matrix_data = np.frombuffer(r.get('tfidf_matrix_data'), dtype=np.float64)
        tfidf_matrix_indices = np.frombuffer(r.get('tfidf_matrix_indices'), dtype=np.int32)
        tfidf_matrix_indptr = np.frombuffer(r.get('tfidf_matrix_indptr'), dtype=np.int32)
        tfidf_matrix_shape = np.frombuffer(r.get('tfidf_matrix_shape'), dtype=np.int32)
        tfidf_matrix = csr_matrix((tfidf_matrix_data, tfidf_matrix_indices, tfidf_matrix_indptr), shape=tuple(tfidf_matrix_shape))
    else:
        vec = TfidfVectorizer(strip_accents="unicode", stop_words="english", min_df=3)
        user_bios = list(CustomUser.objects.values_list("bio", flat=True).order_by("id"))
        tfidf_matrix = vec.fit_transform(user_bios)

        r.set('tfidf_matrix_data', tfidf_matrix.data.tobytes())
        r.set('tfidf_matrix_indices', tfidf_matrix.indices.tobytes())
        r.set('tfidf_matrix_indptr', tfidf_matrix.indptr.tobytes())
        r.set('tfidf_matrix_shape', np.array(tfidf_matrix.shape, dtype=np.int32).tobytes())

    following_time = time.time()
    arr_list = []
    following_list = Follow.objects.filter(follower__id=user_id).values_list("following__id", "followed_on").order_by("-followed_on")[0:5]
    for user in following_list:
        sim = cosine_similarity(tfidf_matrix, tfidf_matrix[id_dict[user[0]]])
        sim[id_dict[user[0]]] = 0
        diff = datetime.now(timezone.utc) - user[1]
        weight = math.exp(-0.05 * diff.days)
        weighted_sim = (weight * sim)
        arr_list.append(weighted_sim)

    print(f"Following time: {time.time() - following_time}")
    user_sim = sum(arr_list) / 5
    interactions = Recommendation.objects.filter(from_user__id=user_id).values_list("to_user__id", "recommended_on")
    for i in interactions:
        diff = datetime.now(timezone.utc) - i[1]
        days, seconds = diff.days, diff.seconds
        
        user_sim[id_dict[i[0]]] = user_sim[id_dict[i[0]]] * (0.9 - (days * 0.1))
    
    scores = enumerate(user_sim)
    sorted_scores=sorted(scores,key=lambda x:x[1], reverse=True)
    return sorted_scores

def build_user_similarity_matrix(user_id, id_dict):
    r = redis.Redis(host='localhost', port=6379, db=0)

    if r.exists('csr_matrix_data'):
        csr_matrix_data = np.frombuffer(r.get('csr_matrix_data'), dtype=np.int32)
        csr_matrix_indices = np.frombuffer(r.get('csr_matrix_indices'), dtype=np.int32)
        csr_matrix_indptr = np.frombuffer(r.get('csr_matrix_indptr'), dtype=np.int32)
        csr_matrix_shape = np.frombuffer(r.get('csr_matrix_shape'), dtype=np.int32)
        sparse_matrix = csr_matrix((csr_matrix_data, csr_matrix_indices, csr_matrix_indptr), shape=tuple(csr_matrix_shape))
    else:
        following = Follow.objects.values_list("follower__id", "following__id")
        
        row = []
        col = []
        data = []

        for i in following:
            row.append(id_dict[i[0]])
            col.append(id_dict[i[1]])
            data.append(1)

        sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_id), len(user_id)), dtype=np.int32)

        r.set('csr_matrix_data', sparse_matrix.data.tobytes())
        r.set('csr_matrix_indices', sparse_matrix.indices.tobytes())
        r.set('csr_matrix_indptr', sparse_matrix.indptr.tobytes())
        r.set('csr_matrix_shape', np.array(sparse_matrix.shape, dtype=np.int32).tobytes())

    

    user_sim = cosine_similarity(sparse_matrix, sparse_matrix[id_dict[user_id]])
    interactions = Recommendation.objects.filter(from_user__id=user_id).values_list("to_user__id", "recommended_on")
    for i in interactions:
        diff = datetime.now(timezone.utc) - i[1]
        days = diff.days

        print(user_sim[id_dict[i[0]]])
        
        user_sim[id_dict[i[0]]] = user_sim[id_dict[i[0]]] * (0.9 - (days * 0.1))
        print(user_sim[id_dict[i[0]]])

    return user_sim

def get_top_n_recommendations(user_id, n=10):
    r = redis.Redis(host='localhost', port=6379, db=0)

    # COLLABORATIVE FILTERING
    # -----------------------


    user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))
    id_dict = dict(zip(user_ids, range(len(user_ids))))

    start = time.time()

    print("Recommending...")
    user_objects = CustomUser.objects.all().order_by("id")
    following_list = CustomUser.objects.get(id=user_id).followers.all().values_list("following__id", flat=True)
    
    if len(following_list) < 5:
        base_recommend(user_id, id_dict)
        q_ids = list(CustomUser.objects.values_list('id', flat=True))
        r_ids = random.sample(q_ids, 10)
        return CustomUser.objects.filter(id__in=r_ids)
    
    matrix_time = time.time()
    user_sim = build_user_similarity_matrix(user_id, id_dict)
    print(f"Collaborative filtering: {time.time() - matrix_time}s")
    

    # CONTENT BASED FILTERING
    # ----------------------
    matrix_time = time.time()    
    cb_score = similarities(user_id, id_dict)
    print(f"Content filtering: {time.time() - matrix_time}s")


    matrix_time = time.time()

    
    following_list_idx = []
    for i in following_list:
        following_list_idx.append(id_dict[i])

    cb_sorted_scores = [i for i in cb_score if i[0] != id_dict[user_id] and i[0] not in following_list_idx][:10]

    print(cb_sorted_scores)
    scores = enumerate(user_sim)
    sorted_scores=sorted(scores,key=lambda x:x[1], reverse=True)
    sorted_scores = [i for i in sorted_scores if i[0] != id_dict[user_id] and i[0] not in following_list_idx][:10]

    combined = [user_objects[x[0]] for pair in zip(cb_sorted_scores, sorted_scores) for x in pair]
    print(f"Score sorting: {time.time() - matrix_time}")

    

    print(f"Recommendations complete")
    print(f"Time taken: {time.time() - start}s")
    # print(sorted_scores)
    return combined