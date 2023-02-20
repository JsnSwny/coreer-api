from accounts.models import CustomUser, Follow
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import redis
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer#
import random

def similarities(user_id, weight=1):
    user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))
    id_dict = dict(zip(user_ids, range(len(user_ids))))
    user_objects = list(CustomUser.objects.all().order_by("id"))

    # following_list = CustomUser.objects.get(id=user_id).likes.all().values_list("id", flat=True).reverse()
    following_list = Follow.objects.filter(follower__id=user_id).values_list("following__id", flat=True).order_by("-followed_on")[0:5]
    print(following_list)
    
    vec = TfidfVectorizer(strip_accents="unicode", stop_words="english", min_df=3)
    user_bios = list(CustomUser.objects.values_list("bio", flat=True).order_by("id"))
    vecs = vec.fit_transform(user_bios)

    arr_list = []
    for user in following_list:
        sim = cosine_similarity(vecs, vecs[id_dict[user]])
        sim[id_dict[user]] = 0
        weighted_sim = (1 * (sim*weight)) # + (0.25 * normed_dist[user])
        arr_list.append(weighted_sim)
    
    scores = enumerate(sum(arr_list))
    sorted_scores=sorted(scores,key=lambda x:x[1], reverse=True)
    return sorted_scores

def build_user_similarity_matrix(user_id):
    # Get the list of all user IDs
    user_objects = list(CustomUser.objects.all().order_by("id"))
    user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))

    following = Follow.objects.values_list("follower__id", "following__id")

    id_dict = dict(zip(user_ids, range(len(user_ids))))
    row = []
    col = []
    data = []
    count = 0

    for i in following:
        row.append(id_dict[i[0]])
        col.append(id_dict[i[1]])
        data.append(1)

    print("COMPLETE")

    sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_ids), len(user_ids)), dtype=np.int32)

    user_sim = cosine_similarity(sparse_matrix, sparse_matrix[id_dict[user_id]])

    return user_sim
    # # Cache the user similarity matrix
    # joblib.dump(user_sim, 'user_similarity_matrix.joblib')

    r = redis.Redis(host='localhost', port=6379, db=0)
    # for i, user in enumerate(user_ids):
    for j, sim in enumerate(user_sim):
        key = f"user:{24}:similarity:{user_ids[j].id}"
        print(key)
        print(sim)
        r.set(key, sim[0])

def get_top_n_recommendations(user_id, n=10):
    # Check if the user similarity matrix is already cached

    print("Recommending...")

    user_objects = list(CustomUser.objects.all().order_by("id"))
    following_list = Follow.objects.filter(follower__id=user_id).values_list("following__id", flat=True)
    if len(following_list) < 5:
        q_ids = list(CustomUser.objects.values_list('id', flat=True))
        r_ids = random.sample(q_ids, 10)
        return CustomUser.objects.filter(id__in=r_ids)

    user_sim = build_user_similarity_matrix(user_id)
    

    
    user_ids = list(CustomUser.objects.values_list("id", flat=True).order_by("id"))

    id_dict = dict(zip(user_ids, range(len(user_ids))))

    # Get the indices of the top n most similar users
    scores = enumerate(user_sim)
    sorted_scores=sorted(scores,key=lambda x:x[1], reverse=True)

    
    following_list_idx = []
    for i in following_list:
        following_list_idx.append(id_dict[i])


    sorted_scores = [i for i in sorted_scores if i[0] != id_dict[user_id] and i[0] not in following_list_idx][:10]

    print(sorted_scores)

    cb_score = similarities(user_id)
    cb_sorted_scores = [i for i in cb_score if i[0] != id_dict[user_id] and i[0] not in following_list_idx][:10]

    combined = [user_objects[x[0]] for pair in zip(cb_sorted_scores, sorted_scores) for x in pair]

    print(combined)
    return combined