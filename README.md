# KROpenApi

A small wrapper for interacting with the https://krdict.korean.go.kr/

```
from kropenapi.kropenapi import KROpenApi
k = KROpenApi()

examples = k.searchExamples('집')
definitions = k.searchWord('집')
print(x)

```

I've had mixed results with the API options, but feel free to experiment.
