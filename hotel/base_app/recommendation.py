import pandas as pd
from . models import Review


def user_data(request):
    datas = Review.objects.all()
    hotelId = []
    userId = []
    rating = []
    for data in datas:
        hotelId.append(data.hotel.reference_id)
        userId.append(data.user.user_id)
        rating.append(data.rating)

    dict = {
        "hotelId": hotelId,
        "userId": userId,
        "rating": rating
    }
    global df
    df = pd.DataFrame(dict)
    #groupby function use to split the data into groups based on some criteria
    popular_products = pd.DataFrame(df.groupby('hotelId')['rating'].count())
    print(popular_products)
    most_popular = popular_products.sort_values('rating', ascending=False)
    df1 = most_popular.reset_index()
    df1 = df1.sort_values('rating', ascending=False)
    most_popular_product_id = df1['hotelId'].tolist()
    userRatings = df.pivot_table(index=['userId'], columns=['hotelId'], values='rating', fill_value=0)

    corrMatrix = userRatings.corr(method='pearson')
    def get_similar(hotelId, rating):
        similar_ratings = corrMatrix[hotelId]*(rating-2)
        similar_ratings = similar_ratings.sort_values(ascending=False)
        return similar_ratings
    
# old_user = [(102, 4), (112, 4), (312, 3)]
    most_popular_product_id_user = None
    if request.user.is_anonymous:
        user = None
    else:
        user = request.user.user_id
    if user:
        old_user = Review.objects.filter(user__user_id=user).values_list('hotel', 'rating')
        if Review.objects.filter(user__user_id=user).exists():
            l1 = []
            for i in old_user:
                l1.append(i)
            similar_product = pd.DataFrame()
            for hotelId, rating in l1:
                similar_product = similar_product._append(
                    get_similar(hotelId, rating), ignore_index=True)
            ssss = similar_product.sum().sort_values(ascending=False)
            df2 = ssss.reset_index()
            most_popular_product_id_user = df2['hotelId'].tolist()
        else:
            most_popular_product_id_user = most_popular_product_id
    return most_popular_product_id, most_popular_product_id_user