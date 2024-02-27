# 한국어 OCR

## EasyOCR

[EasyOCR](https://github.com/JaidedAI/EasyOCR), [PaddleOC](https://github.com/PaddlePaddle/PaddleOCR)와 같은 Open Source OCR을 활용하여 API를 구현하고자 합니다. 여기서는 [detect-text-lambda-with-easyocr(AWS Sample)](https://github.com/aws-samples/detect-text-lambda-with-easyocr)을 참조하여, Lambda로 한국어가 지원되는 OCR를 생성하고자 합니다.

- [데모](https://www.jaided.ai/easyocr/)에서는 가벼운 테스트가 가능합니다.

- [detect-text-lambda-with-easyocr(AWS Sample)](https://github.com/aws-samples/detect-text-lambda-with-easyocr)에 따라, 10240MB Lambda에서 테스트할 경우에 500KB 미만의 이미지 처리 시, 1분 내외 소요가 된다고 합니다.

### 실행결과

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

