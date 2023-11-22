import aioredis


class RedisPubSubManager:

    def __init__(self, host='localhost', port=6379):
        self.redis_connection = None
        self.redis_host = host
        self.redis_port = port
        self.pubsub = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        return aioredis.Redis(host=self.redis_host, port=self.redis_port)

    async def connect(self) -> None:
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def _publish(self, room_id: str, message: str) -> None:
        await self.redis_connection.publish(room_id, message)

    async def subscribe(self, room_id: str) -> aioredis.Redis:

        await self.pubsub.subscribe(room_id)
        return self.pubsub

    async def unsubscribe(self, room_id: str) -> None:
        await self.pubsub.unsubscribe(room_id)