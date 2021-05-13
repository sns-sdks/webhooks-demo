Webhooks

Simple implementation for webhooks provide by [`Facebook`](https://developers.facebook.com/docs/graph-api/webhooks), [`Twitter`](https://developer.twitter.com/en/docs/twitter-api/enterprise/account-activity-api/guides/getting-started-with-webhooks).

<a href="https://github.com/sns-sdks/webhooks-demo/actions"><img src="https://github.com/sns-sdks/webhooks-demo/workflows/Test/badge.svg" alt="Github Action"></a>

## Run

### By Command

just run command as follows:

```commandline
uvicorn app.main:app --reload
```

### By Docker

Build it.

```commandline
docker build -t webhookimage .
```

Run it.

```commandline
docker run -d --name webhookcontainer -p 80:80 webhookimage
```
