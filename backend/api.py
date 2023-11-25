import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.dto.dtos import SingleClassifyDto, PackageClassifyDto
from backend.inference_model import InferenceModel
from backend.address_extractor import AddressExtractor

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor_model = InferenceModel("models/executor")
subject_model = InferenceModel("models/subject")
group_subject_model = InferenceModel("models/group-subject")
address_extractor = AddressExtractor()


@app.get("/")
async def root():
    return {"status": "OK"}


@app.post("/classify_single")
async def classify_single(data: SingleClassifyDto):
    loop = asyncio.get_event_loop()
    executor, subject, group_subject, address = await asyncio.gather(*[
        loop.run_in_executor(None, executor_model.predict, [data.text]),
        loop.run_in_executor(None, subject_model.predict, [data.text]),
        loop.run_in_executor(None, group_subject_model.predict, [data.text]),
        loop.run_in_executor(None, address_extractor.get_address, data.text)
    ])

    # executor = await loop.run_in_executor(None, executor_model.predict, [data.text])
    # subject = await loop.run_in_executor(None, subject_model.predict, [data.text])
    # group_subject = await loop.run_in_executor(None, group_subject_model.predict, [data.text])

    return {
        "originalText": data.text,
        "assignee": executor[0],
        "theme": subject[0],
        "themesGroup": group_subject[0],
        "address": address
    }


@app.post("/classify_package")
async def classify_package(data: PackageClassifyDto):
    return await asyncio.gather(*[
        classify_single(SingleClassifyDto(text=text)) for text in data.texts
    ])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
