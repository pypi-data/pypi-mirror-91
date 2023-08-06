===============================
py_aws_helper
===============================

Helper for AWS services like S3 written in python...

Prerequisites
---------------
 
 * IAM user with read access to S3 and its secret keys
 * AWS CLI configured with the secret keys
 * Python, Pip

Getting Started
------------------

Assuming that the `configuration of AWS CLI <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html>`__ using the corresponding secret keys of the IAM user, set up your environment using Python and virtualenv and install the library using pip once the virtual  environment is activated:

.. code-block:: sh

    $ pip install py-aws-helper

Using s3objectfinder
------------------------

Sample snippet:

.. code-block:: python

    >>> from py_aws_helper import s3objectfinder
    >>> bucket=''     # provide bucket name
    >>> file_name=''    # provide file name
    >>> output = s3objectfinder.find_object(bucket=bucket, file_name=file_name)
    >>> print('Total objects fetched: ', output['total_objects_fetched'])
    >>> print('Total objects matched: ', output['total_objects_matched'])
    >>> for key in output['matched_keys']:
            print('Key: ', key)


Other arguments:

The s3objectfinder module can take in two additional paramters other than the bucket and file_name namely , "prefix" and "delimiter" whose default values have been initiated as empty strings.

The corresponding documentation for populating the "prefix" and "delimiter" arguments can be found `here <https://docs.aws.amazon.com/AmazonS3/latest/dev/ListingKeysHierarchy.html>`__
