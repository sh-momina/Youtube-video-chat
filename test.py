# 🎥 Enter YouTube video URL: https://youtu.be/8GibwhJsxVA?si=j3CPk5oIelo4x5gO
# 📝 Transcribing audio with OpenAI Whisper API...
# Ask a question (or type 'exit' to quit): summarise the video
# 📋 Answer: The video is part of a series called "Road to Success". The speaker is just starting the series and promises more content to come. They also discuss the application requirements for Harvard, indicating that they will delve into this topic in more detail. They encourage viewers to like the video, subscribe, and stay tuned for the next one.
# Ask a question (or type 'exit' to quit): anything important or deadline they talk about
# 📋 Answer: There are two deadlines mentioned in the transcript: an application deadline in November and a regular decision deadline in January.
# Ask a question (or type 'exit' to quit): is sat or act compulsoray for the harvard university
# 📋 Answer: Yes, the SAT or ACT is mandatory for Harvard University.
# Ask a question (or type 'exit' to quit): and how much score for the sat is required
# 📋 Answer: The SAT score you want to aim for to be in the accepted pool of students at Harvard is anywhere around 1510 to 1580.
# Ask a question (or type 'exit' to quit): and what about act 
# 📋 Answer: The transcript does not provide specific information about the ACT score range for Harvard.
# Ask a question (or type 'exit' to quit): is there any score required for act to apply for har
# vard university 
# 📋 Answer: The transcript does not provide information on the required ACT score to apply for Harvard University.
# Ask a question (or type 'exit' to quit): is there any additional material provide like any li
# nk or something
# 📋 Answer: Yes, there is a link provided in the description below for the Ivy League 101 sneak peek. Additionally, within the supplemental essays, there is a link to a Google Doc.       
# Ask a question (or type 'exit' to quit): provide me the link to that essay 
# 📋 Answer: I'm sorry, but the transcript does not provide a specific link to the essay.
# Ask a question (or type 'exit' to quit): ok but where i can find the link 
# 📋 Answer: The link can be found in the description below.
# Ask a question (or type 'exit' to quit): 







# ------------------------------------------------------------------------------------








# https://www.youtube.com/watch?v=J5_-l7WIO_w&list=PLKnIA16_RmvaTbihpo4MtzVm4XOQa0ER0&index=17
# The v= parameter contains the video ID
# The list= parameter contains the playlist ID
# The index= is the position of the video within the playlist

# video_id = "J5_-l7WIO_w"

# video_id = "Gfr50f6ZBvo"

# video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# loader = YoutubeLoader.from_youtube_url(
#     video_url,
#     add_video_info=False,
#     language=["en"]
# )
# transcript = loader.load()

# print(transcript[3].page_content)

# https://www.youtube.com/watch?v=fY1yKQ4It90

# from youtube_transcript_api import YouTubeTranscriptApi
# from urllib.parse import urlparse, parse_qs

# def extract_video_id(youtube_url):
#     query = urlparse(youtube_url).query
#     params = parse_qs(query)
#     return params["v"][0]


# transcript = YouTubeTranscriptApi.get_transcript("6E10ebsKg0M", languages=["en"])
# for entry in transcript:
#     print(entry["text"])

# try:
#     transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
#     print("Transcript:", transcript_list)
# except TranscriptsDisabled:
#     print("❌ Transcripts are disabled for this video.")
# except NoTranscriptFound:
#     print("❌ No transcript found in the specified language.")
# except VideoUnavailable:
#     print("❌ Video is unavailable.")
# except Exception as e:
#     print("❌ Some other error occurred:", str(e))

# transcript = " ".join(chunk["text"] for chunk in transcript_list)

# sample = https://www.youtube.com/watch?v=8GibwhJsxVA