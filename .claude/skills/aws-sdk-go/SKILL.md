---
name: aws-sdk-go
description: Use this skill whenever the user wants to work with AWS SDK for Go v2, including configuring credentials and regions, constructing service clients, calling AWS API operations, handling responses and errors, using paginators and waiters, uploading and downloading S3 objects, setting up authentication, implementing retries and timeouts, using middleware and interceptors, or working with AWS service utilities like RDS, CloudFront, and EC2 metadata.
---

## Setup

### Install the SDK

```go
go get github.com/aws/aws-sdk-go-v2
```

### Get AWS Credentials

1. Create an AWS account and generate access keys
2. Obtain your Access Key ID and Secret Access Key from the AWS console
3. Store credentials securely using one of the supported methods (see Configuration section)

## Quick Start

### Load Configuration

```go
package main

import (
	"context"
	"github.com/aws/aws-sdk-go-v2/config"
)

func main() {
	// Load default configuration (reads from shared config/credentials files, environment, IAM roles)
	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		panic(err)
	}
	// Use cfg to create service clients
}
```

### Create a Service Client

```go
import "github.com/aws/aws-sdk-go-v2/service/s3"

// Using loaded config
client := s3.NewFromConfig(cfg)

// Or create directly
client := s3.New(s3.Options{})
```

### Call an Operation

```go
import (
	"context"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

result, err := client.GetObject(context.TODO(), &s3.GetObjectInput{
	Bucket: aws.String("my-bucket"),
	Key:    aws.String("my-object"),
})
if err != nil {
	// Handle error
}
// Use result
```

## Configuration

### Specifying the AWS Region

**Environment Variable:**
```bash
export AWS_REGION=us-east-1
```

**Programmatically:**
```go
cfg, err := config.LoadDefaultConfig(context.TODO(),
	config.WithRegion("us-west-2"),
)
```

### Specifying Credentials

**IAM Roles (Recommended for EC2):**
Credentials are automatically loaded from EC2 instance metadata service.

**Shared Credentials File (~/.aws/credentials):**
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY

[profile-name]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

**Environment Variables:**
```bash
export AWS_ACCESS_KEY_ID=your-access-key
export AWS_SECRET_ACCESS_KEY=your-secret-key
```

**Programmatically:**
```go
import "github.com/aws/aws-sdk-go-v2/credentials"

cfg, err := config.LoadDefaultConfig(context.TODO(),
	config.WithCredentialsProvider(credentials.NewStaticCredentialsProvider(
		"access-key", "secret-key", "session-token",
	)),
)
```

### Configure HTTP Client

```go
import "net/http"

cfg, err := config.LoadDefaultConfig(context.TODO(),
	config.WithHTTPClient(&http.Client{
		Timeout: 30 * time.Second,
	}),
)
```

### Set Timeouts

```go
import "github.com/aws/aws-sdk-go-v2/aws"

result, err := client.GetObject(context.TODO(),
	&s3.GetObjectInput{
		Bucket: aws.String("bucket"),
		Key:    aws.String("key"),
	},
	func(o *s3.Options) {
		o.APIOptions = append(o.APIOptions, func(stack *middleware.Stack) error {
			return nil // Configure timeouts here
		})
	},
)
```

## Using the SDK

### Calling Service Operations

Pass parameters using the operation's input type:

```go
result, err := client.PutObject(context.TODO(), &s3.PutObjectInput{
	Bucket: aws.String("my-bucket"),
	Key:    aws.String("my-key"),
	Body:   bytes.NewReader([]byte("data")),
})
if err != nil {
	panic(err)
}
```

### Handling Responses

```go
result, err := client.GetObject(context.TODO(), &s3.GetObjectInput{
	Bucket: aws.String("bucket"),
	Key:    aws.String("key"),
})
if err != nil {
	// Handle error
	panic(err)
}
defer result.Body.Close()

// Access response fields
body, _ := ioutil.ReadAll(result.Body)
```

### Handling Errors

```go
import (
	"github.com/aws/smithy-go"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

result, err := client.GetObject(context.TODO(), &s3.GetObjectInput{
	Bucket: aws.String("bucket"),
	Key:    aws.String("key"),
})
if err != nil {
	var noKey *types.NoSuchKey
	if errors.As(err, &noKey) {
		// Handle NoSuchKey error
	}
	var ae smithy.APIError
	if errors.As(err, &ae) {
		// Handle any API error
		fmt.Printf("code: %s, message: %s\n", ae.ErrorCode(), ae.ErrorMessage())
	}
}
```

### Retrieving Request Identifiers

```go
import "github.com/aws/aws-sdk-go-v2/aws/protocol/restxml"

result, err := client.GetObject(context.TODO(), &s3.GetObjectInput{
	Bucket: aws.String("bucket"),
	Key:    aws.String("key"),
})
if err != nil {
	var ae smithy.APIError
	if errors.As(err, &ae) {
		if meta := ae.(*smithy.OperationError).Err.(smithy.RequestIDRetriever); meta != nil {
			fmt.Println("RequestID:", meta.GetRequestID())
		}
	}
}
```

### Using Paginators

```go
import "github.com/aws/aws-sdk-go-v2/service/s3"

paginator := s3.NewListObjectsV2Paginator(client, &s3.ListObjectsV2Input{
	Bucket: aws.String("my-bucket"),
})

for paginator.HasMorePages() {
	page, err := paginator.NextPage(context.TODO())
	if err != nil {
		panic(err)
	}
	for _, obj := range page.Contents {
		fmt.Println(*obj.Key)
	}
}
```

### Using Waiters

```go
waiter := s3.NewBucketExistsWaiter(client)
err := waiter.Wait(context.TODO(), &s3.HeadBucketInput{
	Bucket: aws.String("my-bucket"),
}, 5*time.Minute)
if err != nil {
	panic(err)
}
```

## S3 Operations

### Upload an Object

```go
result, err := client.PutObject(context.TODO(), &s3.PutObjectInput{
	Bucket: aws.String("my-bucket"),
	Key:    aws.String("my-key"),
	Body:   bytes.NewReader(data),
})
if err != nil {
	panic(err)
}
fmt.Println("Upload successful:", result.ETag)
```

### Download an Object

```go
result, err := client.GetObject(context.TODO(), &s3.GetObjectInput{
	Bucket: aws.String("my-bucket"),
	Key:    aws.String("my-key"),
})
if err != nil {
	panic(err)
}
defer result.Body.Close()

data, _ := ioutil.ReadAll(result.Body)
fmt.Println("Downloaded:", string(data))
```

## Utilities

### S3 Transfer Managers

For efficient handling of large objects and concurrent transfers:

```go
import "github.com/aws/aws-sdk-go-v2/feature/s3/manager"

uploader := manager.NewUploader(client)
result, err := uploader.Upload(context.TODO(), &s3.PutObjectInput{
	Bucket: aws.String("my-bucket"),
	Key:    aws.String("my-key"),
	Body:   file,
})

downloader := manager.NewDownloader(client)
numBytes, err := downloader.Download(context.TODO(), buffer, &s3.GetObjectInput{
	Bucket: aws.String("my-bucket"),
	Key:    aws.String("my-key"),
})
```

### RDS IAM Authentication

```go
import "github.com/aws/aws-sdk-go-v2/feature/rds/auth"

authToken, err := auth.BuildAuthToken(context.TODO(), endpoint, region, dbUser, credentials)
```

### CloudFront URL Signer

```go
import "github.com/aws/aws-sdk-go-v2/feature/cloudfront/sign"

signer := sign.NewURLSigner(keyID, privateKey)
signedURL, err := signer.SignURL(url, time.Now().Add(24*time.Hour))
```

### EC2 Instance Metadata

```go
import "github.com/aws/aws-sdk-go-v2/feature/ec2/imds"

client := imds.New(cfg)
result, err := client.GetMetadata(context.TODO(), &imds.GetMetadataInput{
	Path: "iam/security-credentials/",
})
```

## Middleware and Interceptors

### Custom Middleware

```go
import "github.com/aws/smithy-go/middleware"

func customMiddleware(stack *middleware.Stack) error {
	stack.Build.Add(middleware.BuilderFunc(func(ctx context.Context, in middleware.BuildInput) (middleware.BuildOutput, error) {
		// Custom logic
		return middleware.CallNextHandler(ctx, in)
	}), middleware.After)
	return nil
}

cfg, _ := config.LoadDefaultConfig(context.TODO())
client := s3.NewFromConfig(cfg)
client.APIOptions = append(client.APIOptions, customMiddleware)
```

## References

- [AWS SDK for Go v2 Developer Guide](https://docs.aws.amazon.com/sdk-for-go/)
- [AWS SDK for Go v2 API Reference](https://pkg.go.dev/github.com/aws/aws-sdk-go-v2)
- [S3 Operations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/)
- [IAM Authentication](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [CloudFront Utilities](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/)
- [EC2 Instance Metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html)