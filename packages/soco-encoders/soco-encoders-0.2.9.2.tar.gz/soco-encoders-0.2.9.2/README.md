# Encoders
A library of neural encoders to convert any types of data into embeddings, dense or sparse. 


## Build a package
    python setup.py bdist_wheel
    twine upload dist/*

## Use Locally
    model = EncoderLoader.load_model('pretrain-models', <model_id>, use_gpu=True, region='cn')
    model.encode(['I am a good man'], show_progress_bar=True, batch_size=batch_size,)

## Use as RESTful API
Start a server
    
    uvicorn soco_encoders.http.main:app --host 0.0.0.0 --port 8000 --workers 4

Start a client

    res = requests.post(url='http://localhost:8000/encoder/v1/encode',
                          json={
                              "model_id": model_id,
                              "text": [x1] * batch_size,
                              'batch_size': batch_size,
                              "mode": "default",
                              "kwargs": {}
                          })

## Use as GRPC API
Start a server
    
    python -m soco_encoders.grpc.server --host 0.0.0.0 --port 8000 --workers 4
    
Start a client
       
       check out example in bench_grpc.py