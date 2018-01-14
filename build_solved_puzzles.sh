# be in puzzles
cat ../puzzle_filesnames.txt | xargs grep -L index | xargs grep -L midpoint | xargs grep -l "news.word....3.60" > ../solved_puzzles_high_news.txt
