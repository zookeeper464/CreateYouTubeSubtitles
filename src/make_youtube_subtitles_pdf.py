from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from fpdf import FPDF
import requests
import warnings
import os


def save_youtube_captions(video_id: str, title: str):
  transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
  new_folder_path = f'../{title}'
  if not os.path.isdir(new_folder_path):
      os.mkdir(new_folder_path)

  with open(f'../{title}/{video_id}.txt', 'w') as f:
    for line in transcript:
      f.write(line['text'] + '\n')


def get_video_id_from_url(url: str) -> str:
  parsed_url = urlparse(url)
  video_id = parse_qs(parsed_url.query)['v'][0]
  return video_id


def convert_txt_to_pdf(file_name: str, title: str):
  new_folder_path = f'../{title}'
  if not os.path.isdir(new_folder_path):
      os.mkdir(new_folder_path)
  # 텍스트 파일 읽기
  with open(f'../{title}/{file_name}.txt', 'r', encoding='utf-8') as f:
    text = f.read()
  # PDF 생성
  pdf = FPDF()
  pdf.add_font('NanumGothic', '', '../assert/NanumGothic.ttf', uni=True)
  pdf.add_page()
  pdf.set_font("NanumGothic", size=12)
  pdf.multi_cell(0, 10, txt=text)
  pdf.output(f"../{title}/{file_name}.pdf")

def youtube_title (url: str) -> str:
  response = requests.get(url)

# Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(response.content, "html.parser")
  
  # Find the video title element and get its text
  title_element = soup.find("h1", {"class": "title"})
  return title_element.text.strip()

# 예시
warnings.filterwarnings("ignore", category=UserWarning)
url = 'https://www.youtube.com/watch?v=jFyRL4mjlIw'
# Example usage
save_youtube_captions(get_video_id_from_url(url), youtube_title(url))
convert_txt_to_pdf(get_video_id_from_url(url), youtube_title(url))

