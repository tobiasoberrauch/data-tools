import logging
import os

import torch
import whisperx
from fastapi import APIRouter, HTTPException
from moviepy.editor import VideoFileClip
from pydantic import BaseModel
from pytube import YouTube

from .utils import (
    align_transcription,
    assign_speakers,
    diarize_audio,
    download_video,
    ensure_paths_exist,
    extract_audio,
    save_transcription,
    transcribe_audio,
)

router = APIRouter()


class ProcessRequest(BaseModel):
    video_id: str


class TranscriptionRequest(BaseModel):
    audio_path: str


class DiarizationRequest(BaseModel):
    audio_path: str


class AssignSpeakersRequest(BaseModel):
    diarization_result: dict
    aligned_transcription: dict


@router.post("/extract_audio")
async def api_extract_audio(request: ProcessRequest):
    video_download_path, audio_download_path, _ = ensure_paths_exist(request.video_id)
    video_path = download_video(request.video_id, video_download_path)
    audio_path = extract_audio(video_path, audio_download_path)
    return {"audio_path": audio_path}


@router.post("/transcribe_audio")
async def api_transcribe_audio(request: TranscriptionRequest):
    model = whisperx.load_model(
        "large-v2",
        "cuda" if torch.cuda.is_available() else "cpu",
        compute_type="float16",
        download_root="./models",
    )
    transcription = transcribe_audio(request.audio_path, model)
    return {"transcription": transcription}


@router.post("/diarize_audio")
async def api_diarize_audio(request: DiarizationRequest):
    diarization_result = diarize_audio(request.audio_path)
    return {"diarization_result": diarization_result}


@router.post("/assign_speakers")
async def api_assign_speakers(request: AssignSpeakersRequest):
    final_transcription = assign_speakers(
        request.diarization_result, request.aligned_transcription
    )
    return {"final_transcription": final_transcription}


@router.post("/process_video")
async def api_process_video(request: ProcessRequest):
    video_download_path, audio_download_path, transcription_path = ensure_paths_exist(
        request.video_id
    )
    model = whisperx.load_model(
        "large-v2",
        "cuda" if torch.cuda.is_available() else "cpu",
        compute_type="float16",
        download_root="./models",
    )
    process_video(
        request.video_id,
        model,
        video_download_path,
        audio_download_path,
        transcription_path,
    )
    return {"message": "Video processed successfully", "video_id": request.video_id}


# Additional helper functions can be included if necessary
