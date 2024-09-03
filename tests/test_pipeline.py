from unittest.mock import MagicMock, call, mock_open

import pytest

from pipeline import (
    create_directory,
    is_json_serializable,
    process_search_results,
    process_video,
    save_json,
    save_text,
)


@pytest.fixture
def mock_os_path_join():
    with pytest.mock.patch(
        "os.path.join", side_effect=lambda *args: "/".join(args)
    ) as mock_join:
        yield mock_join


def test_create_directory(mocker):
    mock_makedirs = mocker.patch("os.makedirs")
    create_directory("test_directory")
    mock_makedirs.assert_called_once_with("test_directory", exist_ok=True)


def test_save_json(mocker):
    mock_file = mocker.patch("builtins.open", new_callable=mock_open)
    mock_json_dump = mocker.patch("json.dump")
    data = {"key": "value"}
    save_json(data, "test_file.json")
    mock_file.assert_called_once_with("test_file.json", "w")
    mock_json_dump.assert_called_once_with(data, mock_file(), indent=4)


def test_save_text(mocker):
    mock_file = mocker.patch("builtins.open", new_callable=mock_open)
    data = ["line1", "line2"]
    save_text(data, "test_file.txt")
    mock_file.assert_called_once_with("test_file.txt", "w")
    mock_file().write.assert_called_once_with("line1\nline2")


def test_is_json_serializable():
    assert is_json_serializable({"key": "value"})
    assert not is_json_serializable(set([1, 2, 3]))


def test_process_video_with_video_info(mocker, mock_os_path_join):
    mock_rename = mocker.patch("os.rename")
    mock_convert_video = mocker.patch("pipeline.convert_video_to_audio")
    mock_diarize_speakers = mocker.patch(
        "pipeline.diarize_speakers", return_value=(MagicMock(), MagicMock())
    )
    mock_save_json = mocker.patch("pipeline.save_json")
    mock_save_text = mocker.patch("pipeline.save_text")
    mock_makedirs = mocker.patch("os.makedirs")
    mock_path_exists = mocker.patch("os.path.exists", return_value=False)

    video_info = {
        "requested_downloads": [{"filename": "downloaded.mp4"}],
        "id": "video_id",
        "title": "video_title",
    }
    parent_dir = "./data"

    process_video(video_info, parent_dir)

    mock_path_exists.assert_called_once()
    mock_makedirs.assert_called_once_with("./data/video_id = video_title")
    mock_rename.assert_called_once_with(
        "downloaded.mp4", "./data/video_id = video_title/video.mp4"
    )
    mock_convert_video.assert_called_once_with(
        "./data/video_id = video_title/video.mp4",
        "./data/video_id = video_title/audio.mp3",
    )
    mock_diarize_speakers.assert_called_once_with(
        "./data/video_id = video_title/audio.mp3"
    )
    mock_save_json.assert_any_call(
        video_info, "./data/video_id = video_title/metadata.json"
    )
    mock_save_text.assert_called_once()


def test_main_local_mode(mocker):
    mock_isfile = mocker.patch("os.path.isfile", return_value=True)
    mock_process_video = mocker.patch("pipeline.process_video")

    with pytest.mock.patch("sys.argv", ["pipeline.py", "local", "test_audio.m4a"]):
        from pipeline import main

        main("local", "test_audio.m4a")

    mock_isfile.assert_called_once_with("test_audio.m4a")
    mock_process_video.assert_called_once_with(
        None, "./data", local_audio_file="test_audio.m4a"
    )


def test_process_search_results(mocker, mock_os_path_join):
    mock_extract_info = mocker.patch(
        "pipeline.YoutubeDL.extract_info",
        return_value={"entries": [{"id": "video1"}, {"id": "video2"}]},
    )
    mock_process_video = mocker.patch("pipeline.process_video")
    ydl = MagicMock()
    search_results = {"entries": [{"id": "video1"}, {"id": "video2"}]}
    parent_dir = "./data"

    process_search_results(ydl, search_results, parent_dir)

    expected_calls = [
        call("https://www.youtube.com/watch?v=video1", download=True),
        call("https://www.youtube.com/watch?v=video2", download=True),
    ]
    assert ydl.extract_info.call_args_list == expected_calls
    assert mock_process_video.call_count == 2
