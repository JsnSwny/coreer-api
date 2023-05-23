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
from operator import itemgetter
from django.db.models import Q
import heapq

def base_recommend(r, user_id, id_dict, n):
    start_time = time.time()
    if r.exists('tfidf_matrix_data'):
        print("USING REDIS")
        tfidf_matrix_data = np.frombuffer(r.get('tfidf_matrix_data'), dtype=np.float64)
        tfidf_matrix_indices = np.frombuffer(r.get('tfidf_matrix_indices'), dtype=np.int32)
        tfidf_matrix_indptr = np.frombuffer(r.get('tfidf_matrix_indptr'), dtype=np.int32)
        tfidf_matrix_shape = np.frombuffer(r.get('tfidf_matrix_shape'), dtype=np.int32)
        tfidf_matrix = csr_matrix((tfidf_matrix_data, tfidf_matrix_indices, tfidf_matrix_indptr), shape=tuple(tfidf_matrix_shape))
    else:
        vec = TfidfVectorizer(strip_accents="unicode", stop_words="english")
        user_bios = list(CustomUser.objects.all().values_list("tfidf_input", flat=True).order_by("id"))
        tfidf_matrix = vec.fit_transform(user_bios)

        r.set('tfidf_matrix_data', tfidf_matrix.data.tobytes())
        r.set('tfidf_matrix_indices', tfidf_matrix.indices.tobytes())
        r.set('tfidf_matrix_indptr', tfidf_matrix.indptr.tobytes())
        r.set('tfidf_matrix_shape', np.array(tfidf_matrix.shape, dtype=np.int32).tobytes())

    print(f"Redis completed in {time.time() - start_time}s")
    # print(tfidf_matrix)
    sim = cosine_similarity(tfidf_matrix, tfidf_matrix[id_dict[user_id]])[0:168105]
    print(sim[0:100])


    print(f"Sim completed in {time.time() - start_time}s")
    

    interactions = Recommendation.objects.filter(from_user__id=user_id).values_list("to_user__id", "recommended_on")
    for i in interactions:
        diff = datetime.now(timezone.utc) - i[1]
        days, seconds = diff.days, diff.seconds
        sim[id_dict[i[0]]] *= (0.9 - abs(days * 0.1))
    scores = enumerate(sim)

    # sorted_scores=sorted(scores,key=lambda x:x[1], reverse=True)
    sorted_scores = heapq.nlargest(n, scores, key=lambda x: x[1])
    print(f"Base completed in {time.time() - start_time}s")
    return sorted_scores[0:20]


def content_based_recommendations(r, user_id, id_dict, n, weight=1):   
    following_time = time.time() 

    if r.exists('tfidf_matrix_data'):

        tfidf_matrix_data = np.frombuffer(r.get('tfidf_matrix_data'), dtype=np.float64)
        tfidf_matrix_indices = np.frombuffer(r.get('tfidf_matrix_indices'), dtype=np.int32)
        tfidf_matrix_indptr = np.frombuffer(r.get('tfidf_matrix_indptr'), dtype=np.int32)
        tfidf_matrix_shape = np.frombuffer(r.get('tfidf_matrix_shape'), dtype=np.int32)
        tfidf_matrix = csr_matrix((tfidf_matrix_data, tfidf_matrix_indices, tfidf_matrix_indptr), shape=tuple(tfidf_matrix_shape))
        print(f"Redis time: {time.time() - following_time}")
    else:
        vec = TfidfVectorizer(strip_accents="unicode", stop_words="english")
        user_bios = list(CustomUser.objects.all().values_list("tfidf_input", flat=True).order_by("id"))
        tfidf_matrix = vec.fit_transform(user_bios)

        r.set('tfidf_matrix_data', tfidf_matrix.data.tobytes())
        r.set('tfidf_matrix_indices', tfidf_matrix.indices.tobytes())
        r.set('tfidf_matrix_indptr', tfidf_matrix.indptr.tobytes())
        r.set('tfidf_matrix_shape', np.array(tfidf_matrix.shape, dtype=np.int32).tobytes())

    following_time = time.time()
    arr_list = []
    following_list = Follow.objects.filter(follower__id=user_id).values_list("following__id", "followed_on").order_by("-followed_on")[0:5]
    for user in following_list:
        print(user)
        sim = cosine_similarity(tfidf_matrix, tfidf_matrix[id_dict[user[0]]])
        sim[id_dict[user[0]]] = 0
        # diff = datetime.now(timezone.utc) - user[1]
        # weight = math.exp(-0.05 * diff.days)
        # weighted_sim = (weight * sim)
        arr_list.append(sim)
    following_time = time.time()
    user_sim = sum(arr_list) / 5
    user_sim = user_sim[0:168105]

    interactions = Recommendation.objects.filter(from_user__id=user_id).values_list("to_user__id", "recommended_on")
    for i in interactions:
        diff = datetime.now(timezone.utc) - i[1]
        days, seconds = diff.days, diff.seconds
        user_sim[id_dict[i[0]]] = user_sim[id_dict[i[0]]] * (0.9 - abs(days * 0.1))

    following_time = time.time()
    scores = enumerate(user_sim)
    following_time = time.time()
    # sorted_scores=sorted(scores,key=lambda x:x[1], reverse=True)
    sorted_scores = heapq.nlargest(n, scores, key=lambda x: x[1])
    
    return sorted_scores

def build_user_similarity_matrix(r, user_id, user_ids, id_dict, n):
    if r.exists('csr_matrix_data'):
        csr_matrix_data = np.frombuffer(r.get('csr_matrix_data'), dtype=np.int32)
        csr_matrix_indices = np.frombuffer(r.get('csr_matrix_indices'), dtype=np.int32)
        csr_matrix_indptr = np.frombuffer(r.get('csr_matrix_indptr'), dtype=np.int32)
        csr_matrix_shape = np.frombuffer(r.get('csr_matrix_shape'), dtype=np.int32)
        sparse_matrix = csr_matrix((csr_matrix_data, csr_matrix_indices, csr_matrix_indptr), shape=tuple(csr_matrix_shape))
    else:
        following = Follow.objects.all().values_list("follower__id", "following__id")
        
        row = []
        col = []
        data = []

        for i in following:
            row.append(id_dict[i[0]])
            col.append(id_dict[i[1]])
            data.append(1)

        sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_ids), len(user_ids)), dtype=np.int32)

        r.set('csr_matrix_data', sparse_matrix.data.tobytes())
        r.set('csr_matrix_indices', sparse_matrix.indices.tobytes())
        r.set('csr_matrix_indptr', sparse_matrix.indptr.tobytes())
        r.set('csr_matrix_shape', np.array(sparse_matrix.shape, dtype=np.int32).tobytes())

    

    user_sim = cosine_similarity(sparse_matrix, sparse_matrix[id_dict[user_id]])[0:168105]

    
    interactions = Recommendation.objects.filter(from_user__id=user_id).values_list("to_user__id", "recommended_on")
    for i in interactions:
        diff = datetime.now(timezone.utc) - i[1]
        days = diff.days  
        user_sim[id_dict[i[0]]] = user_sim[id_dict[i[0]]] * (0.9 - abs(days * 0.1))
    following_time = time.time()
    scores = enumerate(user_sim)
    scores = [(i, x) for i, x in scores if x > 0]
    sorted_scores = heapq.nlargest(n, scores, key=lambda x: x[1])
    # sorted_scores=sorted(scores,key=lambda x:x[1], reverse=True)
    # print(f"Sort time = {time.time() - following_time}")
    return sorted_scores

def get_top_n_recommendations(user_id, n, users_n=160000):
    r = redis.Redis(host='localhost', port=6379, db=0)
    # r.flushdb()
    # COLLABORATIVE FILTERING
    # -----------------------

    print(f"Getting {user_id}'s recommendations")
    user_objects = CustomUser.objects.all().order_by("id")
    user_ids = list(user_objects.values_list("id", flat=True))
    
    id_dict = dict(zip(user_ids, range(len(user_ids))))

    

    start = time.time()

    print("Recommending...")
    following_list = CustomUser.objects.get(id=user_id).followers.all().values_list("following__id", flat=True)

    following_list_idx = []
    for i in following_list:
        following_list_idx.append(id_dict[i])
    
    if len(following_list) < 5:
        scores = base_recommend(r, user_id, id_dict, n)
        sorted_scores = [user_objects[i[0]] for i in scores if i[0] != id_dict[user_id] and i[0] not in following_list_idx]
        return sorted_scores
    
    # CONTENT BASED FILTERING
    # -----------------------
    matrix_time = time.time()    
    cb_scores = content_based_recommendations(r, user_id, id_dict, n+20)
    print(f"Content filtering: {time.time() - matrix_time}s")
    print(cb_scores)

    # COLLABORATIVE FILTERING
    # -----------------------
    matrix_time = time.time()
    cf_scores = build_user_similarity_matrix(r, user_id, user_ids, id_dict, n+20)
    print(f"Collaborative filtering: {time.time() - matrix_time}s")
    print(cf_scores)


    matrix_time = time.time()
    

    cb_sorted_scores = [i for i in cb_scores if i[0] != id_dict[user_id] and i[0] not in following_list_idx]
    cf_sorted_scores = [i for i in cf_scores if i[0] != id_dict[user_id] and i[0] not in following_list_idx]

    print(cb_sorted_scores)
    print(cf_sorted_scores)
    
        # Take the top elements from each sorted list
    collab_top = cf_sorted_scores[:5]
    content_top = cb_sorted_scores[:5]

    # combined_top = [x for pair in zip(collab_top, content_top) for x in pair]

    combined_top = collab_top + content_top

    print("Combined Top:")
    print(combined_top)

    if len(combined_top) < n:
        remaining = n - len(combined_top)
        if len(cf_sorted_scores) < n:
            content_remaining = cb_sorted_scores[n:n+remaining]
            combined_top += content_remaining
        else:
            collab_remaining = cf_sorted_scores[n:n+remaining]
            combined_top += collab_remaining
    final_scores = sorted(combined_top, key=lambda x: x[1], reverse=True)

    print(f"Total time: {time.time() - start}")

    return [user_objects[i[0]] for i in final_scores][0:n]

    
    
    # # print(sorted_scores)
    return combined