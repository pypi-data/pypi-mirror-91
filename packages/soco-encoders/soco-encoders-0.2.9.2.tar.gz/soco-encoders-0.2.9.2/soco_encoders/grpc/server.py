import grpc
from concurrent import futures
import time
from soco_encoders.grpc.model import MyModel
import soco_encoders.grpc.embedding_pb2_grpc as embedding_pb2_grpc
import argparse
import logging

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description='Starting a GRPC server')
    parser.add_argument('--host', type=str, default='[::]')
    parser.add_argument('--port', type=int, default=50070)
    parser.add_argument('--workers', type=int, default=4)

    args = parser.parse_args()

    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=args.workers))

    # to add the defined class to the server
    embedding_pb2_grpc.add_EncoderServicer_to_server(MyModel(), server)

    # listen on port 50051
    logger.info('Starting server. Listening on port {}:{}'.format(args.host, args.port))
    server.add_insecure_port('{}:{}'.format(args.host, args.port))
    server.start()

    # since server.start() will not block,
    # a sleep-loop is added to keep alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)