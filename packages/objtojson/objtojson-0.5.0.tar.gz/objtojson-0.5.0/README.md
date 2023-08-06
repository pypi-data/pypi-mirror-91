# Object-to-JSON

JSON serializer for class instances with minimal declaration overhead.

# Features
* Attributes that represent object state are automatically detected
  by checking `__init__` argument names
* Custom serializers for objects with complex state
* Automatic generation of `__eq__` method

# Usage

## Installation

`pip install objtojson`

## Example

```python
from objtojson import Serialized

class SomeClass(Serialized):
    def __init__(self, someAttribute, other):
        self.someAttribute = someAttribute
        self.other = other

class AnotherClass(Serialized):
    def __init__(self, a, b):
        self.a = a
        self.b = b

a = SomeClass(4, [AnotherClass(['a', 'list'], {'mykey': 34}), 'somestring'])      
print(a.Serialize())
```
Result:
```json
{
    "__someclass__": {
        "someAttribute": 4,
        "other": [
            {
                "__anotherclass__": {
                    "a": [
                        "a",
                        "list"
                    ],
                    "b": {
                        "mykey": 34
                    }
                }
            },
            "somestring"
        ]
    }
}
```

### Saving to file, loading from file

```python
from objtojson import Serializer

Serializer.Save('data.json', a)
a_reloaded = Serializer.Load('data.json')
```

## Restrictions

* Attribute names must match `__init__` argument names
* Tuples will be serialized/deserialized as lists
* Dict keys must be valid JSON object keys (i.e., strings)