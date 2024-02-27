# AWS CDK로 인프라 구현하기

여기서는 Typescript를 이용하여 인프라를 구현합니다.

S3를 정의합니다.

```typescript
const s3Bucket = new s3.Bucket(this, `storage-${projectName}`, {
    bucketName: bucketName,
    blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
    removalPolicy: cdk.RemovalPolicy.DESTROY,
    autoDeleteObjects: true,
    publicReadAccess: false,
    versioned: false,
    cors: [
        {
            allowedHeaders: ['*'],
            allowedMethods: [
                s3.HttpMethods.POST,
                s3.HttpMethods.PUT,
            ],
            allowedOrigins: ['*'],
        },
    ],
});
```

S3에 "upload.html" 파일을 복사합니다. 관련 명령어를 output에 출력해서 편리하게 이용합니다.
```typescript
new s3Deploy.BucketDeployment(this, `upload-HTML-for-${projectName}`, {
    sources: [s3Deploy.Source.asset("../html/")],
    destinationBucket: s3Bucket,
});

new cdk.CfnOutput(this, 'HtmlUpdateCommend', {
    value: 'aws s3 cp ../html/ ' + 's3://' + s3Bucket.bucketName + '/ --recursive',
    description: 'copy commend for web pages',
});
```

CloudFront를 정의합니다. 젒고하는 URL 정보를 아래와 같이 Output에 출력합니다.

```typescript
const distribution = new cloudFront.Distribution(this, `cloudfront-for-${projectName}`, {
    defaultBehavior: {
        origin: new origins.S3Origin(s3Bucket),
        allowedMethods: cloudFront.AllowedMethods.ALLOW_ALL,
        cachePolicy: cloudFront.CachePolicy.CACHING_DISABLED,
        viewerProtocolPolicy: cloudFront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    },
    priceClass: cloudFront.PriceClass.PRICE_CLASS_200,
});

new cdk.CfnOutput(this, `WebUrl-for-${projectName}`, {
    value: 'https://' + distribution.domainName + '/upload.html',
    description: 'The web url for upload',
}); 
```

OCR을 수행한 이력을 저장하기 위하여 DynamoDB를 설치합니다. 

```typescript
const ocrLogTableName = `db-ocr-log-for-${projectName}`;
const ocrLogDataTable = new dynamodb.Table(this, `db-ocr-log-for-${projectName}`, {
    tableName: ocrLogTableName,
    partitionKey: { name: 'request_id', type: dynamodb.AttributeType.STRING },
    sortKey: { name: 'request_time', type: dynamodb.AttributeType.STRING },
    billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    removalPolicy: cdk.RemovalPolicy.DESTROY,
});
const ocrLogIndexName = `index-type-for-${projectName}`;
ocrLogDataTable.addGlobalSecondaryIndex({ // GSI
    indexName: ocrLogIndexName,
    partitionKey: { name: 'request_id', type: dynamodb.AttributeType.STRING },
}); F
```

REST API를 처리하기 위하여 API Gateway를 정의합니다. 

```typescript
const role = new iam.Role(this, `api-role-for-${projectName}`, {
    roleName: `api-role-for-${projectName}-${region}`,
    assumedBy: new iam.ServicePrincipal("apigateway.amazonaws.com")
  });
  role.addToPolicy(new iam.PolicyStatement({
    resources: ['*'],
    actions: [
      'lambda:InvokeFunction',
      'cloudwatch:*'
    ]
  }));
  role.addManagedPolicy({
    managedPolicyArn: 'arn:aws:iam::aws:policy/AWSLambdaExecute',
  }); 

  // API Gateway
  const api = new apiGateway.RestApi(this, `api-chatbot-for-${projectName}`, {
    description: 'API Gateway for ocr',
    endpointTypes: [apiGateway.EndpointType.REGIONAL],
    binaryMediaTypes: ['application/json'], 
    deployOptions: {
      stageName: stage,

      // logging for debug
      // loggingLevel: apiGateway.MethodLoggingLevel.INFO, 
      // dataTraceEnabled: true,
    },
  });  
```

Lambda (OCR)을 정의합니다. 전체 패키지의 용량이 크므로 Container 이미지를 활용해 배포합니다. 

```typescript
const roleLambdaOCR = new iam.Role(this, `role-lambda-for-${projectName}`, {
    roleName: `role-lambda-for-${projectName}-${region}`,
    assumedBy: new iam.CompositePrincipal(
        new iam.ServicePrincipal("lambda.amazonaws.com")
    )
});
roleLambdaOCR.addManagedPolicy({
    managedPolicyArn: 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
});

// lambda - ocr
const lambdaEasyOCR = new lambda.DockerImageFunction(this, `lambda-for-${projectName}`, {
    description: 'lambda for easy ocr',
    functionName: `lambda-for-${projectName}`,
    code: lambda.DockerImageCode.fromImageAsset(path.join(__dirname, '../../lambda-easy-ocr')),
    timeout: cdk.Duration.seconds(300),
    memorySize: 10240,
    role: roleLambdaOCR,
    environment: {
        bucketName: bucketName,
        s3_prefix: s3_prefix,
        ocrLogTableName: ocrLogTableName,
    }
});
s3Bucket.grantReadWrite(lambdaEasyOCR); // permission for s3
ocrLogDataTable.grantReadWriteData(lambdaEasyOCR); // permission for dynamo

// POST method - ocr
const resourceNameOcr = "ocr";
const ocr = api.root.addResource(resourceNameOcr);
ocr.addMethod('POST', new apiGateway.LambdaIntegration(lambdaEasyOCR, {
    passthroughBehavior: apiGateway.PassthroughBehavior.WHEN_NO_TEMPLATES,
    credentialsRole: role,
    integrationResponses: [{
        statusCode: '200',
    }],
    proxy: false,
}), {
    methodResponses: [
        {
            statusCode: '200',
            responseModels: {
                'application/json': apiGateway.Model.EMPTY_MODEL,
            },
        }
    ]
});

// cloudfront setting  
distribution.addBehavior("/ocr", new origins.RestApiOrigin(api), {
    cachePolicy: cloudFront.CachePolicy.CACHING_DISABLED,
    allowedMethods: cloudFront.AllowedMethods.ALLOW_ALL,
    viewerProtocolPolicy: cloudFront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
});    
```

Presigned URL을 얻기 위해 Lambda(Upload)를 정의합니다. 

```typescript
// Lambda - Upload
const lambdaUpload = new lambda.Function(this, `lambda-upload-for-${projectName}`, {
    runtime: lambda.Runtime.NODEJS_16_X,
    functionName: `lambda-upload-for-${projectName}`,
    code: lambda.Code.fromAsset("../lambda-upload"),
    handler: "index.handler",
    timeout: cdk.Duration.seconds(10),
    environment: {
        bucketName: s3Bucket.bucketName,
        s3_prefix: s3_prefix
    }
});
s3Bucket.grantReadWrite(lambdaUpload);

// POST method - upload
const resourceNameUpload = "upload";
const upload = api.root.addResource(resourceNameUpload);
upload.addMethod('POST', new apiGateway.LambdaIntegration(lambdaUpload, {
    passthroughBehavior: apiGateway.PassthroughBehavior.WHEN_NO_TEMPLATES,
    credentialsRole: role,
    integrationResponses: [{
        statusCode: '200',
    }],
    proxy: false,
}), {
    methodResponses: [
        {
            statusCode: '200',
            responseModels: {
                'application/json': apiGateway.Model.EMPTY_MODEL,
            },
        }
    ]
});

// cloudfront setting  
distribution.addBehavior("/upload", new origins.RestApiOrigin(api), {
    cachePolicy: cloudFront.CachePolicy.CACHING_DISABLED,
    allowedMethods: cloudFront.AllowedMethods.ALLOW_ALL,
    viewerProtocolPolicy: cloudFront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
});    
```

OCR 결과를 조회하기 위한 Query API를 Lambda (Query)를 이용해 구현합니다. 

```typescript
// Lambda - queryResult
const lambdaQueryResult = new lambda.Function(this, `lambda-query-for-${projectName}`, {
    runtime: lambda.Runtime.NODEJS_16_X,
    functionName: `lambda-query-for-${projectName}`,
    code: lambda.Code.fromAsset("../lambda-query"),
    handler: "index.handler",
    timeout: cdk.Duration.seconds(60),
    logRetention: logs.RetentionDays.ONE_DAY,
    environment: {
        tableName: ocrLogTableName,
        indexName: ocrLogIndexName
    }
});
ocrLogDataTable.grantReadWriteData(lambdaQueryResult); // permission for dynamo

// POST method - query
const query = api.root.addResource("query");
query.addMethod('POST', new apiGateway.LambdaIntegration(lambdaQueryResult, {
    passthroughBehavior: apiGateway.PassthroughBehavior.WHEN_NO_TEMPLATES,
    credentialsRole: role,
    integrationResponses: [{
        statusCode: '200',
    }],
    proxy: false,
}), {
    methodResponses: [
        {
            statusCode: '200',
            responseModels: {
                'application/json': apiGateway.Model.EMPTY_MODEL,
            },
        }
    ]
});

// cloudfront setting for api gateway    
distribution.addBehavior("/query", new origins.RestApiOrigin(api), {
    cachePolicy: cloudFront.CachePolicy.CACHING_DISABLED,
    allowedMethods: cloudFront.AllowedMethods.ALLOW_ALL,
    viewerProtocolPolicy: cloudFront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
});
```
