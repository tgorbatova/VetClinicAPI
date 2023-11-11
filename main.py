from enum import Enum
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="VetClinicApp"
              )


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str = Field(title='Name')
    pk: Optional[int] = Field(title='Pk')
    kind: DogType = Field(title='DogType', description='An enumeration.')


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return 'Home'

@app.post('/post')
def reg_post() -> Timestamp:
    post_db.append(Timestamp(id=post_db[-1].id+1, timestamp=post_db[-1].timestamp+1))
    return post_db[-1]

@app.get('/dog')
def get_dogs(kind: DogType) -> List[Dog]:
    dogs=[]
    for id in dogs_db:
        if dogs_db[id].kind == kind:
            dogs.append(dogs_db[id])
    if len(dogs)==0:
        return 'Data not found'
    else:
        return dogs

@app.post('/dog')
def create_dog(dog: Dog) -> Dog:
    if dog.pk == list(dogs_db)[-1] + 1:
        dogs_db[list(dogs_db)[-1] + 1] = dog
        return dogs_db[list(dogs_db)[-1]]
    else:
        return {'Error': 'Unavailable pk'}

@app.get('/dog/{pk}')
def get_dog_by_pk(pk: int) -> Dog:
    if pk not in dogs_db:
        return {'Error': 'pk does not exist'}
    return dogs_db[pk]

@app.patch('/dog/{pk}')
def update_dog(pk: int, dog: Dog) -> Dog:
    if pk not in dogs_db:
        return {'Error': 'pk does not exist'}
    dogs_db[pk] = dog
    return dogs_db[pk]