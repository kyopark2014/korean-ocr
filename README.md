# Korean OCR

## EasyOCR을 이용한 한국어 OCR 구현하기

[EasyOCR](https://github.com/JaidedAI/EasyOCR), [PaddleOC](https://github.com/PaddlePaddle/PaddleOCR)와 같은 Open Source OCR이 있습니다. 여기서는 [detect-text-lambda-with-easyocr(AWS Sample)](https://github.com/aws-samples/detect-text-lambda-with-easyocr)을 참조하여, Lambda로 한국어가 지원되는 OCR을 구현합니다. 

- [데모](https://www.jaided.ai/easyocr/): 가벼운 테스트 가능
- [detect-text-lambda-with-easyocr(AWS Sample)](https://github.com/aws-samples/detect-text-lambda-with-easyocr): Lambda(10240MB)에서 500KB 미만의 이미지를 처리할 때, 약 1분 내외의 시간이 걸린다고 함

### 구현된 Architecture

전체적인 Architecture는 아래와 같습니다. 여기서는 서버리스 architecture를 이용하기 위하여 OCR를 수행하는 lambda는 container 방식을 이용합니다. 

1) 사용자는 웹브라우저를 이용하여 Amazon CloudFront와 연결된 Amazon S3에서 upload.html 파일을 다운로드 합니다.
2) 웹브라우저에서 파일 버튼을 선택하여 Upload 버턴을 선택합니다. Lambda (upload)로 구현되는 '/upload' API를 이용하여 Amazon S3로 직접 업로드를 할 수 있는 presigned url을 가져옵니다.
3) presigned url을 이용하여 S3에 직접 파일을 업로드 합니다.
4) 웹브라우저에서 Extract 버튼을 선택하면, 업로드한 파일명을 포함한 정보를 Lambda (ocr)로 전달하여 이미지로 부터 텍스트를 추출합니다. 추출된 정보에는 텍스트와 문장의 위치 정보를 가지고 있으며, json 포멧으로 브라우저를 통해 조회할 수 있습니다.
5) 추출된 텍스트를 DynamoDB에 저장합니다. 텍스트 추출 시간이 오래 걸려서, 브라우저에서 결과 읽어오기에 실패하면, 다시 텍스트 추출을 요청하지 않고, DynamoDB로 부터 추출된 결과를 조회합니다.

![image](https://github.com/kyopark2014/korean-ocr/assets/52392004/13c56c6b-5b89-4d0d-99f5-ac13cb7c0955)

### 구현 방법

EasyOCR를 lambda에 deploy하기 위하여 아래와 같이 Dockerfile을 정의합니다. [Dockerfile](https://github.com/kyopark2014/korean-ocr/blob/main/lambda-easy-ocr/Dockerfile)와 같이 OCR에 필요한 package는 easyocr과 numpy입니다. 

```text
FROM amazon/aws-lambda-python:3.11
WORKDIR /var/task/lambda-chat

COPY lambda_function.py /var/task/
COPY . ..

RUN /var/lang/bin/python3 -m pip install --upgrade pip
RUN pip install easyocr 
RUN pip install numpy

CMD ["lambda_function.lambda_handler"]
```

아래와 같이 S3로 부터 이미지 정보를 읽은 후에, target 언어로 영어(en)과 한국어(ko)를 지정하고 easyocr에 분석을 요청합니다. 얻어진 결과를 parsing하여 용도에 맞게 활용합니다. 상세한 내용은 [lambda_function.py](https://github.com/kyopark2014/korean-ocr/blob/main/lambda-easy-ocr/lambda_function.py)을 참조합니다. 

```python
image_obj = s3_client.get_object(Bucket = bucketName, Key = key)

image_content = image_obj['Body'].read()
image = Image.open(io.BytesIO(image_content))
image_np = np.array(image)
target_languages = ["en","ko"]

reader = easyocr.Reader(
    target_languages,
    model_storage_directory = '/tmp',
    user_network_directory = '/tmp',
    download_enabled = True,
    gpu = False
)
results = reader.readtext(image_np)
```

### AWS CDK로 인프라 구현하기

[CDK 구현 코드](./cdk-easy-ocr-lambda/README.md)에서는 Typescript로 인프라를 정의하는 방법에 대해 상세히 설명하고 있습니다.

## 직접 실습 해보기

### 사전 준비 사항

이 솔루션을 사용하기 위해서는 사전에 아래와 같은 준비가 되어야 합니다.

- [AWS Account 생성](https://repost.aws/ko/knowledge-center/create-and-activate-aws-account)


### CDK를 이용한 인프라 설치

[인프라 설치](./deployment.md)에 따라 CDK로 인프라 설치를 진행합니다. 



## 실행결과

- [ocr-eng.jpeg](https://github.com/kyopark2014/korean-ocr/blob/main/result/ocr-eng.jpeg)에 대한 결과는 아래와 같습니다.

![ocr-eng.jpeg](https://github.com/kyopark2014/korean-ocr/assets/52392004/54c9c20a-5429-45d5-a429-877e07544951)

얻어진 text는 아래와 같습니다.

```text
A few days later: Ariel asked Calista and Laurel to meet her by the water: 66 1 have presents for you both" Ariel said. She handed the girls two brand-new necklaces made from star shell 'They're beautiful" Laurel breathed. "Thank Princess Ariel" Calista said. Ariel smiled When 1 was wearing the star' shell, it was like carrying part of the ocean with me. Now you two can always carry a of your adventure with you wherever you 0 pieces. you, piece 80."
```

- [test 이미지](https://github.com/aws-samples/detect-text-lambda-with-easyocr/blob/main/img/test.jpeg)로 테스트 했을때의 결과는 아래와 같습니다.

[ocr_result.json](https://github.com/kyopark2014/korean-ocr/blob/main/result/ocr_test.json)와 같이 추출된 결과는 전체 텍스트와 함께 추출된 문장의 위치 정보를 포함합니다. 여기서 텍스트만 표시하면 아래와 같습니다.

```text
"개봉선 자이스 렌즈 와이프 렌즈 표면의 먼지와 얼륙올 흔적 없이 부드럽게 닦아주는 일회용 티슷 안전기준 안전확인대상생활화학제품 틀 드 확인 표시사항 l 신고번호: 제 FB21-02-0531호 품목: 제거제  제품명: 자이스 렌즈 와이프 주요물질: 정제수, 2-프로판올 제조연월: 제품 하단 LOT 번호 앞 네 자리 참조 제조자 제조국: 프로스벤아이언쓰Prosben Inc) 중국 수입자, 주소, 연락처: 갈자이스비전코리아 서울시 승파구 법원로 135, 1201호(02-2252-1001)"
```



## TrOCR

[TrOCR for Korean Language (PoC)](https://huggingface.co/daekeun-ml/ko-trocr-base-nsmc-news-chatbot)을 테스트 (예정)

