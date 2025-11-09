import grpc
from app.grpc_service import model_service_pb2, model_service_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = model_service_pb2_grpc.ModelServiceStub(channel)
        resp = stub.ListModels(model_service_pb2.Empty())
        print("Available models:", resp.models)

if __name__ == "__main__":
    run()
