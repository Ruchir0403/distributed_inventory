# Distributed Inventory Management System
Advanced Operating Systems project under Dr. Asish Bera presented by:
|Name|BITS ID|BITS email|
|-|-|-|
|Mitul Vashista|2026H1020071|H20260071@pilani.bits-pilani.ac.in|
|Ruchir Kumar|2026H|H2026@pilani.bits-pilani.ac.in|
|Parth|2026H1120137P|H20260137@pilani.bits-pilani.ac.in|

# Usage
Install required python dependencies:
```shell
pip install -r requirements.txt
```
## Steps
1. Run LLM server:
```shell
cd llm_server
python llm_service.py
```
2. Run RPC server:
```shell
cd app_server
python server.py
```
3. Run client:
```shell
cd client
python client.py
```

# Explaination of each component
## LLM Server
Serves a local TinyLlama LLM chatbot. It is exposed to the system using gRPC hooks. It is used to provide LLM-powered insights on current inventory & inventory acquisition.
## RPC Server
The main application/inventory server that handles core business logic for inventory management. Handles integration with other services through gRPC.
## Client
A reference client implementation showing how to consume the app_server's gRPC services.
