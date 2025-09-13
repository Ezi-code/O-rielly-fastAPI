from fastapi import APIRouter, HTTPException
from model.explorer import Explorer
import data.explorer as service
from data.errors import Duplicate, Missing
from fastapi import status

router = APIRouter(prefix="/explorer", tags=["Explorer"])


@router.get("/", status_code=status.HTTP_200_OK)
def get_all():
    return service.get_all()


@router.get("/{name}", status_code=status.HTTP_200_OK)
def get_one(name):
    try:
        return service.get_one(name)
    except Missing as err:
        raise HTTPException(status_code=404, detail=err.msg)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(explorer: Explorer):
    try:
        return service.create(explorer)
    except Duplicate as err:
        raise HTTPException(status_code=404, detail=err.msg)


@router.delete("/{name}")
def delete(name):

    return service.delete(name)


@router.patch("/{name}")
def modify(name, explorer: Explorer):
    return service.modify(name, explorer)


@router.put("/{name}")
def replace(name, explorer: Explorer):
    return service.replace(name, explorer)
