import redis from 'redis';

// Create a Redis subscriber client
const subscriber = redis.createClient();

// Event listeners
subscriber.on('connect', () => {
    console.log('Redis client connected to the server');
});

subscriber.on('error', (error) => {
    console.error(`Redis client not connected to the server: ${error}`);
});

// Subscribe to the "holberton school channel"
subscriber.subscribe('holberton school channel');

// Handle incoming messages
subscriber.on('message', (channel, message) => {
    console.log(`Received message from channel ${channel}: ${message}`);
    if (message === 'KILL_SERVER') {
        subscriber.unsubscribe();
        subscriber.quit();
        console.log('Unsubscribed and quit');
    }
});

