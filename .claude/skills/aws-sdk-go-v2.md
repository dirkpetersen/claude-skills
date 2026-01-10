---
name: aws-sdk-go-v2
description: AWS SDK for Go v2 - build Go applications using AWS services with automatic credential management, retries, paginators, and S3 transfer utilities
---

# AWS SDK for Go v2

Build Go applications that interact with AWS services. The SDK handles authentication, retries, error handling, and provides utilities like S3 transfer managers.

## Requirements

Go 1.23+

## Installation

```bash
go mod init myapp
go get github.com/aws/aws-sdk-go-v2/config
go get github.com/aws/aws-sdk-go-v2/service/s3  # or other services
```

## Quick Start

```go
package main

import (
    "context"
    "fmt"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/s3"
)

func main() {
    cfg, err := config.LoadDefaultConfig(context.TODO())
    if err != nil {
        panic(err)
    }

    client := s3.NewFromConfig(cfg)

    result, err := client.ListBuckets(context.TODO(), &s3.ListBucketsInput{})
    if err != nil {
        panic(err)
    }

    for _, bucket := range result.Buckets {
        fmt.Println(*bucket.Name)
    }
}
```

## Configuration

### Region

**Environment variable:**
```bash
export AWS_REGION=us-west-2
```

**Programmatic:**
```go
cfg, err := config.LoadDefaultConfig(context.TODO(),
    config.WithRegion("us-west-2"))
```

### Credential Chain (searched in order)

1. Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`
2. Web Identity Token: `AWS_WEB_IDENTITY_TOKEN_FILE`
3. Shared credentials: `~/.aws/credentials`
4. Shared config: `~/.aws/config`
5. ECS task IAM role
6. EC2 instance IAM role

### Using Profiles

```bash
export AWS_PROFILE=my-profile
```

```go
cfg, err := config.LoadDefaultConfig(context.TODO(),
    config.WithSharedConfigProfile("my-profile"))
```

### Static Credentials (development only)

```go
import "github.com/aws/aws-sdk-go-v2/credentials"

cfg, err := config.LoadDefaultConfig(context.TODO(),
    config.WithCredentialsProvider(credentials.NewStaticCredentialsProvider(
        "AKID", "SECRET", "TOKEN")))
```

### SSO Login

```bash
aws sso login --profile my-sso-profile
```

```go
cfg, err := config.LoadDefaultConfig(context.TODO(),
    config.WithSharedConfigProfile("my-sso-profile"))
```

## Calling Operations

```go
import "github.com/aws/aws-sdk-go-v2/aws"

result, err := client.GetObject(context.TODO(), &s3.GetObjectInput{
    Bucket: aws.String("my-bucket"),
    Key:    aws.String("my-key"),
})
if err != nil {
    // handle error
}
defer result.Body.Close()  // ALWAYS close io.ReadCloser responses
```

### Override Client Options Per-Call

```go
result, err := client.GetObject(context.TODO(), input, func(o *s3.Options) {
    o.Region = "eu-west-1"
})
```

## Error Handling

```go
import (
    "errors"
    "github.com/aws/smithy-go"
)

var apiErr smithy.APIError
if errors.As(err, &apiErr) {
    fmt.Printf("Code: %s, Message: %s\n", apiErr.ErrorCode(), apiErr.ErrorMessage())
}

// Get request ID for AWS support
import "github.com/aws/aws-sdk-go-v2/aws/middleware"
requestID, _ := middleware.GetRequestIDMetadata(result.ResultMetadata)
```

## Paginators

Automatically iterate through paginated results:

```go
paginator := s3.NewListObjectsV2Paginator(client, &s3.ListObjectsV2Input{
    Bucket: aws.String("my-bucket"),
})

for paginator.HasMorePages() {
    page, err := paginator.NextPage(context.TODO())
    if err != nil {
        break
    }
    for _, obj := range page.Contents {
        fmt.Println(*obj.Key)
    }
}
```

## Waiters

Wait for resource state changes:

```go
waiter := s3.NewBucketExistsWaiter(client)
err := waiter.Wait(context.TODO(), &s3.HeadBucketInput{
    Bucket: aws.String("my-bucket"),
}, 5*time.Minute)
```

## S3 Transfer Manager

High-performance multipart uploads/downloads:

```go
import "github.com/aws/aws-sdk-go-v2/feature/s3/manager"

// Upload
uploader := manager.NewUploader(client)
_, err := uploader.Upload(context.TODO(), &s3.PutObjectInput{
    Bucket: aws.String("my-bucket"),
    Key:    aws.String("my-key"),
    Body:   file,
})

// Download
downloader := manager.NewDownloader(client)
_, err := downloader.Download(context.TODO(), file, &s3.GetObjectInput{
    Bucket: aws.String("my-bucket"),
    Key:    aws.String("my-key"),
})
```

## Timeouts

Use context for request timeouts:

```go
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()

result, err := client.GetObject(ctx, input)
```

## Retries

Default: 3 attempts with 20s max backoff.

```go
import "github.com/aws/aws-sdk-go-v2/aws/retry"

// Custom max attempts
cfg, err := config.LoadDefaultConfig(context.TODO(),
    config.WithRetryer(func() aws.Retryer {
        return retry.AddWithMaxAttempts(retry.NewStandard(), 5)
    }))

// Disable retries
client := s3.NewFromConfig(cfg, func(o *s3.Options) {
    o.Retryer = aws.NopRetryer{}
})
```

## Custom Endpoints

Point to local or custom endpoints:

```go
client := s3.NewFromConfig(cfg, func(o *s3.Options) {
    o.BaseEndpoint = aws.String("http://localhost:4566")
})
```

## HTTP Client Configuration

```go
import awshttp "github.com/aws/aws-sdk-go-v2/aws/transport/http"

httpClient := awshttp.NewBuildableClient().
    WithTimeout(60 * time.Second).
    WithDialerOptions(func(d *net.Dialer) {
        d.KeepAlive = 30 * time.Second
    })

cfg, err := config.LoadDefaultConfig(context.TODO(),
    config.WithHTTPClient(httpClient))
```

## Logging

```go
cfg, err := config.LoadDefaultConfig(context.TODO(),
    config.WithClientLogMode(aws.LogRetries | aws.LogRequest))
```

## Concurrency

Service clients are goroutine-safe. Use concurrently without synchronization:

```go
var wg sync.WaitGroup
for _, key := range keys {
    wg.Add(1)
    go func(k string) {
        defer wg.Done()
        client.GetObject(ctx, &s3.GetObjectInput{Bucket: bucket, Key: &k})
    }(key)
}
wg.Wait()
```

## Pointer Helpers

```go
import "github.com/aws/aws-sdk-go-v2/aws"

// Convert to pointer
bucket := aws.String("my-bucket")

// Convert from pointer (nil-safe)
name := aws.ToString(result.Name)
count := aws.ToInt32(result.Count)
```

## Common Services

| Service | Package |
|---------|---------|
| S3 | `github.com/aws/aws-sdk-go-v2/service/s3` |
| DynamoDB | `github.com/aws/aws-sdk-go-v2/service/dynamodb` |
| Lambda | `github.com/aws/aws-sdk-go-v2/service/lambda` |
| SQS | `github.com/aws/aws-sdk-go-v2/service/sqs` |
| SNS | `github.com/aws/aws-sdk-go-v2/service/sns` |
| EC2 | `github.com/aws/aws-sdk-go-v2/service/ec2` |
| IAM | `github.com/aws/aws-sdk-go-v2/service/iam` |
| Bedrock | `github.com/aws/aws-sdk-go-v2/service/bedrockruntime` |

Full list: https://pkg.go.dev/github.com/aws/aws-sdk-go-v2/service

## References

- API Reference: https://pkg.go.dev/github.com/aws/aws-sdk-go-v2
- Developer Guide: https://docs.aws.amazon.com/sdk-for-go/v2/developer-guide/
- GitHub: https://github.com/aws/aws-sdk-go-v2
