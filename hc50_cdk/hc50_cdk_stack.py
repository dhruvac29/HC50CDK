from aws_cdk import (
    aws_s3 as _s3,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
    aws_apigatewayv2 as _apigatewayv2,
    aws_apigatewayv2_integrations as _integrations,
    Stack,
    Duration,
    RemovalPolicy,
)
from constructs import Construct


class Hc50CdkStack(Stack):
    """
    Hc50CdkStack is a CDK stack that sets up S3 buckets, Lambda functions, and API Gateway integrations
    for handling file uploads, presigned URLs, and model analysis.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        """
        Initialize the Hc50CdkStack.

        :param scope: The scope in which this stack is defined.
        :param construct_id: The ID of the stack.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(scope, construct_id, **kwargs)

        # Create the S3 bucket
        self.create_hc50_s3_bucket()

        # Create Lambda function and API Gateway for presigned URLs
        self.create_s3_presigned_lambda_and_apigateway()

        # Create Lambda function and API Gateway for model analysis
        self.create_model_lambda_and_apigateway()

    def create_hc50_s3_bucket(self):
        """
        Create an S3 bucket with CORS configuration and a removal policy.
        """
        self.hc50_bucket = _s3.Bucket(
            self,
            "hc50BucketId",
            bucket_name="hc50-bucket",
            removal_policy=RemovalPolicy.DESTROY,  # Automatically delete bucket when stack is deleted
            cors=[
                _s3.CorsRule(
                    allowed_headers=["*"],  # Allow all headers
                    allowed_methods=[
                        _s3.HttpMethods.GET,
                        _s3.HttpMethods.PUT,
                        _s3.HttpMethods.HEAD,
                    ],  # Allow GET, PUT, and HEAD methods
                    allowed_origins=["*"],  # Allow all origins
                )
            ],
        )

    def create_model_lambda_and_apigateway(self):
        """
        Create a Lambda function for model analysis and an API Gateway to expose it.
        """
        # Define the Lambda function
        self.prediction_lambda = _lambda.DockerImageFunction(
            scope=self,
            id="hc50ModelLambda",
            function_name="hc50-model-lambda",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="hc50_model_lambda"  # Directory containing Dockerfile and code
            ),
            environment={
                "BUCKET_NAME": self.hc50_bucket.bucket_name
            },  # Pass bucket name to Lambda
            architecture=_lambda.Architecture.ARM_64,  # Use ARM 64 architecture
            timeout=Duration.seconds(300),  # Set timeout to 300 seconds
            memory_size=1024,  # Set memory size to 1024 MB
        )

        # Grant read permissions on the S3 bucket to the Lambda function
        self.hc50_bucket.grant_read(self.prediction_lambda)

        # Define the API Gateway and link it to the Lambda function
        self.model_api = _apigateway.LambdaRestApi(
            self,
            "hc50ModelApi",
            rest_api_name="hc50-model-api",
            handler=self.prediction_lambda,
            proxy=False,  # Disable proxy integration
        )

        # Create an "analyze" resource and add POST method
        analyze = self.model_api.root.add_resource("analyze")
        analyze.add_method("POST")

        analyze.add_cors_preflight(
            allow_origins=["*"],
            allow_methods=["POST"],
            allow_headers=["Content-Type", "Authorization"],
        )

    def create_s3_presigned_lambda_and_apigateway(self):
        """
        Create a Lambda function for generating S3 presigned URLs and an API Gateway to expose it.
        """
        # Define the Lambda function for presigned URLs
        self.presigned_lambda = _lambda.Function(
            self,
            "PresignedUrlFunction",
            function_name="hc50-presigned-lambda",
            runtime=_lambda.Runtime.PYTHON_3_9,  # Use Python 3.9 runtime
            handler="lambda_function.handler",  # Define handler function
            code=_lambda.Code.from_asset(
                "hc50_presigned_lambda"
            ),  # Code from directory
            environment={
                "BUCKET_NAME": self.hc50_bucket.bucket_name
            },  # Pass bucket name to Lambda
        )

        # Grant write permissions on the S3 bucket to the Lambda function
        self.hc50_bucket.grant_write(self.presigned_lambda)

        # Define the HTTP API and CORS settings
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
                ],  # Allow these HTTP methods
                allow_headers=["*"],  # Allow all headers
                allow_origins=["*"],  # Allow all origins
            ),
        )

        # Integrate the Lambda function with the HTTP API
        self.presigned_api_integration = _integrations.HttpLambdaIntegration(
            "presignedApiIntegration", handler=self.presigned_lambda
        )

        # Add routes to the HTTP API
        self.presigned_api.add_routes(
            path="/presigned",  # Define the path
            methods=[_apigatewayv2.HttpMethod.GET],  # Allow GET method
            integration=self.presigned_api_integration,  # Set the integration
        )
