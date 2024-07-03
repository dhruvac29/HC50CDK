# aws-cli

### Requirements

The AWS-CLI package works on Python versions:

-   3.8.x and greater
-   3.9.x and greater
-   3.10.x and greater
-   3.11.x and greater
-   3.12.x and greater

### Installation

Installation of the AWS CLI and its dependencies use a range of
packaging features provided by `pip` and `setuptools`. To ensure smooth
installation, it\'s recommended to use:

-   `pip`: 9.0.2 or greater
-   `setuptools`: 36.2.0 or greater

The safest way to install the AWS CLI is to use
[pip](https://pip.pypa.io/en/stable/) in a `virtualenv`:

    $ python -m pip install awscli

or, if you are not installing in a `virtualenv`, to install globally:

    $ sudo python -m pip install awscli

or for your user:

    $ python -m pip install --user awscli

If you have the aws-cli package installed and want to upgrade to the
latest version, you can run:

    $ python -m pip install --upgrade awscli

This will install the aws-cli package as well as all dependencies.

On macOS, if you see an error regarding the version of `six` that came
with `distutils` in El Capitan, use the `--ignore-installed` option:

    $ sudo python -m pip install awscli --ignore-installed six

On Linux and Mac OS, the AWS CLI can be installed using a [bundled
installer](https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html#install-linux-bundled).
The AWS CLI can also be installed on Windows via an [MSI
Installer](https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html#msi-on-windows).

If you want to run the `develop` branch of the AWS CLI, see the
[Development Version](CONTRIBUTING.md#cli-development-version) section
of the contributing guide.

See the
[installation](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv1.html)
section of the AWS CLI User Guide for more information.

### Configuration

Before using the AWS CLI, you need to configure your AWS credentials.
You can do this in several ways:

-   Configuration command
-   Environment variables
-   Shared credentials file
-   Config file
-   IAM Role

The quickest way to get started is to run the `aws configure` command:

    $ aws configure
    AWS Access Key ID: MYACCESSKEY
    AWS Secret Access Key: MYSECRETKEY
    Default region name [us-west-2]: us-west-2
    Default output format [None]: json

To use environment variables, do the following:

    $ export AWS_ACCESS_KEY_ID=<access_key>
    $ export AWS_SECRET_ACCESS_KEY=<secret_key>

To use the shared credentials file, create an INI formatted file like
this:

    [default]
    aws_access_key_id=MYACCESSKEY
    aws_secret_access_key=MYSECRETKEY

    [testing]
    aws_access_key_id=MYACCESSKEY
    aws_secret_access_key=MYSECRETKEY

and place it in `~/.aws/credentials` (or in
`%UserProfile%\.aws/credentials` on Windows). If you wish to place the
shared credentials file in a different location than the one specified
above, you need to tell aws-cli where to find it. Do this by setting the
appropriate environment variable:

    $ export AWS_SHARED_CREDENTIALS_FILE=/path/to/shared_credentials_file

To use a config file, create an INI formatted file like this:

    [default]
    aws_access_key_id=<default access key>
    aws_secret_access_key=<default secret key>
    # Optional, to define default region for this profile.
    region=us-west-1

    [profile testing]
    aws_access_key_id=<testing access key>
    aws_secret_access_key=<testing secret key>
    region=us-west-2

and place it in `~/.aws/config` (or in `%UserProfile%\.aws\config` on
Windows). If you wish to place the config file in a different location
than the one specified above, you need to tell the AWS CLI where to find
it. Do this by setting the appropriate environment variable:

    $ export AWS_CONFIG_FILE=/path/to/config_file

As you can see, you can have multiple `profiles` defined in both the
shared credentials file and the configuration file. You can then specify
which profile to use by using the `--profile` option. If no profile is
specified the `default` profile is used.

In the config file, except for the default profile, you **must** prefix
each config section of a profile group with `profile`. For example, if
you have a profile named \"testing\" the section header would be
`[profile testing]`.

The final option for credentials is highly recommended if you are using
the AWS CLI on an EC2 instance. [IAM
Roles](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)
are a great way to have credentials installed automatically on your
instance. If you are using IAM Roles, the AWS CLI will find and use them
automatically.

In addition to credentials, a number of other variables can be
configured either with environment variables, configuration file
entries, or both. See the [AWS Tools and SDKs Shared Configuration and
Credentials Reference
Guide](https://docs.aws.amazon.com/credref/latest/refdocs/overview.html)
for more information.

For more information about configuration options, please refer to the
[AWS CLI Configuration Variables
topic](http://docs.aws.amazon.com/cli/latest/topic/config-vars.html#cli-aws-help-config-vars).
You can access this topic from the AWS CLI as well by running
`aws help config-vars`.

### Basic Commands

An AWS CLI command has the following structure:

    $ aws <command> <subcommand> [options and parameters]

For example, to list S3 buckets, the command would be:

    $ aws s3 ls

To view help documentation, use one of the following:

    $ aws help
    $ aws <command> help
    $ aws <command> <subcommand> help

To get the version of the AWS CLI:

    $ aws --version

To turn on debugging output:

    $ aws --debug <command> <subcommand>

You can read more information on the [Using the AWS
CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-using.html)
chapter of the AWS CLI User Guide.

### Command Completion

The aws-cli package includes a command completion feature for Unix-like
systems. This feature is not automatically installed so you need to
configure it manually. To learn more, read the [AWS CLI Command
completion
topic](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-completion.html).


### Now we can work on out CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

## More Resources

-   [Changelog](https://github.com/aws/aws-cli/blob/develop/CHANGELOG.rst)
-   [AWS CLI Documentation](https://docs.aws.amazon.com/cli/index.html)
-   [AWS CLI User
    Guide](https://docs.aws.amazon.com/cli/latest/userguide/)
-   [AWS CLI Command
    Reference](https://docs.aws.amazon.com/cli/latest/reference/)
-   [Amazon Web Services Discussion
    Forums](https://forums.aws.amazon.com/)
-   [AWS Support](https://console.aws.amazon.com/support/home#/)

Enjoy!
