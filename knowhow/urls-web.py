from django.urls import path

from knowhow.views import KnowhowCreateView, KnowhowDetailView, KnowhowReplyWriteApi, \
    KnowhowDetailApi, KnowhowReplyApi, KnowhowListApi, KnowhowListView, KnowhowUpdateView, \
    KnowhowDeleteView, KnowhowScrapApi, KnowhowLikeApi, KnowhowReportView, KnowhowRecommendationAPI

app_name = 'knowhow'

urlpatterns = [
    # 노하우 작성
    path('create/', KnowhowCreateView.as_view(), name='create'),
    # 노하우 상세
    path('detail/', KnowhowDetailView.as_view(), name='detail'),
    # 노하우 수정
    path('update/', KnowhowUpdateView.as_view(), name='update'),
    # 노하우 삭제
    path('delete/', KnowhowDeleteView.as_view(), name='delete'),
    # 포스트 신고
    path('report/', KnowhowReportView.as_view(), name='report'),
    # 노하우 목록
    path('list/', KnowhowListView.as_view(), name='list'),
    path('list/<int:page>/<str:filters>/<str:sorting>/<str:types>', KnowhowListApi.as_view(), name='list'),

    # 노하우 스크랩
    path('like/scrap/<int:knowhow_id>/<int:member_id>/<str:scrap_status>/', KnowhowScrapApi.as_view(), name='list'),
    # 노하우 좋아요
    path('like/scrap/<int:knowhow_id>/<int:member_id>/<str:like_status>', KnowhowLikeApi.as_view(), name='list'),

    # 댓글
    path('replies/write/', KnowhowReplyWriteApi.as_view(), name='reply_write'),
    path('replies/list/<int:knowhow_id>/<int:page>/', KnowhowDetailApi.as_view(), name='reply_list'),
    path('replies/<int:reply_id>/', KnowhowReplyApi.as_view()),

    # 제목기반 내용 자동 추천
    path('content-recommendation/<str:title>/', KnowhowRecommendationAPI.as_view())

    #좋아요 스크랩
    # path('like/scrap/<int:status>/', KnowhowLikeScrapApi.as_view(), name='like_scrap'),

]