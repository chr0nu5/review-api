# API Reference

## All requests, except on /oauth/ must send a header 'X-Authorization' with a client token

### POST /oauth/token/ {username, password}

```{"token": "OauthGeneratedUniqueToken"}```

### POST /oauth/invalidate_token/ {username, password}

```{'msg': string}```

### GET /reviews/companies/

```{"companies": [{"rating": int, "id": int, "name": string}]}```

### GET /reviews/reviewers/

```{"reviewers": [{"id": int, "name": string}]}```

### POST /reviews/reviewers/ {name, email}

```{"reviewer": {"email": string, "id": int, "name": string}}```

### GET /reviews/reviews/

```{"reviews": [{"rating": int, "reviewer": {"email": string, "id": int, "name": string}, "title": string, "date": date, "ip": string, "company": {"id": int, "name": string}, "id": int, "summary": string}]}```

### POST /reviews/reviews/ {rating, title, summary, company_id, reviewer_id}

```{"review": {"rating": int, "reviewer": {"email": string, "id": int, "name": string}, "title": string, "date": date, "ip": string, "company": {"id": int, "name": string}, "id": int, "summary": string}}```
