import sys
import grpc
import threading
import json
from concurrent import futures

sys.path.append('../proto')
import system_pb2
import system_pb2_grpc

class InventoryAppServer(system_pb2_grpc.ClientServiceServicer):
    def __init__(self):
        # Thread-safe mock inventory state
        self.inventory = {"ItemA": 100, "ItemB": 50}
        self.lock = threading.Lock()
        
        # Connect to the LLM Server
        self.llm_channel = grpc.insecure_channel('localhost:50051')
        self.llm_stub = system_pb2_grpc.LLMServiceStub(self.llm_channel)

    def login(self, request, context):
        if request.username and request.password:
            return system_pb2.LoginResponse(status="SUCCESS", token="mock_token_123")
        return system_pb2.LoginResponse(status="FAILED", token="")

    def post(self, request, context):
        if request.type == "order":
            order_data = json.loads(request.data)
            item = order_data.get("item")
            qty = order_data.get("qty")
            
            # Concurrency control to prevent race conditions and negative stock
            with self.lock:
                if self.inventory.get(item, 0) >= qty:
                    self.inventory[item] -= qty
                    return system_pb2.StatusMessage(status="ORDER_SUCCESS")
                else:
                    return system_pb2.StatusMessage(status="INSUFFICIENT_STOCK")
                    
        return system_pb2.StatusMessage(status="UNKNOWN_REQUEST")

    def get(self, request, context):
        if request.type == "inventory_levels":
            items = [system_pb2.GetResponse.Item(id=k, data=str(v)) for k, v in self.inventory.items()]
            return system_pb2.GetResponse(status="SUCCESS", items=items)
            
        elif request.type == "analytics":
            # Utilize the LLM Server for insights
            inv_state = json.dumps(self.inventory)
            llm_req = system_pb2.LLMQuery(
                request_id="req_01", 
                query=f"Current stock: {inv_state}", 
                context="reorder_suggestions"
            )
            llm_response = self.llm_stub.getLLMAnswer(llm_req)
            
            items = [system_pb2.GetResponse.Item(id="llm_insight", data=llm_response.answer)]
            return system_pb2.GetResponse(status="SUCCESS", items=items)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    system_pb2_grpc.add_ClientServiceServicer_to_server(InventoryAppServer(), server)
    server.add_insecure_port('[::]:50052')
    print("Application Server running on port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()