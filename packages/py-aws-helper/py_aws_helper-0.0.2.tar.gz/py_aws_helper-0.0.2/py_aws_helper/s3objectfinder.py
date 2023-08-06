import logging
import boto3

s3_client = boto3.client('s3')


def find_object(bucket, file_name, prefix='', delimiter=''):
    """
    Function to iteratively call the ListObjects API of S3 under a given bucket, prefix and delimiter.
    :param bucket: bucket name
    :param file_name: file name to find
    :param prefix: prefix under the bucket to restrict the search
    :param delimiter: group objects based on delimiter
    :return: dictionary containing total count of objects fetched and matched along with the list of matched keys
    """
    marker = ''
    total_objects_fetched = 0
    total_objects_matched = 0
    matched_keys = []

    while True:
        # Gets all prefixes under provided prefix
        get_prefixes = s3_client.list_objects(
            Bucket=bucket,
            Prefix=prefix,
            Delimiter=delimiter,
            Marker=marker
        )

        try:
            total_objects_fetched += len(get_prefixes['Contents'])
        except KeyError:
            # If no objects are returned, 'Contents' attribute will not be returned
            return ({'total_objects_fetched': total_objects_fetched,
                     'total_objects_matched': 0,
                     'matched_keys': []})

        logging.info('Processing fetched objects...')
        for key_dict in get_prefixes['Contents']:
            if file_name == list(key_dict['Key'].split('/'))[-1]:
                total_objects_matched += 1
                matched_keys.append(key_dict['Key'])
                logging.info('Matched object: ', key_dict['Key'])

        if get_prefixes['IsTruncated']:
            marker = get_prefixes['NextMarker']
            logging.info('Fetching more objects from S3...')
        else:
            logging.info('End of processing...')
            logging.info('Total objects fetched: ', total_objects_fetched)
            logging.info('Total objects matched: ', total_objects_matched)
            logging.info('Printing matched keys...')
            for matched_key in matched_keys:
                logging.info('Key: ', matched_key)
            logging.info('Matched keys: ', total_objects_matched)
            if len(matched_keys) == 0:
                return ({'total_objects_fetched': total_objects_fetched,
                         'total_objects_matched': 0,
                         'matched_keys': []})
            else:
                return ({'total_objects_fetched': total_objects_fetched,
                         'total_objects_matched': total_objects_matched,
                         'matched_keys': matched_keys})
