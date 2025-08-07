from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from google.protobuf import json_format
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from . import testMessage_pb2
from database import get_async_session

from test.models import Test
from test.schema import TestResponse, TestCreate

router = APIRouter(
    prefix="/test",
    tags=["Test"],
)


@router.post("/", response_model=TestResponse)
async def create_note(
    test: TestCreate,
    db: AsyncSession = Depends(get_async_session),
):
    # try:
    #     corrected_text = await validate_text(note.content)
    # except Exception:
    #     corrected_text = note.content + "_uncorrected"
    try:
        db_test = Test(test=test.test)
        db.add(db_test)
        await db.commit()
        await db.refresh(db_test)
        return db_test
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")


@router.get("/", response_model=List[TestResponse])
async def read_notes(
    db: AsyncSession = Depends(get_async_session),
    # user: UserResponse = Depends(get_current_user),
):
    try:
        result = await db.execute(select(Test))
        tests = result.scalars().all()
        return tests
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")


@router.post("/proto", response_model=TestResponse)
async def new_proto(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
):
    body = await request.body()

    # Создаем объект Protobuf и парсим данные
    test_proto = testMessage_pb2.TestMessage()
    try:
        test_proto.ParseFromString(body)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Protobuf data")

    # Конвертируем Protobuf в dict (опционально)
    test_data = json_format.MessageToDict(test_proto)
    try:
        db_test = Test(test=test_data.test)
        db.add(db_test)
        await db.commit()
        await db.refresh(db_test)
        return db_test
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")