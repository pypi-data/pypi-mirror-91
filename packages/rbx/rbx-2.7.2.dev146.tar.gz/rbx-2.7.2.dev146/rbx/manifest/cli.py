import click

from .processor import ManifestHandler, zip_images
from ..settings import AWS_BUCKET, AWS_REGION


@click.command(help='Get the manifest from a url.')
@click.argument('url')
@click.option('-f', '--filename', default='out',
              help='Name of Zip File to output.')
@click.option('-m', '--mode', type=click.Choice(['http', 'aws']), default='http',
              help='Mode of Download (http or aws).')
@click.option('-b', '--bucket', default=AWS_BUCKET,
              help='Optional bucket path')
@click.option('-r', '--region', default=AWS_REGION,
              help='Optional region')
def build_image_from_manifest(url, filename, mode, bucket, region):
    """Using the specified URL location, will retrieve, process manifest and write image to zip.

    Parameters:
        url (str):
            The location of the manifest to download and build image from.
        filename (str):
            The filename of the final zip file to generate.
        mode (str):
            If we are retrieving the manifest from http or aws.
        bucket (str):
            The name of the bucket where the file is stored.
        region (str):
            The region of the bucket where the file is stored.
    """
    if mode == 'http':
        handler = ManifestHandler()
    else:
        handler = ManifestHandler(bucket=bucket, region=region)

    image_list = handler.build_image_from_manifest(manifest_url=url)
    click.echo("Image Generated!")

    zip_images(image_list, filename=filename)
    click.echo("Image Now Available in {}.zip".format(filename))
