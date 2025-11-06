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
