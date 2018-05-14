# KROpenApi

A small wrapper for interacting with the https://krdict.korean.go.kr/

```
from kropenapi.kropenapi import KROpenApi
k = KROpenApi(your_api_key)

examples = k.searchExamples('집')
definitions = k.searchWord('집')
print(examples)
print(definitions)
```

I've had mixed results with the API options, but feel free to experiment.
