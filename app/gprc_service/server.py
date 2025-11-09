import grpc, time
from concurrent import futures

from app.grpc_service import model_service_pb2, model_service_pb2_grpc
from app.models_manager import list_available_models, train_model, predict, delete_model
from app.logger import get_logger

logger = get_logger()

class ModelServiceServicer(model_service_pb2_grpc.ModelServiceServicer):
    def ListModels(self, request, context):
        return model_service_pb2.ModelList(models=list_available_models())

    def TrainModel(self, request, context):
        try:
            # interpret X as flattened pairs: [x11, x12, x21, x22, ...]
            X = [[request.X[i], request.X[i+1]] for i in range(0, len(request.X), 2)]
            model_id = train_model(request.model_type, X, request.y, {})
            return model_service_pb2.TrainResponse(message="OK", model_id=model_id)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return model_service_pb2.TrainResponse()

    def Predict(self, request, context):
        try:
            X = [[request.X[i], request.X[i+1]] for i in range(0, len(request.X), 2)]
            preds = predict(request.model_id, X)
            return model_service_pb2.PredictResponse(predictions=preds)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return model_service_pb2.PredictResponse()

    def DeleteModel(self, request, context):
        ok = delete_model(request.model_id)
        return model_service_pb2.DeleteResponse(message="Deleted" if ok else "Not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_service_pb2_grpc.add_ModelServiceServicer_to_server(ModelServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    logger.info("gRPC server listening on :50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
