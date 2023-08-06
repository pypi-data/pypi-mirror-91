# py_aws_helper

Helper for AWS services like S3 written in python...

### Prerequisites

 •	IAM user with read access to S3 and its secret keys<br>
 •	AWS CLI configured with the secret keys<br>
 •	Python, Pip<br>


### Getting Started

Assuming that the [configuration of AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) using the corresponding secret keys of the IAM user, set up your environment using Python and virtualenv and install the library using pip once the virtual  environment is activated:

`$ pip install py-aws-helper`

### Using s3objectfinder

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sample snippet:

	from py_aws_helper import s3objectfinder
    
	bucket=''     # provide bucket name
	file_name=''    # provide file name
	output = s3objectfinder.find_object(bucket=bucket, file_name=file_name)
	print('Total objects fetched: ', output['total_objects_fetched'])
	print('Total objects matched: ', output['total_objects_matched'])
	print('Matched keys list: ', output['matched_keys'])

#### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Other arguments:

The s3object finder module can take in two additional paramters other than the bucket and file_name namely , "prefix" and "delimiter" whose default values have been initiated as empty strings.

The corresponding documentation for populating the "prefix" and "delimiter" arguments can be found [here](https://docs.aws.amazon.com/AmazonS3/latest/dev/ListingKeysHierarchy.html)
