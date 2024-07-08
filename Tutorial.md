# AWS CDK Tutorial for Our HC50 Model

## Overview

The `Hc50CdkStack` class is part of an AWS Cloud Development Kit (CDK) application. This class defines a stack that sets up AWS resources like S3 buckets, Lambda functions, and API Gateway integrations. The purpose of this stack is to handle file uploads, generate pre-signed URLs for S3, and perform model analysis using Lambda functions.

### Generate Pre-Signed URL
Before setting up the CDK for S3, Lambda, and API Gateway, we need to create a pre-signed URL Lambda function. This function will handle file uploads and generate a unique URL, which will be sent to our Lambda function to run the ML model.

*   This code sets up a function to generate a special URL that allows someone to upload a CSV file to a specific location in an S3 bucket.
*   It ensures each file uploaded has a unique name.
*   It returns this URL to the requester, allowing them to upload the file within a 5-minute window.

```
s3_client = boto3.client("s3")
```

*   This line initializes an S3 client using the `boto3` library, which will allow the code to interact with the S3 service.
```
bucket_name = os.environ["BUCKET_NAME"]
```
*   This retrieves the name of the S3 bucket (storage space in AWS) from the environment variables set in the system where this code is running.

### The Main Function

```
def handler(event, context):
    """
    Lambda function handler to generate a presigned URL for uploading a CSV file to S3.

    :param event: The event dictionary containing the request data.
    :param context: The context in which the function is called.
    :return: A response dictionary containing the presigned URL and unique key.
    """
```

*   This defines a function named `handler`. In AWS Lambda (a service that runs code in response to events), this function is automatically called when the event it is configured for occurs.
*   **event**: Contains data about the request.
*   **context**: Provides information about the function's execution environment.

### Generating a Unique Key

```
unique_key = f"{uuid.uuid4()}.csv"
```

*   This line generates a unique identifier using `uuid.uuid4()` and appends `.csv` to it. This ensures that each file uploaded has a unique name.

### Generating a Pre-signed URL

```
presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_name, "Key": unique_key, "ContentType": "text/csv"},
        ExpiresIn=300,  # URL expiration time in seconds (5 minutes)
        HttpMethod="PUT",
    )
```
*   This line generates a pre-signed URL, which is a special URL that allows someone to upload a file directly to S3 without needing to have AWS credentials.
*   **"put_object"**: This specifies the type of operation (uploading a file).
*   **Params**: These are the parameters for the operation.
*   **"Bucket"**: The name of the S3 bucket where the file will be uploaded.
*   **"Key"**: The unique key (filename) for the file.
*   **"ContentType"**: Specifies the type of file (CSV in this case).
*   **ExpiresIn=300**: The URL will expire in 300 seconds (5 minutes).
*   **HttpMethod="PUT"**: Specifies that the HTTP method for this URL is PUT, which means it's used for uploading a file.

### Returning the Response

```
return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"url": presigned_url, "key": unique_key}),
    }
```

*   This returns a response back to the requester.
*   **statusCode: 200**: Indicates that the request was successful.
*   **headers**: Specifies that the response content is JSON.
*   **body**: Contains the pre-signed URL and the unique key in JSON format.

# HC50 CDK Main Function

### Initialization
```
class Hc50CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.create_hc50_s3_bucket()
        self.create_s3_presigned_lambda_and_apigateway()
        self.create_model_lambda_and_apigateway()
```
   **Line by Line Explanation**:
*   `class Hc50CdkStack(Stack):` - Defines the `Hc50CdkStack` class that inherits from the `Stack` class provided by the AWS CDK.
*   `def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:` - The initialization method for the stack. It takes `scope`, `construct_id`, and additional keyword arguments.
*   `super().__init__(scope, construct_id, **kwargs)` - Calls the parent class (`Stack`) constructor to initialize the stack.
*   `self.create_hc50_s3_bucket()` - Calls the method to create the S3 bucket.
*   `self.create_s3_presigned_lambda_and_apigateway()` - Calls the method to create the Lambda function and API Gateway for pre-signed URLs.
*   `self.create_model_lambda_and_apigateway()` - Calls the method to create the Lambda function and API Gateway for model analysis.
    
   **Edit Instructions**:
*   To modify the stack initialization, such as adding more resources or changing the initialization logic, edit the `__init__` method.
*   Add or remove method calls as needed to customize the resources being created.

### S3 Bucket Creation

```
def create_hc50_s3_bucket(self):
    self.hc50_bucket = _s3.Bucket(
        self,
        "hc50BucketId",
        bucket_name="hc50-bucket",
        removal_policy=RemovalPolicy.DESTROY,
        cors=[
            _s3.CorsRule(
                allowed_headers=["*"],
                allowed_methods=[
                    _s3.HttpMethods.GET,
                    _s3.HttpMethods.PUT,
                    _s3.HttpMethods.HEAD,
                ],
                allowed_origins=["*"],
            )
        ],
    )
```
   **Line by Line Explanation**:
*   `def create_hc50_s3_bucket(self):` - Defines a method to create an S3 bucket.
*   `self.hc50_bucket = _s3.Bucket(` - Creates a new S3 bucket and assigns it to `self.hc50_bucket`.
*   `self, "hc50BucketId",` - The CDK scope and the logical ID for the bucket within the stack.
*   `bucket_name="hc50-bucket",` - Specifies the name of the S3 bucket.
*   `removal_policy=RemovalPolicy.DESTROY,` - Configures the bucket to be automatically deleted when the stack is deleted.
*   `cors=[` - Defines CORS (Cross-Origin Resource Sharing) rules for the bucket.
*   `_s3.CorsRule(` - Creates a CORS rule.
*   `allowed_headers=["*"],` - Allows all headers in CORS requests.
*   `allowed_methods=[` - Allows specific HTTP methods for CORS requests.
*   `_s3.HttpMethods.GET,` - Allows GET method.
*   `_s3.HttpMethods.PUT,` - Allows PUT method.
*   `_s3.HttpMethods.HEAD,` - Allows HEAD method.
*   `allowed_origins=["*"],` - Allows all origins to access the bucket.

   **Edit Instructions**:
*   To change bucket properties such as the name, CORS settings, or removal policy, modify the parameters in the `_s3.Bucket` constructor.
*   Update the `bucket_name` parameter to change the bucket's name.
*   Adjust the `removal_policy` to change how the bucket is handled when the stack is deleted.
*   Modify the CORS rules to change allowed headers, methods, or origins.

### Lambda Function and API Gateway for Model Analysis

```
def create_model_lambda_and_apigateway(self):
    self.prediction_lambda = _lambda.DockerImageFunction(
        scope=self,
        id="hc50ModelLambda",
        function_name="hc50-model-lambda",
        code=_lambda.DockerImageCode.from_image_asset(
            directory="hc50_model_lambda"
        ),
        environment={
            "BUCKET_NAME": self.hc50_bucket.bucket_name
        },
        architecture=_lambda.Architecture.ARM_64,
        timeout=Duration.seconds(300),
        memory_size=1024,
    )

    self.hc50_bucket.grant_read(self.prediction_lambda)

    self.model_api = _apigateway.LambdaRestApi(
        self,
        "hc50ModelApi",
        rest_api_name="hc50-model-api",
        handler=self.prediction_lambda,
        proxy=False,
    )

    analyze = self.model_api.root.add_resource("analyze")
    analyze.add_method("POST")

    analyze.add_cors_preflight(
        allow_origins=["*"],
        allow_methods=["POST"],
        allow_headers=["Content-Type", "Authorization"],
    )
```

   **Line by Line Explanation**:
*   `def create_model_lambda_and_apigateway(self):` - Defines a method to create a Lambda function and an API Gateway for model analysis.
*   `self.prediction_lambda = _lambda.DockerImageFunction(` - Creates a Docker-based Lambda function for model analysis.
*   `scope=self,` - The CDK scope.
*   `id="hc50ModelLambda",` - The logical ID for the Lambda function.
*   `function_name="hc50-model-lambda",` - Specifies the name of the Lambda function.
*   `code=_lambda.DockerImageCode.from_image_asset(` - Specifies the location of the Docker image for the Lambda function.
*   `directory="hc50_model_lambda"` - Directory containing the Dockerfile and code.
*   `environment={` - Defines environment variables for the Lambda function.
*   `"BUCKET_NAME": self.hc50_bucket.bucket_name` - Passes the bucket name as an environment variable.
*   `architecture=_lambda.Architecture.ARM_64,` - Specifies the architecture for the Lambda function.
*   `timeout=Duration.seconds(300),` - Sets the timeout for the Lambda function to 300 seconds.
*   `memory_size=1024,` - Sets the memory size for the Lambda function to 1024 MB.
*   `self.hc50_bucket.grant_read(self.prediction_lambda)` - Grants the Lambda function read permissions on the S3 bucket.
*   `self.model_api = _apigateway.LambdaRestApi(` - Creates an API Gateway linked to the Lambda function.
*   `self, "hc50ModelApi",` - The CDK scope and the logical ID for the API Gateway.
*   `rest_api_name="hc50-model-api",` - Specifies the name of the API Gateway.
*   `handler=self.prediction_lambda,` - Links the Lambda function as the handler for the API Gateway.
*   `proxy=False,` - Disables proxy integration.
*   `analyze = self.model_api.root.add_resource("analyze")` - Creates an "analyze" resource in the API Gateway.
*   `analyze.add_method("POST")` - Adds a POST method to the "analyze" resource.
*   `analyze.add_cors_preflight(` - Adds CORS preflight settings to the "analyze" resource.
*   `allow_origins=["*"],` - Allows all origins.
*   `allow_methods=["POST"],` - Allows the POST method.
*   `allow_headers=["Content-Type", "Authorization"],` - Allows specific headers.
   
   **Edit Instructions**:
*   To modify the Lambda function configuration, change the parameters in `_lambda.DockerImageFunction`.
*   Update the `directory` parameter to change the location of the Dockerfile and code.
*   Adjust the `environment` dictionary to add or modify environment variables.
*   Change the `architecture`, `timeout`, or `memory_size` parameters to update the Lambda function's configuration.
*   To update API Gateway settings, adjust the `_apigateway.LambdaRestApi` and resource/method definitions.
*   Modify the CORS settings to change allowed origins, methods, or headers.

### Lambda Function and API Gateway for Presigned URLs

```
def create_s3_presigned_lambda_and_apigateway(self):
    self.presigned_lambda = _lambda.Function(
        self,
        "PresignedUrlFunction",
        function_name="hc50-presigned-lambda",
        runtime=_lambda.Runtime.PYTHON_3_9,
        handler="lambda_function.handler",
        code=_lambda.Code.from_asset("hc50_presigned_lambda"),
        environment={
            "BUCKET_NAME": self.hc50_bucket.bucket_name
        },
    )

    self.hc50_bucket.grant_write(self.presigned_lambda)

    self.presigned_api = _apigatewayv2.HttpApi(
        self,
        "hc50PresignedApi",
        api_name="hc50-presigned-api",
        cors_preflight=_apigatewayv2.CorsPreflightOptions(
            allow_methods=[
                _apigatewayv2.CorsHttpMethod.GET,
                _apigatewayv2.CorsHttpMethod.POST,
                _apigatewayv2.CorsHttpMethod.DELETE,
                _apigatewayv2.CorsHttpMethod.OPTIONS,
            ],
            allow_headers=["*"],
            allow_origins=["*"],
        ),
    )

    self.presigned_api_integration = _integrations.HttpLambdaIntegration(
        "presignedApiIntegration", handler=self.presigned_lambda
    )

    self.presigned_api.add_routes(
        path="/presigned",
        methods=[_apigatewayv2.HttpMethod.GET],
        integration=self.presigned_api_integration,
    )
```

   **Line by Line Explanation**:
*   `def create_s3_presigned_lambda_and_apigateway(self):` - Defines a method to create a Lambda function and an HTTP API Gateway for generating pre-signed URLs.
*   `self.presigned_lambda = _lambda.Function(` - Creates a Lambda function for generating pre-signed URLs.
*   `"PresignedUrlFunction",` - The logical ID for the Lambda function.
*   `function_name="hc50-presigned-lambda",` - Specifies the name of the Lambda function.
*   `runtime=_lambda.Runtime.PYTHON_3_9,` - Specifies the runtime for the Lambda function.
*   `handler="lambda_function.handler",` - Specifies the handler function.
*   `code=_lambda.Code.from_asset("hc50_presigned_lambda"),` - Specifies the location of the Lambda function code.
*   `environment={` - Defines environment variables for the Lambda function.
*   `"BUCKET_NAME": self.hc50_bucket.bucket_name` - Passes the bucket name as an environment variable.
*   `self.hc50_bucket.grant_write(self.presigned_lambda)` - Grants the Lambda function write permissions on the S3 bucket.
*   `self.presigned_api = _apigatewayv2.HttpApi(` - Creates an HTTP API Gateway linked to the Lambda function.
*   `self, "hc50PresignedApi",` - The CDK scope and the logical ID for the API Gateway.
*   `api_name="hc50-presigned-api",` - Specifies the name of the API Gateway.
*   `cors_preflight=_apigatewayv2.CorsPreflightOptions(` - Adds CORS preflight settings to the API Gateway.
*   `allow_methods=[` - Allows specific HTTP methods.
*   `_apigatewayv2.CorsHttpMethod.GET,` - Allows GET method.
*   `_apigatewayv2.CorsHttpMethod.POST,` - Allows POST method.
*   `_apigatewayv2.CorsHttpMethod.DELETE,` - Allows DELETE method.
*   `_apigatewayv2.CorsHttpMethod.OPTIONS,` - Allows OPTIONS method.
*   `allow_headers=["*"],` - Allows all headers.
*   `allow_origins=["*"],` - Allows all origins.
*   `self.presigned_api_integration = _integrations.HttpLambdaIntegration(` - Creates an integration between the HTTP API Gateway and the Lambda function.
*   `"presignedApiIntegration", handler=self.presigned_lambda` - Specifies the integration ID and the Lambda function handler.
*   `self.presigned_api.add_routes(` - Adds routes to the HTTP API Gateway.
*   `path="/presigned",` - Defines the path for the routes.
*   `methods=[_apigatewayv2.HttpMethod.GET],` - Allows the GET method for the routes.
*   `integration=self.presigned_api_integration,` - Specifies the integration for the routes.

   **Edit Instructions**:
*   To modify the Lambda function for pre-signed URLs, update the parameters in `_lambda.Function`.
*   Change the `runtime` or `handler` parameters to update the Lambda function's runtime or handler function.
*   Adjust the `environment` dictionary to add or modify environment variables.
*   To update the HTTP API settings, modify the `_apigatewayv2.HttpApi` and route definitions.
*   Change the CORS settings to update allowed methods, headers, or origins.

## Summary

*   The `Hc50CdkStack` class sets up an S3 bucket, Lambda functions, and API Gateway integrations for file uploads, pre-signed URLs, and model analysis.
  
*   **To edit the stack**:
*   Modify the `__init__` method to change stack initialization logic.
*   Update the `create_hc50_s3_bucket` method to change S3 bucket configurations.
*   Change the `create_model_lambda_and_apigateway` method to adjust the model analysis Lambda function and its API Gateway.
*   Modify the `create_s3_presigned_lambda_and_apigateway` method to update the presigned URLs Lambda function and its API Gateway
