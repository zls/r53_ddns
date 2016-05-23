Quickstart
==========

This utility can be used to create your own dynamic dns service using Amazon's
Route53.

Environment Variables

* R53_ZONE_ID: The zone id of the resource record you wish to change in the
  following format '/hostedzone/<zone_id>'
* R53_A_NAME: The name of the A resource record type you would like to set. If
  this record does not exist it will be created, otherwise it will be updated.
* AWS_ACCESS_KEY_ID: AWS credentials, will also use ~/.aws/credentials file.
* AWS_SECRET_ACCESS_KEY: AWS credentials, will also use ~/.aws/credentials file.
* R53_TTL (optional): The TTL of the record being updated. Defaults to 360 seconds.
* R53_IPURL (optional): Url to retrieve IP from. Returned IP must be plaintext and free of
  any characters aside from the IP address. Defaults to https://ip.appspot.com.


Example:

    AWS_ACCESS_KEY_ID='<aws_access_key_id>' \
    AWS_SECRET_ACCESS_KEY='<aws_secret_access_key>' \
    R53_ZONE_ID='/hostedzone/<zone_id>' \
    R53_A_NAME='dyn.example.com' \
    python r53_ddns.py
