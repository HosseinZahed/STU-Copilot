#from services.cosmos_db_service import CosmosDBService
#from services.foundry_service import FoundryService
import logging
from dotenv import load_dotenv
import json
from github_crawler import GitHubCrawler
import asyncio
from blogs_crawler import BlogsCrawler
from cosmos_db_service import CosmosDBService
from foundry_service import FoundryService
from seismic_crawler import SeismicCrawler

load_dotenv(override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# db_service = CosmosDBService()
# foundry_service = FoundryService()
# logger.info("CosmosDBService initialized successfully.")

# search_terms = "ios app"

# # search_embedding = foundry_service.generate_embedding(search_terms)
# # print(search_embedding)

# results = db_service.hybrid_search(search_terms=search_terms, container_name="github-repos", top_count=1)

# #Show result items
# # for item in list(results):
# #     print(json.dumps(item, indent=2))

# print(results)

# github_crawler = GitHubCrawler()
# logger.info("GitHubCrawler initialized successfully.")
# github_crawler.run()

# blogs_crawler = BlogsCrawler(
#     cosmos_db_service=CosmosDBService(),
#     foundry_service=FoundryService()
# )

# feeds = blogs_crawler.rss_feed_to_json(
#     feed_url="https://devblogs.microsoft.com/landing")

# # for feed in feeds:
# #     logger.info(f"Processed blog item: {feed}")

seismic_crawler = SeismicCrawler(
    cosmos_db_service=CosmosDBService(),
    foundry_service=FoundryService()
)

seismic_crawler.run()
