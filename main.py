


import json
import sys

from scraper.channel import scrape as channel_scrape
from scraper.keyword_search import scrape as keyword_search_scrape
from scraper.keyword_search_shorts import scrape as keyword_search_scrape_shorts
import argparse

if __name__ == '__main__':
    # Argument Parser 생성
    parser = argparse.ArgumentParser(description="Search Channel URL or Search Keyword for scraper.")

    # 커맨드라인에서 받을 channel url 추가
    parser.add_argument("--channel_url", type=str, help="YouTube channel URL")

    # # 커맨드라인에서 받을 search keyword 추가
    parser.add_argument("--keyword", type=str, help="Search keyword")

    parser.add_argument("shorts", type=str, help="Shorts")

    parser.add_argument("video", type=str, help="Video")

    # 출력 파일 경로 (선택 인자, 기본값 제공)
    parser.add_argument(
        "--output",
        type=str,
        default="./output/output.json",  # 출력 파일 기본값 설정
        help="Path for saving the scraper output (default: 'output.txt')."
    )

    # 파라미터 파싱
    args = parser.parse_args()

    # 유효성 검사
    if not args.channel_url and not args.keyword:
        print("Error: Please provide either search keyword or channel URL.")
        sys.exit(1)

    if args.channel_url and args.keyword:
        print("Error: Please provide either search keyword or channel URL, not both.")
        sys.exit(1)

    if args.channel_url:
        data_result = channel_scrape(args.channel_url)
    if args.keyword:
        if args.shorts:
            data_result = keyword_search_scrape_shorts(args.keyword)
        else:
            data_result = keyword_search_scrape(args.keyword)
    json_data = json.dumps(data_result, ensure_ascii=False, indent=4)

    # 결과를 파일로 저장
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_data)
        print(f"Output successfully written to {args.output}")
    except Exception as e:
        print(f"Error writing to file {args.output}: {e}")
        sys.exit(1)  # 에러 발생 시 종료


