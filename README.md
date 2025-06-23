# Simple RAG System

이 프로젝트는 Kubernetes 환경에서 kakaocorp/kanana-1.5-2.1b-instruct-2505 모델을 사용한 RAG(Retrieval-Augmented Generation) 시스템을 구현합니다.

> **참고**: minikube 환경에서 싱글노드로 테스트했습니다.

## 시스템 구조

- **01_LLM_API**: LLM API 서버 (vLLM 기반 Kanana 2.1B 모델)
- **02_RAG**: RAG 컨트롤러 및 VectorDB 초기화
- **03_DEPLOY**: Kubernetes 배포 yaml

## Docker 이미지 빌드

### 1. LLM API 이미지 빌드

```bash
cd 01_LLM_API
docker build -t llm-api:latest .
minikube image load llm-api:latest
```

### 2. RAG 컨트롤러 이미지 빌드

```bash
cd 02_RAG
docker build -t rag-controller:latest .
minikube image load rag-controller:latest
```

## Kubernetes 배포

### 1. 환경 설정

배포 전에 namespace 및 .env 파일을 생성하고 OpenAI API 키를 설정합니다.

네임스페이스를 생성합니다:
```bash
kubectl create namespace rag-system
kubectl label namespace rag-system name=rag-system
```

`.env.example` 파일을 `.env`로 복사합니다:

```bash
cp .env.example .env
```

`.env` 파일에 OpenAI API 키를 입력합니다:
```env
OPENAI_API_KEY=your_openai_api_key
```

.env 파일에서 Secret을 Kubernetes Secret으로 생성합니다:

```bash
kubectl create secret generic rag-secrets --from-env-file=.env --namespace rag-system
```


### 2. 네임스페이스 및 기본 리소스 생성

```bash
kubectl apply -f 03_DEPLOY/k8s_manifest.yaml
```

### 3. 배포 확인

```bash
# 파드 상태 확인
kubectl get pods -n rag-system

# 서비스 확인
kubectl get svc -n rag-system

# 로그 확인
kubectl logs -n rag-system -l app=llm-api
kubectl logs -n rag-system -l app=rag-controller
kubectl logs -n rag-system -l app=chromadb
```

### 4. 벡터DB 데이터 초기화

RAG 시스템이 배포된 후, IT 기술 뉴스 데이터를 벡터DB에 로드하는 Job이 자동으로 실행됩니다:

```bash
# 초기화 Job 상태 확인
kubectl get jobs -n rag-system
kubectl logs -n rag-system -l job-name=rag-data-initialization
```

## API 엔드포인트

시스템이 정상 배포되면 다음 명령어를 통해 서비스에 접근할 수 있습니다:

- **RAG API**: `minikube service rag-controller-service -n rag-system`
- **LLM API**: `minikube service llm-api-service -n rag-system`
- **Vector DB**: `minikube service chromadb-service -n rag-system`

## API 사용 가이드

### RAG Controller API 엔드포인트

#### 1. 헬스 체크

시스템 상태를 확인합니다.

```bash
curl -X GET http://<RAG_SERVICE_URL>/health
```

**응답 예시:**

```json
{"status": "ok"}
```

#### 2. RAG 생성 API

질문을 입력하여 관련 문서를 검색하고 AI 응답을 생성합니다.

```bash
curl -X POST http://<RAG_SERVICE_URL>/api/rag/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "클라우드 컴퓨팅에 대해 설명해주세요"}'
```

**요청 파라미터:**
- `text` (string, 필수): 검색할 질문 텍스트

**응답 예시:**

```json
{
  "response": "클라우드 컴퓨팅은 인터넷을 통해 컴퓨팅 서비스를 제공하는 기술입니다..."
}
```