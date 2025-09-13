"""creature endpoints."""

from fastapi import APIRouter
from model.creature import Creature
import data.creature as service

router = APIRouter(prefix="/creature", tags=["Creature"])


@router.get("/")
def get_all():
    return service.get_all()


@router.get("/{name}")
def get_one(name):
    return service.get_one(name)


@router.post("/")
def create(creature: Creature):
    return service.create(creature)


@router.delete("/{name}")
def delete(name):
    return service.delete(name)


@router.patch("/{name}")
def modify(name, creature: Creature):
    return service.modify(name, creature)


@router.put("/{name}")
def replace(name, creature: Creature):
    return service.replace(name, creature)
