# types-linq

![Python](https://img.shields.io/badge/python-3.7%2B-blue.svg) [![pypi](https://img.shields.io/pypi/v/types-linq)](https://pypi.org/project/types-linq/)

This is an attempt to implement linq methods seen in .NET ([link](https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable?view=net-5.0)). Currently WIP.

Goal:
* Incorporates Enumerable method specs as precise as possible
* Handles infinite streams (generators) smoothly like in _SICP_
  * Deferred evaluations
* Detailed typing support
* Honours collections.abc interfaces

To run the test cases, install `pytest`, and then invoke it under the current directory:
```sh
$ pytest
```

To install it on the computer, do
```sh
$ pip install .
# or
$ python setup.py install
```
Or install from pypi.

## Examples

The usage is simple if you know about the interfaces in .NET as this library provides almost the exact methods.

### [Grouping](https://docs.microsoft.com/en-us/dotnet/api/system.linq.enumerable.groupjoin) & Transforming lists
```py
from typing import NamedTuple
from types_linq import Enumerable as En


class AnswerSheet(NamedTuple):
    subject: str
    score: int
    name: str

students = ['Jacque', 'Franklin', 'Romeo']
papers = [
    AnswerSheet(subject='calculus', score=78, name='Jacque'),
    AnswerSheet(subject='calculus', score=98, name='Romeo'),
    AnswerSheet(subject='Algorithms', score=59, name='Romeo'),
    AnswerSheet(subject='Mechanics', score=93, name='Jacque'),
    AnswerSheet(subject='E & M', score=87, name='Jacque'),
]

query = En(students) \
    .group_join(papers,
        lambda student: student,
        lambda paper: paper.name,
        lambda student, papers: {
            'student': student,
            'papers': papers.select(lambda paper: {
                'subject': paper.subject,
                'score': paper.score,
            }).to_list(),
            'gpa': papers.average2(lambda paper: paper.score, None),
        }
    )

for obj in query:
    print(obj)

# output:
# {'student': 'Jacque', 'papers': [{'subject': 'calculus', 'score': 78}, {'subject': 'Mechanics', 'score': 93}, {'subject': 'E & M', 'score': 87}], 'gpa': 86.0}
# {'student': 'Franklin', 'papers': [], 'gpa': None}
# {'student': 'Romeo', 'papers': [{'subject': 'calculus', 'score': 98}, {'subject': 'Algorithms', 'score': 59}], 'gpa': 78.5}
```

### Working with generators
```py
import random
from types_linq import Enumerable as En

def toss_coins():
    while True:
        yield random.choice(('Head', 'Tail'))

times_head = En(toss_coins()).take(5) \  # [:5] also works
    .count(lambda r: r == 'Head')

print(f'You tossed 5 times with {times_head} HEADs!')

# possible output:
# You tossed 5 times with 2 HEADs!
```

### Also querying stream output
Mixing with builtin iterable type objects.
```py
import sys, subprocess
from types_linq import Enumerable as En

proc = subprocess.Popen('kubectl logs -f my-pod', shell=True, stdout=subprocess.PIPE)
stdout = iter(proc.stdout.readline, b'')

query = En(stdout).where(lambda line: line.startswith(b'CRITICAL: ')) \
    .select(lambda line: line[10:].decode())

for line in query:
    sys.stdout.write(line)
    sys.stdout.flush()

# whatever.
```
