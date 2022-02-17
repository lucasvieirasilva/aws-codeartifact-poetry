# CLI Reference

## help

```text
Usage: aws-codeartifact-poetry [OPTIONS] COMMAND [ARGS]...

  AWS CodeArtifact Poetry CLI.

Options:
  --loglevel [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Log level.  [default: WARNING]
  --log-file TEXT                 Log file name
  --help                          Show this message and exit.

Commands:
  login  Login to AWS CodeArtifact
```

## login

```text
Usage: aws-codeartifact-poetry login [OPTIONS]

  Login to AWS CodeArtifact

Options:
  --repository TEXT    Your CodeArtifact repository name  [required]
  --domain TEXT        Your CodeArtifact domain name  [required]
  --domain-owner TEXT  The AWS account ID that owns your CodeArtifact domain
                       [required]
  --profile TEXT       AWS Profile.
  --region TEXT        AWS Region name  [default: us-east-1]
  --help               Show this message and exit.
```
