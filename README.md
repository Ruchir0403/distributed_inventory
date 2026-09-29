# Distributed Inventory Management System
Advanced Operating Systems project under Dr. Asish Bera, Birla Institute of Technology & Science, Pilani-Pilani Campus, presented by:
|Name|BITS ID|BITS email|
|-|-|-|
|Mitul Vashista|2026H1030071|H20260071@pilani.bits-pilani.ac.in|
|Ruchir Kumar|2026H1030083|H2026083@pilani.bits-pilani.ac.in|
|Parth|2026H1120137P|H20260137@pilani.bits-pilani.ac.in|

## Overview
This project implements a scalable, distributed inventory management solution using modern microservices architecture. It combines traditional inventory operations with AI/LLM capabilities to provide intelligent inventory analytics and natural language query support.

## Requirements
- Python 3.8+ (or language of choice based on implementation)
- gRPC and Protocol Buffers
- Python dependencies (see requirements.txt)

## Build Instructions
1. Clone Repository:
```shell
git clone https://github.com/Ruchir0403/distributed_inventory.git
cd distributed_inventory
```
2. Install required python dependencies:
```shell
pip install -r requirements.txt
```
3. Install grpcio-tools:
```shell
python-grpc-tools-protoc --python_out=./proto --grpc_python_out=./proto -I./proto proto/system.proto              
```

## Usage
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

## Explaination of each component
### LLM Server
Serves a local TinyLlama LLM chatbot. It is exposed to the system using gRPC hooks. It is used to provide LLM-powered insights on current inventory & inventory acquisition.
### RPC Server
The main application/inventory server that handles core business logic for inventory management. Handles integration with other services through gRPC.
### Client
A reference client implementation showing how to consume the app_server's gRPC services.
