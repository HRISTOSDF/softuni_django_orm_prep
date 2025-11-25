# Python ORM Exam – 26 November 2023

This project is a solution for the Python ORM Exam.  
It represents a simple articles/reviews publishing platform built with Django ORM.  
The project manages Authors, Articles, and Reviews, with database models, queries, a custom model manager, and Django Admin customizations.

---

## Project Skeleton

- Ready-to-use skeleton provided. Do not change folder or file names.  
- Additional files may be added.  
- Archive project files (zip) for submission.  
- Do not include: `venv/`, `.idea/`, `__pycache__/`, `__MACOSX/` (Mac users).  
- Maximum archive size: 31.25 KB.

---

## Database Models

### Author Model
- `full_name` – CharField, 3–100 chars  
- `email` – EmailField, unique  
- `is_banned` – BooleanField, default False  
- `birth_year` – PositiveIntegerField, 1900–2005  
- `website` – URLField, optional  

### Article Model
- `title` – CharField, 5–200 chars  
- `content` – TextField, min 10 chars  
- `category` – CharField, choices: Technology, Science, Education (max 10, default Technology)  
- `authors` – ManyToMany → Author  
- `published_on` – DateTimeField, auto-generated on creation, not editable  

### Review Model
- `content` – TextField, min 10 chars  
- `rating` – FloatField, 1.0–5.0  
- `author` – ForeignKey → Author, on_delete=CASCADE  
- `article` – ForeignKey → Article, on_delete=CASCADE  
- `published_on` – DateTimeField, auto-generated, not editable  

---

## Django Admin Customizations

### AuthorAdmin
- Display: full_name, email, is_banned  
- Filter: is_banned  
- Search: full_name, email  

### ArticleAdmin
- Display: title, category, published_on  
- Filter: category  
- Search: title  
- Read-only: published_on  

### ReviewAdmin
- Display: author, article, rating, published_on  
- Filters: rating, published_on  
- Search: article title  
- Read-only: published_on  

---

## Custom Model Manager

### Author Manager
- Method: `get_authors_by_article_count()`  
- Returns all authors ordered by: 1) number of articles (desc), 2) email (asc)

---

## Functions in `caller.py`

- `get_authors(search_name=None, search_email=None)` – Retrieves authors partially and case-insensitively matching full name and/or email. If both arguments are None, return empty string. If both provided, search by both; otherwise search by the provided field. Matching authors are ordered by full_name descending. Returns string per author: `"Author: {full_name}, email: {email}, status: {Banned/Not Banned}"`.  

- `get_top_publisher()` – Retrieves the author with the greatest number of published articles. If multiple authors tie, order by email ascending and return the first one. Returns: `"Top Author: {full_name} with {num_of_articles} published articles."`. If no published articles, return empty string.  

- `get_top_reviewer()` – Retrieves the author with the greatest number of published reviews. If multiple authors tie, order by email ascending and return the first one. Returns: `"Top Reviewer: {full_name} with {num_of_reviews} published reviews."`. If no reviews, return empty string.  

- `get_latest_article()` – Retrieves the last published article. Authors’ full names separated by comma and sorted ascending. Average rating formatted to two decimals. Returns: `"The latest article is: {article_title}. Authors: {author1}, …, {authorN}. Reviewed: {num_reviews} times. Average Rating: {avg_reviews_rating}."`. If no articles, return empty string.  

- `get_top_rated_article()` – Retrieves the top-rated article based on review ratings. If multiple articles tie, order by title ascending. Average rating formatted to two decimals. Returns: `"The top-rated article is: {article_title}, with an average rating of {avg_rating}, reviewed {num_reviews} times."`. If no reviews, return empty string.  

- `ban_author(email=None)` – Finds author by exact email and sets is_banned=True. Deletes all their reviews (count first). Returns: `"Author: {full_name} is banned! {num_reviews} reviews deleted."`. If email is None or author not found, return `"No authors banned."`.  

---

## Testing Notes
- There will always be authors and articles when publishing reviews.  
- Populate the database with your own test data to verify function outputs.
