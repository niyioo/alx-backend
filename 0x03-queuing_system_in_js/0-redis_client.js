import redis from 'redis';

// Connect to Redis server
const client = redis.createClient();

// Event listeners
client.on('connect', () => {
    console.log('Redis client connected to the server');
});

client.on('error', (error) => {
    console.error(`Redis client not connected to the server: ${error}`);
});

