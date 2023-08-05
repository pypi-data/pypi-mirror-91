# Flexidispatch
> to dispatch according to arbitary criteria 


## Install

`pip install flexidispatch`

## How to use

Fill me in please! Don't forget code examples:

```python
process = Multimethod("processing payload", lambda x: x["framework"])

@process.add("polaris")
def f(x):
    return "I am polaris"

@process.add("vega")
def f(x):
    return "I am vega"
```

```python
process({
    "framework":"polaris",
    "scores":{"P":1,"O":1}
})
```




    'I am polaris'



```python
process({
    "framework":"vega",
    "x":[1,2],
    "scores":{"V":1,"E":1}
})
```




    'I am vega'


