
from pathlib import Path
import re
import os

PROJECT = "NMB"

def main():

    PARATEXT_DIRECTORY = Path("C:/My Paratext 9 Projects/" + PROJECT)

    files = PARATEXT_DIRECTORY.glob('*.SFM')
    finished_chapters = []
    for file in files:
        with open(file, "r", encoding="utf-8") as read_f:

            chapter_text = ""
            for line in read_f:
                line = line.strip()

                if line.startswith("\\id"):
                    book_id = line[4:7]

                elif line.startswith("\\mt"):
                    # Since the book name is used in the URL, remove zero-width spaces
                    book_name = line[4:].replace("\u200B","")

                elif line.startswith("\\c"):
                    # Add the previous chapter
                    if chapter_text:
                        finished_chapters.append((book_name, book_id, chapter_number, chapter_text))

                    chapter_number = convert_numbers(line[3:])
                    chapter_text = ""

                elif line.startswith("\\v"):
                    match = re.match(r'\\v (\d+) (.*)', line)
                    if match:
                        verse_number, verse_text = int(match.group(1)), match.group(2)
                        chapter_text += f" <sup>{verse_number}</sup> {verse_text}\n"

                elif line.startswith("\\p"):
                    chapter_text += "</p><p>"

            # Add the last chapter
            if chapter_text:
                finished_chapters.append((book_name, book_id, chapter_number, chapter_text))


    for chapter in finished_chapters:
        book_name, book_id, chapter_number, chapter_text = chapter
        title = book_name + " " + chapter_number
        output = add_head(finished_chapters, chapter, title)
        output += f"<h1>{title}</h1>\n"
        output += "<p>" + chapter_text + "</p>"
        output += add_foot(finished_chapters, chapter)
        os.makedirs(f"{PROJECT}/dist/{book_name}", exist_ok=True)
        os.makedirs(f"{PROJECT}/dist/{book_name}/{chapter_number}", exist_ok=True)
        with open(f"{PROJECT}/dist/{book_name}/{chapter_number}/index.html", "w", encoding="utf-8") as write_f:
            write_f.write(output)


def add_head(finished_chapters, current_chapter, title):

    current_book_name, _current_book_id, current_chapter_number, _current_chapter_text = current_chapter

    book_select = '<select onchange="window.location = this.value;" class="px-4 py-3 text-base bg-zinc-50 border border-zinc-300 text-zinc-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">'
    chapter_select = '<select onchange="window.location = this.value;" class="px-4 py-3 text-base bg-zinc-50 border border-zinc-300 text-zinc-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full dark:bg-zinc-700 dark:border-zinc-600 dark:placeholder-zinc-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 text-end">'
    previous_book_name = ""
    for book_name, _book_id, chapter_number, _chapter_text in finished_chapters:
        if book_name != previous_book_name:
            previous_book_name = book_name
            if current_book_name == book_name:
                book_select += f'<option selected value="../../{book_name}/{convert_numbers("1")}">{book_name}</option>'
            else:
                book_select += f'<option value="../../{book_name}/{convert_numbers("1")}">{book_name}</option>'

        if current_book_name == book_name and current_chapter_number == chapter_number:
            chapter_select += f'<option selected value="../../{book_name}/{convert_numbers(chapter_number)}">{chapter_number}</option>'
        else:
            chapter_select += f'<option value="../../{book_name}/{convert_numbers(chapter_number)}">{chapter_number}</option>'
    book_select += '</select>'
    chapter_select += '</select>'

    return f'''
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="../../css/style.css" rel="stylesheet">
  <title>{title}</title>
</head>
<body>
  <main class="pt-8 pb-16 px-8 lg:pt-16 lg:pb-24 bg-white dark:bg-zinc-900 text-xl md:text-2xl text-zinc-700 dark:text-zinc-300">
  <div class="grid gap-6 mb-8 lg:mb-16 md:grid-cols-4 max-w-xl mx-auto">
    <div class="md:col-span-3">
      {book_select}
    </div>
    <div>
      {chapter_select}
    </div>
  </div>
    <article class="mx-auto max-w-prose">
'''

def add_foot(finished_chapters, current_chapter):

    previous_chapter = None
    next_chapter = None

    for index, chapter in enumerate(finished_chapters):
        if chapter == current_chapter:
            if index > 0:
                previous_chapter = finished_chapters[index - 1]
            if index < (len(finished_chapters) - 1):
                next_chapter = finished_chapters[index + 1]
            break

    if previous_chapter:
        book_name, _book_id, chapter_number, _chapter_text = previous_chapter
        previous_html = f'''
        <a href="../../{book_name}/{chapter_number}/" class="text-white bg-zinc-700 hover:bg-zinc-800 rounded-full p-2.5 text-center inline-flex items-center dark:bg-zinc-600 dark:hover:bg-zinc-700">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
          </svg>
        </a>
        '''
    else:
        previous_html = ""

    if next_chapter:
        book_name, _book_id, chapter_number, _chapter_text = next_chapter
        next_html = f'''
        <a href="../../{book_name}/{chapter_number}/" class="text-white bg-zinc-700 hover:bg-zinc-800 rounded-full p-2.5 text-center inline-flex items-center dark:bg-zinc-600 dark:hover:bg-zinc-700">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
          </svg>
        </a>
        '''
    else:
        next_html = ""


    return f'''
    </article>
    <div class="w-[90vw] flex sticky bottom-[30%] z-10 justify-between max-w-6xl mx-auto">
      <div>
        {previous_html}
      </div>
      <div>
        {next_html}
      </div>
    </div>
  </main>
</body>
</html>
'''

def convert_numbers(numbers):
    numbers = numbers.replace("0","၀")
    numbers = numbers.replace("1","၁")
    numbers = numbers.replace("2","၂")
    numbers = numbers.replace("3","၃")
    numbers = numbers.replace("4","၄")
    numbers = numbers.replace("5","၅")
    numbers = numbers.replace("6","၆")
    numbers = numbers.replace("7","၇")
    numbers = numbers.replace("8","၈")
    numbers = numbers.replace("9","၉")

    return numbers


if __name__ == "__main__":
    main()