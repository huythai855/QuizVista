from youtube_transcript_api import YouTubeTranscriptApi


def get_youtube_transcript(video_url, language="en"):
    # Tách ID video từ URL
    video_id = video_url.split('v=')[1]
    # Trường hợp URL có thêm các tham số sau ID
    video_id = video_id.split('&')[0]

    try:
        # Lấy transcript cho video
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        all_text = ""

        # Hiển thị transcript
        for entry in transcript:
            # print(f"{entry['start']} - {entry['start'] + entry['duration']}: {entry['text']}")
            all_text += entry['text'] + " "
        return all_text

    except Exception as e:
        print(f"Lỗi: {e}")
        return ""


# Thay URL dưới đây bằng URL của video bạn muốn tải transcript
video_url = "https://www.youtube.com/watch?v=tzbLDH7Wa5o"
language = "vi"  # vi for Vietnamese, en for English


print(get_youtube_transcript(video_url, language))
