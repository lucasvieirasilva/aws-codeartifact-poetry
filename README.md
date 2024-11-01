# AWS CodeArtifact Poetry

## SonarCloud Status

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=bugs)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=lucasvieirasilva_aws-codeartifact-poetry)

AWS CodeArtifact Poetry CLI is a CLI designed to perform Poetry login with AWS CodeArtifact Private PyPi.

## Motivation

AWS CodeArtifact is a fully managed artifact repository service that makes it easy for organizations of any size to securely store, publish, and share software packages used in their development process. CodeArtifact supports npm, Maven, and Python packaging formats and allows you to easily integrate with your existing build and deployment workflows.

However, the AWS CLI does not support Poetry login with AWS CodeArtifact Private PyPi. This CLI was created to solve this problem.

## Install

`pip install aws-codeartifact-poetry`

## Usage

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

### Login

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

## Contributing

- See our [Contributing Guide](CONTRIBUTING.md)

## Change Log

- See our [Change Log](CHANGELOG.md)
