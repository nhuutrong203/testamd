from fastapi import APIRouter, HTTPException
from src.data.schemas import ExplorerBase
from src.model.explorer import Explorer
import src.service.explorer as service
from error import Duplicate, Missing

router = APIRouter(prefix="/explorer")

@router.get("")
@router.get("/")
def get_all() -> list[ExplorerBase]:
    return service.get_all()

@router.get("/{name}")
def get_one(name) -> ExplorerBase:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(explorer: ExplorerBase) -> ExplorerBase:
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.patch("/{explorer_id}")
def modify(explorer_id: str, explorer: ExplorerBase) -> ExplorerBase:
    try:
        return service.modify(explorer_id, explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.delete("/{explorer_id}", status_code=204)
def delete(explorer_id: str):
    try:
        return service.delete(explorer_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

