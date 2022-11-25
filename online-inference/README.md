# HomeWork #2

## Local docker build
### Build
```bash
docker build . -t online_inference
```
### Run
```bash
docker run -p 8080:8080 online_inference
```

## Build from dockerhub
### Pull
```bash
docker pull rtmlrtx/online-inference:latest     
```

### Run
```bash
docker run -p 8080:8080 rtmlrtx/online-inference
```

## Docker Image optimization
1. Минимизация количества зависимостей.

2. Минимизация количества слоев COPY.

3. Использование slim версии базового образа (python:3.9-slim-buster), что дало прирост в минус 288.76 MB
к общему весу. 

Итоговый docker image имеет COMPRESSED SIZE 168.17 MB.
