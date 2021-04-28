from flask.cli import AppGroup
from blueprints.images.models.image import Image
from google.cloud import storage
import pandas
import csv


def register_commands(app):
    """
    Register useful commands to execute.
    """

    cloud_cli = AppGroup("cloud")

    @cloud_cli.command("add")
    def add_images():
        """
        add images url from cloud
        """
        client = storage.Client.from_service_account_json("service_account.json")
        bucket = client.get_bucket("shopify0")

        dataset = bucket.list_blobs()

        for index, blob in enumerate(dataset):
            splits = blob.name.split("/")
            if len(splits) != 4:
                continue
            pokemon_name = splits[2]
            image_name = splits[3]
            url = f"https://storage.googleapis.com/shopify0/dataset/{pokemon_name}/{image_name}"
            Image(url=url, tag=pokemon_name).save()
            if index % 100 == 0:
                print(index)

    @cloud_cli.command("test")
    def test():
        """
        test mongodb connection
        """
        Image(url="https://google.com", tag="test").save()

    @cloud_cli.command("generate_csv")
    def generate_csv():
        """
        Create csv files for training
        """
        client = storage.Client.from_service_account_json("service_account.json")
        bucket = client.get_bucket("shopify1")

        dataset = bucket.list_blobs()
        data = []
        for blob in dataset:
            splits = blob.name.split("/")
            if len(splits) != 4:
                continue
            label = splits[2]
            file_name = f"gs://shopify1/dataset/{label}/{splits[3]}"

            if file_name[-4:] == ".png" or file_name[-4:] == ".jpg":
                data.append((file_name, label))

        df = pandas.DataFrame(data)
        df.to_csv("all_data.csv", header=False, index=False)

    @cloud_cli.command("generate_names")
    def get_pokemon_names():
        """
        Generate pokemon names
        """
        names = set()
        with open("all_data.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                label = row[1]
                names.add(label)

        with open("names.txt", "w+") as f:
            f.write(",".join(names))

    app.cli.add_command(cloud_cli)
