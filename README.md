# matome_python
(Helper for https://matome.fun) Web scraping, parsing, translation, saving to JSON, image download

### How to use
Edit url_.py's variable ```url``` to a matome site's article url.<br/>
Run ```py auto.py```

### Explanation
1. Given a particular URL, it automatically fetches original article's url, and selected comments' indcies.
2. Then, it goes to origianl article's url, fetches comment information, and downloads images.
3. Then, it translate japanese to korean using google translation api or naver papago api.
4. Finally, it saves all of the above to a JSON file.
