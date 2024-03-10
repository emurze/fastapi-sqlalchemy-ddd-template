## Monolith Architecture

* CQS, not (pure CQRS)

## Test Architecture




* Mark unit, integration, e2e tests
  ```python
  @pytest.mark.unit
  # or
  @pytest.mark.integration
  # or  
  @pytest.mark.e2e
  ```
  
* Import fixtures automatically using pytest
  * integration
    ```python
    @pytest.fixture(scope="function")
    def repo(session: AsyncSession) -> IExampleRepository:
        return ExampleSqlAlchemyRepository(example_session)
    
    
    @pytest.mark.unit
    async def test_can_get_for_update(repo: IExampleRepository) -> None:
        await add_example(repo, "example")
  
        example = await repo.get_for_update(id=1)

        assert example.id == 1
        assert example.name == "example"
    
    
    @pytest.fixture(scope="function")
    def uow(session_factory: Callable) -> IAuthUnitOfWork:
        return AuthSqlAlchemyUnitOfWork(
            session_factory=session_factory,
            clients=ClientSqlAlchemyRepository,
        )
    
    
    @pytest.mark.integration
    async def test_client_unique_username(uow: IAuthUnitOfWork) -> None:
        vlad_data = {"username": "vlad"}
  
        async with uow:
            await uow.clients.add(**vlad_data)
            await uow.commit()
  
        async with uow:
            with pytest.raises(sqlalchemy.exc.IntegrityError):
                await uow.clients.add(**vlad_data)
    ```
  * e2e
    ```python
    @pytest.mark.e2e
    def test_add_client(client: TestClient) -> None:
        response: httpx.Response = client.post(
            "/clients/", json={"username": "Vlad"}
        )
        response_client = response.json()

        assert response.status_code == 201
        assert response_client["id"] == 1
        assert response_client["username"] == "Vlad"
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
