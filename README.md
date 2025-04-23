# YMatch

# 🚕 YontakMatch - 연세대학교 미래캠퍼스 택시 합승 플랫폼

YontakMatch는 연세대학교 미래캠퍼스 학생들을 위한 **택시 합승 매칭 플랫폼**입니다.  
FastAPI 백엔드 + Jinja2 기반 HTML 프론트엔드로 제작된 MVP 버전이며,  
학생들이 출발지, 도착지, 시간 정보를 등록하고 **서로 합승 제안과 수락**을 통해 편리하게 택시를 공유할 수 있도록 설계되었습니다.

---

## 주요 기능

### 요청 기능
- [x] 택시 요청 등록 (닉네임, 출발지, 도착지, 시간)
- [x] 전체 요청 리스트 보기 (활성 요청만)
- [x] 요청 취소 (자동으로 관련 제안도 취소)

### 합승 제안
- [x] 특정 요청자에게 합승 제안
- [x] 받은 제안 확인 (취소된 제안 제외)
- [x] 합승 수락 → 자동으로 해당 요청 비활성화
- [x] 제안자 본인이 제안 취소 가능

### 프론트엔드
- [x] HTML 기반 택시 요청 폼 (`/`)
- [ ] 추후 React 기반 SPA로 확장 예정

---

## 기술 스택

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** Jinja2, HTML
- **API 문서:** Swagger (`/docs`)
- **기타:** Pydantic, Uvicorn

---

## 실행 방법

### 1. 클론 및 이동
```bash
git clone https://github.com/yourusername/YontakMatch.git
cd YontakMatch
