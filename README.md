# 한국어 OCR

## EasyOCR

[EasyOCR](https://github.com/JaidedAI/EasyOCR), [PaddleOC](https://github.com/PaddlePaddle/PaddleOCR)와 같은 Open Source OCR을 활용하여 API를 구현하고자 합니다. 여기서는 [detect-text-lambda-with-easyocr(AWS Sample)](https://github.com/aws-samples/detect-text-lambda-with-easyocr)을 참조하여, Lambda로 한국어가 지원되는 OCR를 생성하고자 합니다.

- [데모](https://www.jaided.ai/easyocr/)에서는 2MB 파일도 처리할 수 없다고 나오나 실제로는 제한은 없습니다.

- [detect-text-lambda-with-easyocr(AWS Sample)](https://github.com/aws-samples/detect-text-lambda-with-easyocr)에 따라, 10240MB Lambda에서 테스트할 경우에 500KB 미만의 이미지 처리 시, 1분 내외 소요가 된다고 합니다.

### 실행결과


- 아래 이미지에 대한 결과는 아래와 같습니다.

![noname](https://github.com/kyopark2014/korean-ocr/assets/52392004/54c9c20a-5429-45d5-a429-877e07544951)


```java
detected_texts_join:  A few days later: Ariel asked Calista and Laurel to meet her by the water: 66 1 have presents for you both" Ariel said. She handed the girls two brand-new necklaces made from star shell 'They're beautiful" Laurel breathed. "Thank Princess Ariel" Calista said. Ariel smiled When 1 was wearing the star' shell, it was like carrying part of the ocean with me. Now you two can always carry a of your adventure with you wherever you 0 pieces. you, piece 80."
```

- [test 이미지](https://github.com/aws-samples/detect-text-lambda-with-easyocr/blob/main/img/test.jpeg)로 테스트 했을때의 결과는 아래와 같습니다.

하나의 문장으로 추출한 결과입니다.

```java
"DetectedText":"개봉선 자이스 렌즈 와이프 렌즈 표면의 먼지와 얼륙올 흔적 없이 부드럽게 닦아주는 일회용 티슷 안전기준 안전확인대상생활화학제품 틀 드 확인 표시사항 l 신고번호: 제 FB21-02-0531호 품목: 제거제  제품명: 자이스 렌즈 와이프 주요물질: 정제수, 2-프로판올 제조연월: 제품 하단 LOT 번호 앞 네 자리 참조 제조자 제조국: 프로스벤아이언쓰Prosben Inc) 중국 수입자, 주소, 연락처: 갈자이스비전코리아 서울시 승파구 법원로 135, 1201호(02-2252-1001)"
```

전체 결과는 아래와 같습니다.

```java
{
   "DetectedText":"개봉선 자이스 렌즈 와이프 렌즈 표면의 먼지와 얼륙올 흔적 없이 부드럽게 닦아주는 일회용 티슷 안전기준 안전확인대상생활화학제품 틀 드 확인 표시사항 l 신고번호: 제 FB21-02-0531호 품목: 제거제  제품명: 자이스 렌즈 와이프 주요물질: 정제수, 2-프로판올 제조연월: 제품 하단 LOT 번호 앞 네 자리 참조 제조자 제조국: 프로스벤아이언쓰Prosben Inc) 중국 수입자, 주소, 연락처: 갈자이스비전코리아 서울시 승파구 법원로 135, 1201호(02-2252-1001)",
   "DetectedResults":[
      {
         "Text":"개봉선",
         "TopLeft":{
            "x":553,
            "y":67
         },
         "TopRight":{
            "x":663,
            "y":67
         },
         "BottomRight":{
            "x":663,
            "y":111
         },
         "BottomLeft":{
            "x":553,
            "y":111
         }
      },
      {
         "Text":"자이스 렌즈 와이프 렌즈 표면의 먼지와 얼륙올",
         "TopLeft":{
            "x":117,
            "y":101
         },
         "TopRight":{
            "x":1067,
            "y":101
         },
         "BottomRight":{
            "x":1067,
            "y":163
         },
         "BottomLeft":{
            "x":117,
            "y":163
         }
      },
      {
         "Text":"흔적 없이 부드럽게 닦아주는 일회용 티슷",
         "TopLeft":{
            "x":121,
            "y":151
         },
         "TopRight":{
            "x":935,
            "y":151
         },
         "BottomRight":{
            "x":935,
            "y":213
         },
         "BottomLeft":{
            "x":121,
            "y":213
         }
      },
      {
         "Text":"안전기준",
         "TopLeft":{
            "x":228,
            "y":342
         },
         "TopRight":{
            "x":384,
            "y":342
         },
         "BottomRight":{
            "x":384,
            "y":396
         },
         "BottomLeft":{
            "x":228,
            "y":396
         }
      },
      {
         "Text":"안전확인대상생활화학제품",
         "TopLeft":{
            "x":496,
            "y":346
         },
         "TopRight":{
            "x":1051,
            "y":346
         },
         "BottomRight":{
            "x":1051,
            "y":414
         },
         "BottomLeft":{
            "x":496,
            "y":414
         }
      },
      {
         "Text":"틀",
         "TopLeft":{
            "x":1095,
            "y":297
         },
         "TopRight":{
            "x":1133,
            "y":297
         },
         "BottomRight":{
            "x":1133,
            "y":381
         },
         "BottomLeft":{
            "x":1095,
            "y":381
         }
      },
      {
         "Text":"드",
         "TopLeft":{
            "x":1098,
            "y":382
         },
         "TopRight":{
            "x":1130,
            "y":382
         },
         "BottomRight":{
            "x":1130,
            "y":414
         },
         "BottomLeft":{
            "x":1098,
            "y":414
         }
      },
      {
         "Text":"확인",
         "TopLeft":{
            "x":222,
            "y":386
         },
         "TopRight":{
            "x":388,
            "y":386
         },
         "BottomRight":{
            "x":388,
            "y":486
         },
         "BottomLeft":{
            "x":222,
            "y":486
         }
      },
      {
         "Text":"표시사항",
         "TopLeft":{
            "x":497,
            "y":400
         },
         "TopRight":{
            "x":690,
            "y":400
         },
         "BottomRight":{
            "x":690,
            "y":468
         },
         "BottomLeft":{
            "x":497,
            "y":468
         }
      },
      {
         "Text":"l",
         "TopLeft":{
            "x":1051,
            "y":304
         },
         "TopRight":{
            "x":1137,
            "y":304
         },
         "BottomRight":{
            "x":1137,
            "y":549
         },
         "BottomLeft":{
            "x":1051,
            "y":549
         }
      },
      {
         "Text":"신고번호: 제 FB21-02-0531호",
         "TopLeft":{
            "x":89,
            "y":575
         },
         "TopRight":{
            "x":731,
            "y":575
         },
         "BottomRight":{
            "x":731,
            "y":635
         },
         "BottomLeft":{
            "x":89,
            "y":635
         }
      },
      {
         "Text":"품목: 제거제",
         "TopLeft":{
            "x":89,
            "y":629
         },
         "TopRight":{
            "x":349,
            "y":629
         },
         "BottomRight":{
            "x":349,
            "y":689
         },
         "BottomLeft":{
            "x":89,
            "y":689
         }
      },
      {
         "Text":"",
         "TopLeft":{
            "x":1055,
            "y":537
         },
         "TopRight":{
            "x":1139,
            "y":537
         },
         "BottomRight":{
            "x":1139,
            "y":747
         },
         "BottomLeft":{
            "x":1055,
            "y":747
         }
      },
      {
         "Text":"제품명: 자이스 렌즈 와이프",
         "TopLeft":{
            "x":85,
            "y":681
         },
         "TopRight":{
            "x":659,
            "y":681
         },
         "BottomRight":{
            "x":659,
            "y":743
         },
         "BottomLeft":{
            "x":85,
            "y":743
         }
      },
      {
         "Text":"주요물질: 정제수, 2-프로판올",
         "TopLeft":{
            "x":84,
            "y":734
         },
         "TopRight":{
            "x":711,
            "y":734
         },
         "BottomRight":{
            "x":711,
            "y":798
         },
         "BottomLeft":{
            "x":84,
            "y":798
         }
      },
      {
         "Text":"제조연월: 제품 하단 LOT 번호 앞 네 자리 참조",
         "TopLeft":{
            "x":83,
            "y":785
         },
         "TopRight":{
            "x":1065,
            "y":785
         },
         "BottomRight":{
            "x":1065,
            "y":852
         },
         "BottomLeft":{
            "x":83,
            "y":852
         }
      },
      {
         "Text":"제조자 제조국: 프로스벤아이언쓰Prosben Inc) 중국",
         "TopLeft":{
            "x":83,
            "y":838
         },
         "TopRight":{
            "x":1137,
            "y":838
         },
         "BottomRight":{
            "x":1137,
            "y":907
         },
         "BottomLeft":{
            "x":83,
            "y":907
         }
      },
      {
         "Text":"수입자, 주소,",
         "TopLeft":{
            "x":84,
            "y":896
         },
         "TopRight":{
            "x":358,
            "y":896
         },
         "BottomRight":{
            "x":358,
            "y":950
         },
         "BottomLeft":{
            "x":84,
            "y":950
         }
      },
      {
         "Text":"연락처: 갈자이스비전코리아",
         "TopLeft":{
            "x":375,
            "y":893
         },
         "TopRight":{
            "x":973,
            "y":893
         },
         "BottomRight":{
            "x":973,
            "y":953
         },
         "BottomLeft":{
            "x":375,
            "y":953
         }
      },
      {
         "Text":"서울시 승파구 법원로 135, 1201호(02-2252-1001)",
         "TopLeft":{
            "x":81,
            "y":938
         },
         "TopRight":{
            "x":1129,
            "y":938
         },
         "BottomRight":{
            "x":1129,
            "y":1004
         },
         "BottomLeft":{
            "x":81,
            "y":1004
         }
      }
   ]
}
```

## TrOCR

[TrOCR for Korean Language (PoC)](https://huggingface.co/daekeun-ml/ko-trocr-base-nsmc-news-chatbot)을 deploy하고 성능을 데모로 보여주고자합니다. (추후... )

