# rag-crawler

## 프로젝트 구조

```
project-root/
├── application/
│   ├── services/
│   │   ├── crawl_service.py       # (내부에 class CrawlService)
│   │   └── scheduler_service.py   # (내부에 class SchedulerService)
│   └── commands/
├── domain/
│   ├── model/
│   │   ├── article.py             # (내부에 class Article)
│   │   └── url.py                 # (내부에 class Url)
│   └── repository/
│       └── article_repository.py  # (내부에 class ArticleRepository)
├── infrastructure/
│   ├── crawler/
│   │   ├── http_client.py
│   │   ├── parser.py
│   │   └── specific_site_crawler.py
│   └── persistence/
│       └── implementation/
│           └── sql_article_repository.py # (내부에 class SqlArticleRepository)
└── shared/
    ├── utils/
    └── exceptions/
```

## Poetry

### 버그

- dockerfile의 poetry 버전 맞추기
- poetry에 있는 README.md 옮기기

## Crawler

전반적인 흐름

- 데이터 베이스에 채널을 입력한다. 이건

## 개발

### 동영상 원시데이터 크롤링 로직

youtube api를 사용해 사용 특정 채널의 동영상을 전부 가져온다.

- 채널의 initialized가 false일 경우에는 그냥 전부 수집. 전부 수집이 완료된 경우에 initialized를 체크.
    -  일단은 채널마다 한번씩 시행하므로 수작업 api로 실행 가능
- initialized가 true일 경우에는 가장 먼저 같은 동영상을 만날경우 수집종료 (가장 최근 동영상만 수집)
    -   