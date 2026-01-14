from app.services.ml_services import predict

sample_data = {
    "protocol": 1,
    "packet_size": 512,
    "duration": 10
}

print(predict(sample_data))