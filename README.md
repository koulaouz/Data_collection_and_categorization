# Parallel Data Scraper and Categorization with Clustering in Python

This repository is part of a larger project aimed at streamlining data collection and analysis for product categorization. It demonstrates the use of Selenium scripts for parallel scraping from three sources and subsequent categorization of products using a logistic regression model. Additionally, it applies K-means clustering on products within certain categories for further grouping.

 ## Features
 + Parallel Data Scrapping
   - Selenium scripts run in parallel to collect data from three different sources to achieve better execution time.
 + Product Categorization
   - Products are categorized into 14 categories using a logistic regression model
   - This custom model is trained on a train dataset that consists of 10000 entries from different sources but similar to the ones this project is aiming
   - The train dataset is not included due to copyright constraints
 + K-means Clustering
   - Products within specific categories are clustered into groups for deeper insights
