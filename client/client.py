import sys
import grpc
import json

sys.path.append('../proto')
import system_pb2
import system_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50052')
    stub = system_pb2_grpc.ClientServiceStub(channel)

    # 1. Login
    login_res = stub.login(system_pb2.LoginRequest(username="admin", password="password"))
    token = login_res.token
    print(f"Login Status: {login_res.status}")

    # 2. Check Inventory
    get_res = stub.get(system_pb2.GetRequest(token=token, type="inventory_levels"))
    print("Initial Inventory:")
    for item in get_res.items:
        print(f" - {item.id}: {item.data}")

    # 3. Place an Order
    order_data = json.dumps({"item": "ItemA", "qty": 10})
    post_res = stub.post(system_pb2.PostRequest(token=token, type="order", data=order_data))
    print(f"Order Status: {post_res.status}")

    # 4. Request LLM Analytics
    analytics_res = stub.get(system_pb2.GetRequest(token=token, type="analytics"))
    print("LLM Analytics Report:")
    for item in analytics_res.items:
        print(f" - {item.data}")

if __name__ == '__main__':
    run()