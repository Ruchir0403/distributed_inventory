import sys
import grpc
from concurrent import futures
from transformers import pipeline

sys.path.append('../proto')
import system_pb2
import system_pb2_grpc

class LLMServiceServicer(system_pb2_grpc.LLMServiceServicer):
    def __init__(self):
        print("Loading local LLM (TinyLlama)...")
        # CPU-optimized, lightweight open-source model
        self.pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", device=-1)
        print("LLM Loaded and ready.")

    def getLLMAnswer(self, request, context):
        print(f"Received query type: {request.context}")
        
        # Craft domain-specific prompts based on the context
        if request.context == "reorder_suggestions":
            prompt = f"<|system|>\nYou are an inventory management assistant.<|user|>\nBased on this data, what should we reorder? {request.query}<|assistant|>\n"
        else:
            prompt = f"<|system|>\nYou are an AI assistant.<|user|>\n{request.query}<|assistant|>\n"

        response = self.pipe(prompt, max_new_tokens=100, truncation=True)
        generated_text = response[0]['generated_text'].split("<|assistant|>\n")[-1].strip()
        
        return system_pb2.LLMAnswerResponse(
            request_id=request.request_id,
            answer=generated_text
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    system_pb2_grpc.add_LLMServiceServicer_to_server(LLMServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("LLM Server running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()