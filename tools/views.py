from django.shortcuts import render


# Create your views here.
def frequency_view(request):
    if request.method == 'POST':
        words = stats(request.POST['text'])
        return render(request, 'tools/frequency.html', context={"words_stats": words})
    return render(request, 'tools/frequency.html')


def clean_line(line):
    for char in ".,:;!":
        line = line.replace(char, " ")
    return line.replace("  ", " ")


def stats(text):
    words = {}
    cleaned_line = clean_line(text)
    tokens = cleaned_line.split()
    for token in tokens:
        if token not in words:
            words[token] = 1
        else:
            words[token] += 1
    ordered_words = sorted(words.items(), key=lambda tuple: tuple[1], reverse=True)
    return ordered_words
