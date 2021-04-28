"""
utility library for communicating with auto-ml rest api
"""

from google.cloud import automl

import config as c


def predict(content):
    """
    Predict labels
    """
    project_id = c.PROJECT_ID
    model_id = c.MODEL_ID
    location = c.LOCATION

    predictor = automl.PredictionServiceClient.from_service_account_json(
        "service_account.json"
    )

    model_full_id = automl.AutoMlClient.model_path(project_id, location, model_id)
    image = automl.Image(image_bytes=content)
    payload = automl.ExamplePayload(image=image)

    request = automl.PredictRequest(name=model_full_id, payload=payload)
    response = predictor.predict(request=request)

    pred_sum = 0
    prediction = {}
    for result in response.payload:
        prediction[result.display_name] = result.classification.score
        pred_sum += result.classification.score

    if pred_sum != 0:
        for pred in prediction:
            prediction[pred] /= pred_sum

    return prediction
