# Setup

You will need to install:
- Docker for [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community-1) or [MacOS](https://docs.docker.com/docker-for-mac/install/)
- Dmake: see https://github.com/deepomatic/dmake#installation.

Please use [this link](https://github.com/Deepomatic/challenge-workflow/archive/master.zip) to download the source code and do not fork the repository. Please also read all the instructions carefully. Feel free to send any question to vincent@deepomatic.com.

Then you can start the project with the API key we provided you with by email:

```
export DEEPOMATIC_API_KEY=XXX
cd challenge-workflow
dmake shell web
make
```

You can then try to access to the api via `curl http://127.0.0.1:8000/api/model/` or visit directly http://127.0.0.1:8000/api/model/.

You will get:

```json
[
    {
        "id": 1,
        "name": "interior_vs_trash",
        "kind": "CLA"
    },
    {
        "id": 2,
        "name": "furniture-v1",
        "kind": "DET"
    },
    {
        "id": 3,
        "name": "textures",
        "kind": "CLA"
    },
    {
        "id": 4,
        "name": "imagenet-inception-v3",
        "kind": "CLA"
    }
]
```

Here, `kind` is `CLA` for a classification model (it will find the main content of an image), and `DET` for a detection model (it will localize the position of objects in an image and give you their type). Please find a description of those models below.

Now, you can perform an inference (i.e. the act of running your model on an image) like this:

```bash
curl 'http://127.0.0.1:8000/api/model/4/infer/' -H 'Content-Type: application/json' --data '{"url": "https://storage.googleapis.com/dp-public/tech_challenge/415185a7-8864-40a3-991d-59760327fb6b.jpg"}'
```

or by visiting http://127.0.0.1:8000/api/model/4/infer/ and entering `{"url": "https://storage.googleapis.com/dp-public/tech_challenge/415185a7-8864-40a3-991d-59760327fb6b.jpg"}` in the "Content" text box of the "Raw data" tab. The request may take a dozen of seconds the first time while we wake up the model in our own cloud API.

You will get a result like this:

```
{
    "outputs": [
        {
            "labels": {
                "discarded": [],
                "predicted": [
                    {
                        "score": 0.893848479,
                        "label_id": 831,
                        "threshold": 0.025,
                        "label_name": "studio couch, day bed"
                    }
                ]
            }
        }
    ]
}
```

You only need to pay attention to the `predicted` field which lists all the recognized concepts in the image. In this case, the models recognized a `"studio couch, day bed"` in the image with a confidence of `0.893848479` (the confidence is between 0 and 1).

If you try the same image with the furniture model, you will also get the localization of the image. Indeed, if you run:

```bash
curl 'http://127.0.0.1:8000/api/model/2/infer/' -H 'Content-Type: application/json' --data '{"url": "https://storage.googleapis.com/dp-public/tech_challenge/415185a7-8864-40a3-991d-59760327fb6b.jpg"}'
```

or by visiting http://127.0.0.1:8000/api/model/2/infer/ and entering `{"url": "https://storage.googleapis.com/dp-public/tech_challenge/415185a7-8864-40a3-991d-59760327fb6b.jpg"}`, you should get the following. Again, it might take a dozen of seconds to respond the first time:

```json
{
    "outputs": [
        {
            "labels": {
                "discarded": [],
                "predicted": [
                    {
                        "roi": {
                            "bbox": {
                                "xmax": 0.476669759,
                                "xmin": 0.339794695,
                                "ymax": 0.444144785,
                                "ymin": 0.250198632
                            },
                            "region_id": 2
                        },
                        "score": 0.948721647,
                        "label_id": 8717,
                        "threshold": 0.692,
                        "label_name": "Cushion"
                    },
                    {
                        "roi": {
                            "bbox": {
                                "xmax": 0.595482826,
                                "xmin": 0.456722796,
                                "ymax": 0.453077972,
                                "ymin": 0.266793281
                            },
                            "region_id": 12
                        },
                        "score": 0.945338428,
                        "label_id": 8717,
                        "threshold": 0.692,
                        "label_name": "Cushion"
                    },
                    {
                        "roi": {
                            "bbox": {
                                "xmax": 0.877484739,
                                "xmin": 0.722455144,
                                "ymax": 0.486952662,
                                "ymin": 0.26641506
                            },
                            "region_id": 7
                        },
                        "score": 0.92992419,
                        "label_id": 8717,
                        "threshold": 0.692,
                        "label_name": "Cushion"
                    },
                    {
                        "roi": {
                            "bbox": {
                                "xmax": 0.97238785,
                                "xmin": 0,
                                "ymax": 0.92256397,
                                "ymin": 0.24570249
                            },
                            "region_id": 0
                        },
                        "score": 0.920165,
                        "label_id": 8722,
                        "threshold": 0.565,
                        "label_name": "Sofa"
                    },
                    {
                        "roi": {
                            "bbox": {
                                "xmax": 0.338726342,
                                "xmin": 0.140227675,
                                "ymax": 0.563713431,
                                "ymin": 0.298070401
                            },
                            "region_id": 16
                        },
                        "score": 0.789360404,
                        "label_id": 8717,
                        "threshold": 0.692,
                        "label_name": "Cushion"
                    },
                    {
                        "roi": {
                            "bbox": {
                                "xmax": 0.715462863,
                                "xmin": 0.588295937,
                                "ymax": 0.487777442,
                                "ymin": 0.271388531
                            },
                            "region_id": 186
                        },
                        "score": 0.755201042,
                        "label_id": 8717,
                        "threshold": 0.692,
                        "label_name": "Cushion"
                    }
                ]
            }
        }
    ]
}
```

This means that one `Sofa` and 5 `Cushion` have been detected. You get their coordinates in normalized coordinates (between 0 and 1): `xmin` is the left coordinate of the box, `ymin` is the top coordinate of the box. So the top-left corner of the image has coordinates (0, 0) and the bottom-right corner has coordinates (1, 1).

# Goal

The goal is to develop an API that allow the user to specify and run an inference on a workflow, i.e. a succession of models.

To be more precise, the goal is two write two endpoints. The first endpoint `/api/workflow/` will be used to create, list, delete a workflow. For that, you will need to write a new view that gives to the user the possibility to define a succesion of actions in one object:

- Is image valid (model with ID 1)?
- If yes (label `ok`):
    - Is there furniture (model with ID 2)?
    - If yes and if it has label `Sofa`:
        - What color has the sofa (model with ID 3)?

Then you need to implement an additionnal endpoint such that calling `/api/workflow/1/infer` will return JSON that is similar in essence to the examples below:

- ex1 :
    - input : https://deepomatic.com/wp-content/uploads/2019/02/logo-blanc.png
    - output: can't recognize this image

- ex2:
    - input: https://storage.googleapis.com/dp-public/tech_challenge/b688efc5-8d63-4b84-b768-2dade04e3af9.jpg

    - output:
        - the image is valid
        - items found:
            - Poster-Painting-Decoration:
                - bbox: {xmin: ..., ymin: ..., xmax: ..., ymax: ...}
            - Cushion:
                - bbox: {...}
            - Cushion:
                - bbox: {...}
            - Bed:
                - bbox: {...}

- ex3:
    - input: https://storage.googleapis.com/dp-public/tech_challenge/415185a7-8864-40a3-991d-59760327fb6b.jpg
    - output:
        - the image is valid
        - items found:
            - ...
            - ...
            - Sofa:
                - bbox: {...}
                - the sofa is red

## What is mandatory to do:

- endpoints `/api/workflow/` and `/api/workflow/{:id}/infer` need to be implemented and return JSON.
- `make test` should work.

### Steps:

- Probably write at least one new model and a new serializer to handle the workflow.
- Write a new view that gives the user the possibility to perform an inference on a workflow.
- Update the file tests.py to make it work, especially `test_workflow_run`.

### At your disposal you have:

- 3 neural network:
    - model with ID = 1: a binary classifier with two labels:
        - ok : the image is valid
        - ko: invalid image
    - model with ID = 2: a furniture detector with the following labels:
        - Sofa
        - Lamp-Luminaire
        - Shelf-Bookcase
        - TV_stand
        - Poster-Painting-Decoration
        - Table
        - Coffee_table
        - Curtains
        - Chair-Armchair
        - Cupboard-Cabinet
        - Sideboard-Commode
        - Stool
        - Carpet
        - Cushion
        - Chest
        - Vase
        - Plant
        - Bed
        - Desk
        - Clock
        - Mirror
        - Bedside_table
    - model with ID = 3: a classifier for Sofa with the following labels:
        - red
        - black
        - unkown

You can define the API that you want, the only restriction is that the API should return JSON.

### Ideas for improvements:

Those improvements are not demanded unless specifically required:

- How would you design a front-end for this API? We use Angular & Vue.js at Deepomatic, but feel free to use what ever you like.
- Async task: running many neural network calls in a web server can be long, too long for what is recommended for a healthy API. You may want to implement a task system where you inference request returns a task ID that can be used to poll for results and get the results when ready.
- Web sockets: Instead of polling the results of a task above, you could implement Websockets (e.g. with Django Channels) to push the new task results to a front-end.
- Deploy everything in production mode, e.g. with nginx (reverse proxy) and uwsgi/uvicorn/gunicorn.
- Add a user system with authentification/permissions
- Add quota per user for API calls
- ...

# Submission

Once you are happy with the results, please zip this folder and  provide us with any information needed to run your code. For example, please add a proper requirements.txt with:
Please send an archive with your solution to vincent@deepomatic.com. You will be judged on:

- the quality of your code and tests
- the self-explainability of your API
- potential improvements/bonus

Good luck ! :-)

