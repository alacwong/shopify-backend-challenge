from flask.cli import AppGroup
from blueprints.images.models.image import Image
from google.cloud import storage


def register_commands(app):
    """
    Register useful commands to execute.
    """

    cloud_cli = AppGroup('cloud')

    @cloud_cli.command('add')
    def add_images():
        """
        add images url from cloud
        """
        client = storage.Client.from_service_account_json('service_account.json')
        bucket = client.get_bucket("shopify0")

        dataset = bucket.list_blobs()

        for index, blob in enumerate(dataset):
            splits = blob.name.split('/')
            if len(splits) != 4:
                continue
            pokemon_name = splits[2]
            image_name = splits[3]
            url = f'https://storage.googleapis.com/shopify0/dataset/{pokemon_name}/{image_name}'
            Image(
                url=url,
                tag=pokemon_name
            ).save()
            if index % 100 == 0:
                print(index)

    @cloud_cli.command('test')
    def test():
        """
        test mongodb connection
        """
        Image(
            url='https://google.com',
            tag='test'
        ).save()

    app.cli.add_command(cloud_cli)
