```
OPENAI_API_KEY=<API_KEY_HERE>

docker build -t gptspeaktest .
docker run --rm -it -v ${PWD}:/app -p 5000:5000 -e OPENAI_API_KEY gptspeaktest
```

open "http://localhost:5000/public/index.html"
