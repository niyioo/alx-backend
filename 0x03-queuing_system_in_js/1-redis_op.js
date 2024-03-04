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

// Function to set a new school value
function setNewSchool(schoolName, value) {
    client.set(schoolName, value, redis.print);
}

// Function to display the value for a school
function displaySchoolValue(schoolName) {
    client.get(schoolName, (error, value) => {
        if (error) {
            console.error(`Error fetching value for ${schoolName}: ${error}`);
            return;
        }
        console.log(value);
    });
}

// Call the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

