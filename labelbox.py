mport json
import uuid

import labelbox as lb

# credentials
API_KEY = ""
client = lb.Client(API_KEY)

# get the dataset from Catalog by catalog ID
dataset = client.get_dataset("")

# get the project from Annotate
project = client.get_project("")


def sample_generator(data, batch_size=500):
    """
    Generator function that yields a batch of samples at a time.

    Parameters:
    data (list): List of input samples.
    batch_size (int): The number of samples to include in each batch.

    Yields:
    tuple: A tuple of the batch data and labels.
    """
    n_batches = len(data) // batch_size

    for i in range(n_batches):
        start = i * batch_size
        end = start + batch_size
        batch_data = data[start:end]

        # yield a tuple of batch data and labels
        yield batch_data

    # Yield the remaining samples in the final batch
    if len(data) % batch_size != 0:
        yield data[n_batches * batch_size:]


def import_labels(batch_idx, objects):
    global_keys = []
    label_ndjson_method2 = []

    for obj in objects:  # list of files, uploading first 500 samples
        template = {}
        bbox_template = []
        vid = obj["vid"]
        for name, bbox in zip(obj["cls"], obj["bbox"]):
            template["name"] = name
            template["bbox"] = {
                "top": bbox[0],
                "left": bbox[1],
                "height": bbox[2],
                "width": bbox[3]
            }
            bbox_template.append(template.copy())

        global_keys.append(vid)

        for annotation in bbox_template:
            annotation.update({'dataRow': {'globalKey': vid}})
            label_ndjson_method2.append(annotation)

    # create a batch and upload the labels
    batch = project.create_batch(
        f"batch_{batch_idx}",  # name of the batch
        global_keys=global_keys,  # a list of global keys, data rows, or data row ids
        priority=1  # priority between 1-5
    )
    print("Batch", batch)

    upload_job = lb.MALPredictionImport.create_from_objects(
        client=client,
        project_id=project.uid,
        name="mal_job" + str(uuid.uuid4()),
        predictions=label_ndjson_method2
    )

    print("Errors:", upload_job.errors)


if __name__ == '__main__':
    with open("upload_to_labelbox.json", "r") as f:
        objects = json.load(f)

    for idx, data in enumerate(sample_generator(objects)):
        import_labels(idx, data)

    print("Importing completed successfully!")
