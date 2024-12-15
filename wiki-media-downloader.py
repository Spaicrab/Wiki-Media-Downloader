import sys, argparse, os, traceback, re, html
import requests


def get_mime_url(wiki_url: str, MIME_type: str, offset: int, amount: int) -> str:
    mime_url = f"https://{wiki_url}/wiki/Special:MIMESearch?mime={MIME_type}&offset={offset}&limit={amount}"
    return mime_url


def download_media(
    wiki_url: str, MIME_type: str, file_callback: callable,
    offset: int = 0, amount: int = 5000, *callback_arguments
) -> int:
    # Return value, -1 means the function didn't even go inside the loop
    downloaded_file_count = -1

    if amount == 0:
        return downloaded_file_count

    # Make request look like it comes from Postman, some wikis block requests from a suspicious user agent
    headers = {"User-Agent": "PostmanRuntime/7.43.0"}
    mime_url = get_mime_url(wiki_url, MIME_type, offset, amount)
    try:
        request = requests.get(mime_url, headers=headers)
    except:
        raise ValueError("Invalid URL or no internet")

    request_result = str(request.content)
    for line in re.findall("<li>.+?(?=>download</a>)>download</a>", request_result):
        file_url = re.findall('[^"]*/[^"]*', line)[0]
        if not re.search("https://", file_url):
            if re.search("//", file_url):
                file_url = "https:" + file_url
            else:
                file_url = f"https://{wiki_url}{file_url}"

        filename = re.findall('title="[^"]*', line)[0][7:]
        if re.search("File:", filename):
            filename = filename[5:]

        decoded_characters = []
        for special_character in re.findall("&#[0-9]*;", filename):
            if special_character in decoded_characters:
                continue
            ascii_value = int(special_character[2:-1])
            real_character = chr(ascii_value)
            filename = filename.replace(special_character, real_character)
            decoded_characters.append(special_character)
        filename = html.unescape(filename)
        bad_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        filename = "".join(char for char in filename if char not in bad_characters)

        downloaded_file = file_callback(
            file_url, headers, filename, *callback_arguments
        )
        if downloaded_file_count == -1:
            downloaded_file_count = 0
        if downloaded_file:
            downloaded_file_count += 1

    return downloaded_file_count


def download_media_file(
    file_url: str, request_headers: dict, filename: str,
    output_directory: str, verbose: bool
) -> bool:
    path = os.path.join(output_directory, filename)
    if os.path.isfile(path):
        return False
    request = requests.get(file_url, headers=request_headers)
    file = open(path, "wb")
    file.write(request.content)
    file.close()
    if verbose:
        print("  " + filename)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Automatically downloads media files of a specified MIME type from a Wiki's MIME search page."
    )
    parser.add_argument(
        "WIKI_URL", type=str, help="wiki domain - e.g. 'simple.wikipedia.org'"
    )
    parser.add_argument(
        "MIME_TYPE", type=str, help="MIME type - e.g. 'image/png'"
    )
    parser.add_argument(
        "-d", "--output-directory",
        type = str, default = "", required = False,
        help = " output directory - default: new directory named after the wiki domain"
    )
    parser.add_argument(
        "-o", "--offset",
        type = int, default = 0, required = False,
        help = "start offset - default: 0"
    )
    parser.add_argument(
        "-a", "--amount",
        type = int, default = 100, required = False,
        help = "amount of files to download - default: 100"
    )
    parser.add_argument(
        "-v", "--verbose", action='store_true',
        help = "print detailed information - default: disabled"
    )
    
    WIKI_URL, MIME_TYPE, output_directory, offset, amount, verbose = "", "", "", 0, 100, False
    if not len(sys.argv) > 1:
        print(
            "This script will automatically download media files of a specified MIME type from a Wiki's MIME search page."
        )
        try:
            WIKI_URL = input("Wiki URL (e.g. 'simple.wikipedia.org'): ")
            MIME_TYPE = input("MIME type (e.g. 'image/png'): ")

            amount = input("Amount of files to download: ")
            amount = int(amount)

            start = input(
                "Starting file (e.g. if you have downloaded 100 files, this should be '101'): "
            )
            start = int(start)
            offset = start - 1

            verbose = True
        except:
            print("Invalid input. Quitting... \nPress Enter to close...")
            print(traceback.format_exc())
            input()
            return
    else:
        args = parser.parse_args()
        WIKI_URL = args.WIKI_URL
        MIME_TYPE = args.MIME_TYPE
        amount = args.amount
        offset = args.offset
        output_directory = args.output_directory
        verbose = args.verbose

    WIKI_URL = re.sub("https?://", "", WIKI_URL)
    WIKI_URL = re.findall("/?[^/]+", WIKI_URL)[0]

    offset = max(offset, 0)
    amount = max(amount, 0)

    if output_directory == "":
        directory_name = WIKI_URL.replace(".", "_") + "_images"
        output_directory = os.path.join(os.getcwd(), directory_name)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(f"Downloading media into {output_directory}...")

    downloaded_file_count = 0
    try:
        for i in range(int(amount / 5000) + 1):
            operation_offset = offset + 5000 * i
            operation_amount = min(amount, 5000)
            amount -= operation_amount
            downloaded_file_count += download_media(
                WIKI_URL, MIME_TYPE, download_media_file,
                operation_offset, operation_amount, output_directory, verbose,
            )
    except ValueError:
        print("Error: Invalid URL or no internet. \nQuitting...")
        if not len(sys.argv) > 1:
            input("Press Enter to close... \n")
        return

    if downloaded_file_count < 0:
        print(
            "The query didn't download anything. \n"
            + "Maybe you used an invalid MIME type? Try opening this url to see the valid types: \n"
            + get_mime_url(WIKI_URL, MIME_TYPE, offset, amount)
        )
    else:
        print("All done!")

    if not len(sys.argv) > 1:
        input("Press Enter to close... \n")


if __name__ == "__main__":
    main()
