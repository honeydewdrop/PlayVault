
import asyncio
import aiohttp
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

async def fetch_games(session, headers, limit, offset):
    url = 'https://api.igdb.com/v4/games'
    data = f'''fields name, cover.url; 
               limit {limit}; 
               offset {offset};'''

    try:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                logger.error(f"Error fetching games: {response.status}")
                return []
    except Exception as e:
        logger.exception(f"Exception occurred while fetching games: {e}")
        return []

async def fetch_all_igdb_games(total_games=500):
    # Twitch API credentials from settings

    headers = {
        'Client-ID': '5fx0c2tdp25zr3fuazhlqmwvezok4f',
        'Authorization': 'Bearer 9xs6a5rq9q9i37q84ca5w82uasrwt9',
    }

    limit = 50  # Adjust based on API's max allowed limit
    all_games = []
    offsets = range(0, total_games, limit)
    max_requests_per_batch = 4  # IGDB rate limit

    # Create a session and send asynchronous requests
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(offsets), max_requests_per_batch):
            # Prepare batch of requests respecting rate limits
            batch_offsets = offsets[i:i + max_requests_per_batch]
            tasks = [
                asyncio.create_task(fetch_games(session, headers, limit, offset))
                for offset in batch_offsets
            ]

            # Gather results
            results = await asyncio.gather(*tasks)

            # Flatten and store results
            for result in results:
                all_games.extend(result)

            # Respect rate limit by waiting asynchronously
            await asyncio.sleep(1)

    return all_games

