"""
Celery background tasks for monitoring and maintenance
"""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.tasks.celery_app import celery_app
from app.config.database import async_session_maker
from app.repositories.image_repo import ImageRepository
from app.models.image import EnhancementStatus
from app.core.logging import get_logger
from app.core.metrics import image_enhancement_queue_length

logger = get_logger(__name__)


@celery_app.task(name="app.tasks.monitoring_tasks.check_stuck_images")
def check_stuck_images():
    """
    Check for images that have been processing for too long (>48 hours)
    and mark them as timeout
    """
    import asyncio
    
    async def _check_stuck_images():
        async with async_session_maker() as db:
            image_repo = ImageRepository(db)
            
            # Get stuck images (processing for more than 48 hours)
            stuck_images = await image_repo.get_stuck_images(hours=48)
            
            if stuck_images:
                image_ids = [img.id for img in stuck_images]
                count = await image_repo.mark_as_timeout(image_ids)
                await db.commit()
                
                logger.warning(
                    "stuck_images_marked_timeout",
                    count=count,
                    image_ids=[str(id) for id in image_ids]
                )
                
                return count
            
            return 0
    
    result = asyncio.run(_check_stuck_images())
    logger.info("check_stuck_images_completed", marked_count=result)
    return result


@celery_app.task(name="app.tasks.monitoring_tasks.aggregate_analytics")
def aggregate_analytics():
    """
    Aggregate analytics data hourly
    Update property view counts and calculate trending properties
    """
    import asyncio
    from sqlalchemy import select, func
    from app.models.property import Property
    from app.models.image import PropertyImage
    
    async def _aggregate_analytics():
        async with async_session_maker() as db:
            # Update active properties count metric
            from app.core.metrics import active_properties_total
            
            # Count by property type
            result = await db.execute(
                select(
                    Property.property_type,
                    func.count(Property.id)
                ).where(
                    Property.is_active == True
                ).group_by(
                    Property.property_type
                )
            )
            
            for property_type, count in result:
                active_properties_total.labels(
                    property_type=property_type.value
                ).set(count)
            
            # Update image enhancement queue length
            queue_result = await db.execute(
                select(func.count(PropertyImage.id)).where(
                    PropertyImage.enhancement_status == EnhancementStatus.PROCESSING
                )
            )
            queue_length = queue_result.scalar_one()
            image_enhancement_queue_length.set(queue_length)
            
            logger.info(
                "analytics_aggregated",
                timestamp=datetime.utcnow().isoformat(),
                queue_length=queue_length
            )
            
            return True
    
    result = asyncio.run(_aggregate_analytics())
    logger.info("aggregate_analytics_completed")
    return result


@celery_app.task(name="app.tasks.monitoring_tasks.warm_cache")
def warm_cache():
    """
    Warm cache with popular searches
    Run daily to pre-populate cache
    """
    import asyncio
    from app.models.property import PropertyType
    from app.repositories.property_repo import PropertyRepository
    from app.infrastructure.cache.redis_client import redis_client
    
    async def _warm_cache():
        async with async_session_maker() as db:
            property_repo = PropertyRepository(db)
            
            # Popular search combinations
            popular_searches = [
                {
                    "budget_min": 5000000,
                    "budget_max": 10000000,
                    "property_type": PropertyType.FLAT,
                    "bhk": 2
                },
                {
                    "budget_min": 10000000,
                    "budget_max": 20000000,
                    "property_type": PropertyType.FLAT,
                    "bhk": 3
                },
                {
                    "budget_min": 20000000,
                    "budget_max": 50000000,
                    "property_type": PropertyType.VILLA,
                    "bhk": 4
                },
            ]
            
            cached_count = 0
            
            for search_params in popular_searches:
                try:
                    properties, total = await property_repo.search_properties(
                        **search_params,
                        skip=0,
                        limit=20
                    )
                    
                    # Cache key
                    cache_key = f"search:{hash(str(search_params))}"
                    
                    # Cache results (simplified - in production, properly serialize)
                    await redis_client.set(
                        cache_key,
                        {"count": total, "timestamp": datetime.utcnow().isoformat()},
                        expire=300  # 5 minutes
                    )
                    
                    cached_count += 1
                    
                except Exception as e:
                    logger.error(
                        "cache_warming_failed",
                        search_params=search_params,
                        error=str(e)
                    )
            
            logger.info("cache_warmed", searches_cached=cached_count)
            return cached_count
    
    result = asyncio.run(_warm_cache())
    logger.info("warm_cache_completed", cached_count=result)
    return result
