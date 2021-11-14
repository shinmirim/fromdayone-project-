from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from .models import Fashion
from django.db.models import Q # new
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
import seaborn as sns
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics import mean_squared_error
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

# Create your views here.
        
def index(request):
    return render(request, 'index.html')

def ver1(request):
    return render(request, 'ver1.html')

def ver2(request):
    return render(request, 'ver2.html')

def cos_sim(A, B):
       return dot(A, B)/(norm(A)*norm(B))



def ver1(request):
    getlist = pd.read_csv('아이템기반최종데이터.csv', encoding='cp949')

    if request.method == 'POST':

        data = pd.read_csv('아이템기반최종데이터.csv', encoding='cp949')
    
        data=data[['상품명','카테고리','패턴재질','모양','계절','스타일','종합점수']]
        
        df=data.drop_duplicates(['상품명'])
        
        df=df[['상품명','스타일','계절','카테고리','모양','패턴재질']]
        
        df = pd.get_dummies(data = df, columns = ['스타일'], prefix = '스타일')
        df = pd.get_dummies(data = df, columns = ['계절'], prefix = '계절')
        df = pd.get_dummies(data = df, columns = ['카테고리'], prefix = '카테고리')
        df = pd.get_dummies(data = df, columns = ['모양'], prefix = '모양')
        df = pd.get_dummies(data = df, columns = ['패턴재질'], prefix = '패턴재질')
        
        df.set_index(['상품명'],inplace=True)

        cosine_sim = linear_kernel(df, df)

        indices =pd.Series(range(1844),index=df.index)
        indices1=pd.Series(df.index)
        idx = indices['[DAYONE LABEL]렌프 자켓원피스(벨트set)']
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [i[0] for i in sim_scores]
        dfs=pd.read_csv('아이템기반최종데이터.csv', encoding='cp949')
        dfs=dfs[['상품명','카테고리','패턴재질','모양','계절','스타일']]

        def get_recommendations(title, cosine_sim=cosine_sim):
            # 선택한 상품명 해당되는 인덱스를 받아옵니다. 이제 선택한 상품를 가지고 연산할 수 있습니다.
            idx = indices[title]

            # 모든 상품대해서 해당 상품와의 유사도를 구합니다.
            sim_scores = list(enumerate(cosine_sim[idx]))

            # 유사도에 따라 상품들을 정렬합니다.
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # 가장 유사한 10개의 상품을 받아옵니다.
            sim_scores = sim_scores[1:11]

            # 가장 유사한 10개의 상품의 인덱스를 받아옵니다.
            movie_indices = [i[0] for i in sim_scores]
            
            result=pd.DataFrame(indices1[movie_indices])
            laster=pd.merge(result,dfs,how='left' )
            laster=laster.drop_duplicates(['상품명'])
            
            # 가장 유사한 10개의 상품의 제목을 리턴합니다.
            return laster


        product_name = request.POST.get('name','')
        result = get_recommendations(product_name)
        print(result)
        print(type(result))
        val_list = result.values.tolist()
        print(type(val_list))
        print(val_list)



    #     result = recomm_beer(df, beer_name)
    #     result = result.index.tolist()

    #     # 클러스터링 결과
    #     tmp_cluster=[]
    #     category=[]
    #     food=[]
    #     for i in range(3):
    #         target = cluster_all[cluster_all['맥주']==result[i]]
    #         target = target[['Aroma', 'Appearance', 'Flavor', 'Mouthfeel', 'Overall']]
    #         target = target.values[0]
    #         tmp_cluster.append(target)

    #         try :
    #             category.append(beer_data[beer_data['맥주이름']==result[i]]['Main Category'].values[0])
    #             food.append(beer_data[beer_data['맥주이름']==result[i]]['Paring Food'].values[0])
    #         except :
    #             category.append('수집되지 않았습니다.')
    #             food.append('수집되지 않았습니다.')
    #     # 연도별 평점 결과
    #     tmp_year = []
    #     tmp_ratings = []
    #     for i in range(3):
    #         target = beer_year[beer_year['맥주']==result[i]]
    #         target_year = target['년'].tolist()
    #         target_rating = target['평점'].tolist()
    #         tmp_year.append(target_year)
    #         tmp_ratings.append(target_rating)

    #     # 넘겨줄 데이터 Json 변환
    #     targetdict = {
    #         'beer_name' : result,
    #         'beer_cluster1' : tmp_cluster[0].tolist(),
    #         'beer_cluster2' : tmp_cluster[1].tolist(),
    #         'beer_cluster3' : tmp_cluster[2].tolist(),
    #         'cluster1' : cluster_3[0].tolist(),
    #         'cluster2' : cluster_3[1].tolist(),
    #         'cluster3' : cluster_3[2].tolist(),
    #         'tmp_year' : tmp_year,
    #         'tmp_ratings' : tmp_ratings
    #     }

    #     targetJson = json.dumps(targetdict)

        return render(request, 'ver1_result.html',
                 {'result':val_list})
    else:
        return render(request, 'ver1.html', {'list':getlist})

