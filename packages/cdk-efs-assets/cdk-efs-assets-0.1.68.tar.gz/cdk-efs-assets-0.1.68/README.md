[![NPM version](https://badge.fury.io/js/cdk-efs-assets.svg)](https://badge.fury.io/js/cdk-efs-assets)
[![PyPI version](https://badge.fury.io/py/cdk-efs-assets.svg)](https://badge.fury.io/py/cdk-efs-assets)
![Release](https://github.com/pahud/cdk-efs-assets/workflows/Release/badge.svg)

# cdk-efs-assets

CDK construct library to populate Amazon EFS assets from Github or S3.

# `GithubSourceSync`

The `GithubSourceSync` deploys your Amazon EFS assets from specified Github repository.

## Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_efs_assets import GithubSourceSync

app = App()

env = {
    "region": process.env.CDK_DEFAULT_REGION ?? AWS_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = Stack(app, "testing-stack", env=env)

vpc = ec2.Vpc.from_lookup(stack, "Vpc", is_default=True)

fs = efs.FileSystem(stack, "Filesystem",
    vpc=vpc,
    removal_policy=RemovalPolicy.DESTROY
)

efs_access_point = fs.add_access_point("EfsAccessPoint",
    path="/demo",
    create_acl={
        "owner_gid": "1001",
        "owner_uid": "1001",
        "permissions": "0755"
    },
    posix_user={
        "uid": "1001",
        "gid": "1001"
    }
)

# create the one-time sync from Github repository to Amaozn EFS
GithubSourceSync(stack, "GithubSourceSync",
    repository="https://github.com/pahud/cdk-efs-assets.git",
    efs_access_point=efs_access_point,
    runs_after=[fs.mount_targets_available],
    vpc=vpc
)
```

# `S3ArchiveSync`

The `S3ArchiveSync` deploys your Amazon EFS assets from a specified zip archive file stored in S3. The extracted contents will be placed into the root directory of the access point.

If the `syncOnUpdate` property is set to `true` (defaults to `true`), then the specified zip file path will be monitored, and if a new object is uploaded to the path, then it will resync the data to EFS. Note that to use this functionality, you must have a CloudTrail Trail in your account that captures the desired S3 write data event.

*WARNING*: The contents of the access point will be removed before extracting the zip file.

## Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_efs_assets import S3ArchiveSync

app = App()

env = {
    "region": process.env.CDK_DEFAULT_REGION ?? AWS_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = Stack(app, "testing-stack", env=env)

vpc = ec2.Vpc.from_lookup(stack, "Vpc", is_default=True)

fs = efs.FileSystem(stack, "Filesystem",
    vpc=vpc,
    removal_policy=RemovalPolicy.DESTROY
)

efs_access_point = fs.add_access_point("EfsAccessPoint",
    path="/demo",
    create_acl={
        "owner_gid": "1001",
        "owner_uid": "1001",
        "permissions": "0755"
    },
    posix_user={
        "uid": "1001",
        "gid": "1001"
    }
)

bucket = Bucket.from_bucket_name(self, "Bucket", "demo-bucket")

# Will sync initial data from compressed S3 archive to EFS, and resync if the zip file in S3 changes
S3ArchiveSync(self, "S3ArchiveSync",
    bucket=bucket,
    zip_file_path="folder/foo.zip",
    vpc=vpc,
    efs_access_point=efs_access_point,
    runs_after=[fs.mount_targets_available]
)
```

# `S3SourceSync`

TBD
