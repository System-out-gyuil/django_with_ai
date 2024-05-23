# 🪴Selleaf

### 목차

1. AI 서비스 설명

2. AI 사전 훈련 모델

3. AI 모델 내보내기

4. AI 모델 적용

### 1. AI 서비스 설명

  #### 회원이 자주보는 노하우 게시글을 통해 AI가 추천하는 게시글을 메인화면에 나타내주는 서비스입니다.

  #### 회원가입 시 해당 회원의 사전훈련모델을 기반으로 한 개인 모델을 생성합니다.

  #### 가장 최근에 본 세개의 노하우 게시글의 제목과 내용을 사용하여 predict_proba를 통해 나온 각각의 확률을 순위를 매겨 게시글을 추천해줍니다.

  #### 노하우 게시글 상세보기 페이지에 들어갈때마다 해당 회원의 개인 모델에 fit 해줍니다.

### 2. AI 사전 훈련 모델



- 1. 데이터 수집  
     https://www.gardening.news/ 해당 사이트에서 크롤링을 통해 제목과 내용, 카테고리를 발췌하였습니다.

- 2. 데이터 전처리 및 모델 학습

  - 우선 데이터의 제목과 내용을 이어서 붙혀주었습니다.  
    ex) 제목: 안녕하세요, 내용: 반갑습니다 ▶️ 안녕하세요 반갑습니다.

  - 타겟피쳐인 카테고리가 문자열 형식으로 되어있어 레이블인코딩을 통해 인코딩해주었습니다

    > 0 - 꽃  
    > 1 - 농촌  
    > 2 - 원예  
    > 3 - 정원

  - 파이프라인 구축을 통해 CountVectorizer와 MultinomialNB를 사용하여 훈련하였을 때

    <img src='../images/knowhow_eva01.png'>

    정확도: 0.6844, 정밀도: 0.6620, 재현율: 0.6352, F1: 0.6309

  - 결과가 그렇게 나쁘지 않았으나 위의 시각화를 통해 확인할 수 있듯이 타겟의 비중이 맞지않아  
    정답이 한쪽에 쏠려있는 모습을 볼 수 있습니다.

  - 따라서 타겟의 비중을 맞추기 위하여 언더샘플링을 진행하였습니다.

  - 언더샘플링을 진행한 후  
    <img src='../images/knowhow_eva02.png'>  
    정확도: 0.5580, 정밀도: 0.6526, 재현율: 0.5796, F1: 0.5387

  - 수치가 조금 떨어지긴 하였으나 언더샘플링을 진행하기 전엔 임의의 값을 넣고 predict를 하였을 경우  
    결과가 자꾸 한쪽으로만 나타나서 언더샘플링을 사용한채로 진행하였습니다.

- 3. 테스트

  - 직접 제목과 내용을 전달하여 확인해보았습니다.

  <details>
  <summary>Click all Code</summary>
  <!-- 가장 최근에 본 세개의 게시글의 제목과 내용을 이어붙힌 문자열을 직접 전달 -->
  proba1 = m_nb_pipe.predict_proba(['제가 직접 키운 나무 어떤가요 제작년부터 아들이랑 같이 심어본 나무인데 어떠신가요? 쑥쑥 자라더니 이제 키높이만큼 자랐어요'])  
  proba2 = m_nb_pipe.predict_proba(['꽃을 키우는걸 너무 좋아하는데 원예동아리같은데에 들어가고싶어요'])  
  proba3 = m_nb_pipe.predict_proba(['집앞에서 이렇게 해봤어요 집앞에 나가봤는데 꽃이 많이 피었길래 화관을 만들어보았어요'])

  <!-- 세개의 게시글에 predict_proba를 통해 나온 각 타겟별 확률들을 더해줌 -->

  total_proba = [0] \* len(proba1[0])
  for i in range(len(proba1[0])): # print(proba1[0][i])
  total_proba[i] = (proba1[0][i] + proba2[0][i] + proba3[0][i])

  <!-- 더해진 확률 출력 -->

  print(total_proba)

  <!-- 각 확률의 결과를 argsort를 통해 높은순으로 정렬 후 슬라이싱을 통해 3등까지의 결과를 가져왔다. -->

  result*proba = np.argsort(total_proba)[::-1][0:3]
  for i in result_proba:
  print(encoder.classes*[i])
  </details>

  - 최근에 본 세개의 게시글의 제목과 내용은
    > 1. 제가 직접 키운 나무 어떤가요 제작년부터 아들이랑 같이 심어본 나무인데 어떠신가요? 쑥쑥 자라더니 이제 키높이만큼 자랐어요
    > 2. 꽃을 키우는걸 너무 좋아하는데 원예동아리같은데에 들어가고싶어요
    > 3. 집앞에서 이렇게 해봤어요 집앞에 나가봤는데 꽃이 많이 피었길래 화관을 만들어보았어요
  - 위와 같이 직접 작성하였고
  - 결과는 아래와 같았습니다.  
    <img src='../images/knowhow_result01.png'>

  - 글의 내용과 결과로 나온 카테고리가 굉장히 잘 맞는 모습을 보였습니다.

#### 3. pkl파일로 내보내기

- joblib의 dump를 사용하여 모델을 pkl파일로 내보내준 후 잘 나오는지 확인을 해보았습니다.  
  <img src='../images/knowhow_eva03.png'>  
  정확도: 0.5580, 정밀도: 0.6526, 재현율: 0.5796, F1: 0.5387
- 위에서 내보낸 pkl파일을 불러와서 불러온 모델을 통해 학습한 결과또한 기본 모델과 똑같이 작동되는것을 확인하였습니다.

#### 4. AI모델 적용

- 노하우 게시글을 세개 이상 들어가본 회원의 메인화면에서 제목과 내용을 토대로 카테고리를 예측해 추천해줍니다.  
<img src='../images/knowhjow_ai_main01.png'>  