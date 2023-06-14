# OLX Home Scraper
Get list of homes for rent from [olx.pl](https://www.olx.pl/d/nieruchomosci/mieszkania/wynajem/wroclaw/), and help filter by animal sentiment.

# Building
```
docker build -t olx-scraper .
```

# Running
(pobrany model zapisywany w /home/kamil/.cache)
```
docker run -it -v /home/kamil/.cache:/root/.cache -v /home/kamil/Desktop/OLX-Home-Scraper/:/app olx-scraper python3 main.py
```