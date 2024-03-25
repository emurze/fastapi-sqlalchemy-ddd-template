## Monolith Architecture

* CQS, not (pure CQRS)

* Goals
  * Single UoW
  * Base syntax - pydantic2


## Test Architecture

```python
@pytest.mark.unit
# or
@pytest.mark.integration
# or  
@pytest.mark.e2e
  ```

## Test shell commands

Runs all type checks, linting, and tests
```
poe check_all
```
Runs only tests
```
poe test
```
Runs unit tests
```
poe test_unit
```
Runs integration tests
```
poe test_integration
```
Runs e2e tests
```
poe test_e2e
```
