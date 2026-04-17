import subprocess

letters = 'ابتثجحخدذرزسشصضطظعغفقكلمنهوي'

for letter in letters:
    print(f"\nجاري تحليل: {letter}")
    subprocess.run(
        ['python', 'analyze_letter_stats.py'],
        input=letter,
        text=True,
        encoding='utf-8'
    )