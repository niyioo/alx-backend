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

// Function to create and store a hash
function createHash() {
    client.hset('HolbertonSchools', 'Portland', 50, redis.print);
    client.hset('HolbertonSchools', 'Seattle', 80, redis.print);
    client.hset('HolbertonSchools', 'New York', 20, redis.print);
    client.hset('HolbertonSchools', 'Bogota', 20, redis.print);
    client.hset('HolbertonSchools', 'Cali', 40, redis.print);
    client.hset('HolbertonSchools', 'Paris', 2, redis.print);
}

// Function to display the stored hash
function displayHash() {
    client.hgetall('HolbertonSchools', (error, result) => {
        if (error) {
            console.error(`Error fetching hash: ${error}`);
            return;
        }
        console.log(result);
    });
}

// Call the functions
createHash();
displayHash();

