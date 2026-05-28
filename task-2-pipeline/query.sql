
SELECT
  source_name,
  COUNT(*)                        AS article_count,
  ROUND(AVG(title_word_count), 1) AS avg_title_length,
  COUNTIF(has_description = TRUE) AS articles_with_desc
FROM `GOOGLE_APPLICATION_CREDENTIALS.news_pipeline.top_headlines`
WHERE search_topic = 'marketing'
GROUP BY source_name
ORDER BY article_count DESC
LIMIT 10;



SELECT
  hour_of_day,
  COUNT(*) AS article_count
FROM `GOOGLE_APPLICATION_CREDENTIALS.news_pipeline.top_headlines`
GROUP BY hour_of_day
ORDER BY hour_of_day ASC;



SELECT
  published_date,
  COUNT(*)                    AS total_articles,
  COUNT(DISTINCT source_name) AS unique_sources
FROM `GOOGLE_APPLICATION_CREDENTIALS.news_pipeline.top_headlines`
GROUP BY published_date
ORDER BY published_date DESC;