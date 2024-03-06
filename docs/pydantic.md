# Pydantic

### Config

* frozen

* strict

* extra - 'forbid', 'allow' in init, 'ignore' - auto repr=False, exclude=True
  ```python
  class BaseConfig(BaseModel):
      model_config = ConfigDict(extra='forbid')
  
  
  class NewModel(BaseConfig):
      a: int
  
  
  def test_new_model_forbid() -> None:
      with pytest.raises(ValidationError):
          NewModel(a=1, b=3)
  ```

* populate_by_name
  ```python
  class Model1(BaseModel):
      model_config = ConfigDict(populate_by_name=True)
      kitty: str = Field(alias='cat')
  
  
  def test_populate_by_name() -> None:
      m1 = Model1(kitty='dog')
      assert m1.model_dump() == {'kitty': 'dog'}
  
  
  def test_populate_by_name_attr() -> None:
      m2 = Model1(cat='dog')
      assert m2.model_dump() == {'kitty': 'dog'}
  ```

* validate_assignment - Revalidate Model when field is changed
  ```python
  class Class(BaseModel, validate_assignment=True):
      a: int
  
  
  def test_validate_assignment_success() -> None:
      class_ = Class(a=2)
      class_.a = '3'  # because of strict = False
  
  
  def test_validate_assignment_error() -> None:
      class_ = Class(a=2)
      with pytest.raises(ValidationError):
          class_.a = 'hi'
  ```
  
* use_enum_values
  ```python
  class Card(Enum):
      F = 'FIRST'
      S = 'SECOND'
  
  
  class Deck(BaseModel):
      model_config = ConfigDict(use_enum_values=True)
      cards: list[Card] = Field(default=Card.F)
  
  
  def test_deck_schema() -> None:
      deck = Deck(cards=[Card.F])
      print(deck.model_dump() == {'cards': ['FIRST']})
  ```

* validate_default - validate default in Field

* coerce_numbers_to_str - independent of strict option

* arbitrary_types_allowed - you can use simple __init__.py classes
  ```python
  class ICar(Protocol):
      mark: str
  
  
  class Car:
      def __init__(self, mark: str) -> None:
          self.mark = mark
  
      def __eq__(self, other: ICar) -> bool:
          return self.mark == other.mark
  
      def __repr__(self) -> str:
          return self.mark
  
  
  class Builder(BaseModel):
      model_config = ConfigDict(arbitrary_types_allowed=True)
  
      car: Car
      age: int
  
  
  def test_arbitrary_type_allowed() -> None:
      car = Car('BMW')
      builder = Builder(car=car, age=10)
      assert builder.model_dump() == {'car': Car('BMW'), 'age': 10}
  ```

* from_attributes
  ```python
  @dataclass
  class Human:
      name: str
      age: int
  
  
  class Person(BaseModel):
      model_config = ConfigDict(from_attributes=True)
      name: str
      age: PositiveInt
  
  
  def test_from_attributes() -> None:
      human = Human('vlad', 24)
      person = Person.model_validate(human)
      print(person.model_dump())
  ```

* json_schema_extra
  ```python
  class Bora3(BaseModel):
      model_config = ConfigDict(json_schema_extra={'vlad': 'THE BEST GUY'})
      a: int = Field(json_schema_extra={'name': 'THE BEST GUY'})
  
  
  def test_config_json_schema_extra() -> None:
      assert Bora3.model_json_schema(mode='validation') == {
          'properties': {
              'a': {
                  'name': 'THE BEST GUY',
                  'title': 'A',
                  'type': 'integer',
              },
          },
          'required': ['a'],
          'title': 'Bora3',
          'type': 'object',
          'vlad': 'THE BEST GUY',
      }
  ```

* revalidate_instances ( Mutable Problem ) - dataclasses, etc aren't revalidated during validation
  ```python
  class SubHuman(BaseModel):
      name: str
      age: int
  
      
  class SubPerson(BaseModel):
      human: SubHuman
  
  
  def test_revalidate_instances_no_error() -> None:
      human = SubHuman(name='Vlad', age=24)
      human.name = 1234
      SubPerson(human=human)
  ```
  ```python
  class SubPerson(BaseModel, revalidate_instances='always'):
      human: SubHuman
  
  
  def test_revalidate_instances_errors() -> None:
      human = SubHuman(name='Vlad', age=24)
      human.age = 'age'
  
      with pytest.raises(ValidationError):
          SubPerson(human=human)
  ```
  
* hide_input_in_errors - protects you from SQL-injection
  ```
  [type=string_type]
  
  # rather than
   
  [type=string_type, input_value=1, input_type=int]
  ```

* base_settings sources reordering, adding, removing

### Methods

* .model_construct() - build without validation

```python
class YourModel(BaseModel):
    # model_config = ConfigDict(defer_build=True) to change types_namespace
    value: int


def test_model_construct() -> None:
    model = YourModel.model_construct(value='hi')
    assert model.value == 'hi'
```

* .model_validate() - you can pass any format, but firstly convert it to dict
* .model_validate_json() - fast build-in validation


* .model_dump()
* .model_dump_json()


* .model_copy()


* .model_extra() - Field set during validation
  ```python
  class Post(BaseModel):
      model_config = ConfigDict(extra='allow')
  
      id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
      title: str = Field(
          description='FROM ARG',
          json_schema_extra={
              'description': 'FROM JSON_SCHEMA_EXTRA',
              'name': 'Lera',
          }
      )
  
      def __post_init__(self, data: str) -> None:
          self.data = data
  
  
  
  def test_model_extra_data() -> None:
      post = Post(title='Hello world!', name='Vlad')
      post.model_post_init('hello')
  
      assert post.model_extra == {'name': 'Vlad'}
  ```


* .model_parametrized_name() - name with Generic


* .model_perform_post_init(**kwargs)


* .model_fields - dict('field_1': FieldInfo(), 'field_2': FieldInfo())
* .model_fields_set - ('id', 'title'')


* .model_json_schema(mode="validation" | "serialization") - model presentation
* .model_rebuild()
  ```python
  class Bar(BaseModel):
      foo: 'Foo10'


  def test_rebuild() -> None:
      with pytest.raises(PydanticUserError):
          Bar.model_json_schema()

      class Foo10(BaseModel):
          pass

      Bar.model_rebuild()
      pprint(Bar.model_json_schema())
  ```

### Field


* helpers
  - AliasPath('names', 0)
  - AliasChoices('first_alias', 'second_alias')


* default
  - default
  - default_factory


* alias
  - alias - becomes general for validation_alias and serialization_alias
  - validation_alias - init, model_validate
  - serialization_alias - model_dump, model_dump_json


* hide
  - exclude = True - exclude from model_dump
  - repr = False - exclude from representation


* docs
  - title   
  - description
  - examples

  
* pydantic dataclass
  - init_var - or InitVar - error if it doesn't exist
  - kw_only - pydantic dataclass


* string
  - min_length
  - max_length
  - pattern


* number
  - gt
  - ge
  - lt
  - le
  - multiple_of
  - allow_inf_nan


* decimal
  - decimal_places
  - max_digits


* union polymorphism
  - discriminator
  ```python
  class Cat(BaseModel):
      type: Literal['cat', 'kitty']
      age: PositiveInt
    
    
  class Dog(BaseModel):
     type: Literal['dog', 'puppy']
     age: PositiveInt
    
    
  class Model(BaseModel):
     """
     Discriminator allows you to know which model to use.
     Is a type of polymorphism
     """
    
     pet: Cat | Dog = Field(discriminator='type')
    
    
    def test_model_discriminator() -> None:
        model = Model(pet={'type': 'dog', 'age': 1})
    
        assert model.pet.type == 'dog'
        assert model.pet.age == 1
    ```


* strict (table) '1' -> 1 parsing


* frozen, useful for Entity id


* validate_default

  ```python
  class YourModel(BaseModel):
      age: int = Field(default="an apple", validate_default=False)


  def test_validate_default() -> None:
      model = YourModel()
      assert model.age == 'an apple'
  ```
  
* json_schema_extra - add field like title, description, or examples

  ```python
  class Post(BaseModel):
      id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
      title: str = Field(
          description='FROM ARG',
          json_schema_extra={
              'description': 'FROM JSON_SCHEMA_EXTRA',
              'name': 'Lera',
          }
      )
  
  
  def test_json_schema_extra() -> None:
      post = Post(title='Hello world!')
      pprint(post.model_json_schema())
  ```

### Annotations

```python
Annotated[
    int,
    Field(...),
    Field(...),
]
```

* SecretStr


* PositiveInt


* NonNegativeInt


* StrictBool - Annotated[bool, Strict()]


* Json


### Validators

* @validate_call

* TypeAdapter

* Annotated validators
  - AfterValidator - takes first available place if initialized then executed
  - BeforeValidator - takes order place
  - PlainValidator - takes order place and stops after execution
  - WrapValidator - takes any order place
  
  ```python
  str_validation = Annotated[
      int,
      BeforeValidator(make_validator(max_validator, 'before-1')),
      WrapValidator(make_validator(wrap_map_validator, 'wrap-1')),
      BeforeValidator(make_validator(max_validator, 'before-2')),
      WrapValidator(make_validator(wrap_map_validator, 'wrap-2')),
      AfterValidator(make_validator(max_validator, 'after-2')),
      PlainValidator(make_validator(max_validator, 'plain-2')),
      BeforeValidator(make_validator(max_validator, 'before-3')),
      AfterValidator(make_validator(max_validator, 'after-3')),
      WrapValidator(make_validator(wrap_map_validator, 'wrap-3')),
      BeforeValidator(make_validator(max_validator, 'before-4')),
      WrapValidator(make_validator(wrap_map_validator, 'wrap-4')),
  ]
  # wrap-4
  # before-4
  # wrap-3
  # before-3
  # plain-2
  # after-3
  ```

* pydantic model validators
  ```python
  @field_validator('name', mode='after')
  @classmethod
  def check_after_name(cls, value: str) -> str:
      print('Validated')
      return value

  @model_validator(mode='before')
  @classmethod
  def check_before_model(cls, data: Any) -> str:
      print(data)
      return data

  @model_validator(mode='after')
  def check_after_model(self, data: Any) -> str:
      print(data)
      raise PydanticCustomError('Hello vlados', 'vlad is an answer')
      # return data
  ```

### Serializations

* @field_serializer
* @model_serializer
  ```python
  class Model(BaseModel):
      value: str
  
      @model_serializer
      def serialize_model(self) -> dict:
          return {'value': f'serialized {self.value}'}
  
  
  def test_model_serializer() -> None:
      model = Model(value='Hello')
      assert model.model_dump() == {'value': 'serialized Hello'}
  ```
  ```python
  class User(BaseModel):
      id: UUID = Field(frozen=True, default_factory=uuid4)
      name: str = Field(min_length=3, serialization_alias="username")
      age: int = Field(gt=16)
      city: str = Field(min_length=3, default='London')
      zip_code: Optional[str] = Field(default=None)
  
      @field_serializer('name')
      def serialize_name(self, name: str) -> str:
          return f'{name} + Vlad'
  
  
  def test_serialization() -> None:
      user = User(name='Arthas', age=28)
      assert (
          user.model_dump(
              include={'id', 'name', 'age', 'city', 'zip_code'},
              exclude={'age'},
              by_alias=True,
              exclude_defaults=True,
              exclude_unset=True,  # fields that you don't set manually,
              exclude_none=True,
          )
      ) == {'username': 'Arthas + Vlad'}
  ```

* Annotated
  - PlainSerializer
  - WrapSerializer
  
  ```python
  def serialize_int(value: Any, nxt: SerializerFunctionWrapHandler) -> str:
      return f"serialized {nxt(value)}"


  FancyInt = Annotated[int, WrapSerializer(serialize_int)]
  
  
  class Car(BaseModel):
      quantity: FancyInt
  
  
  def test_serializer() -> None:
      car = Car(quantity=40)
      print(car.model_dump())
  ```


### Performance

* list | tuple rather than Sequence


* Use Literal, not Enum - 3 times performance


* Use TypedDict over nested models


* TypeAdapter to namespace or definition area
