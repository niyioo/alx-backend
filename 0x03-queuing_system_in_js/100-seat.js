import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

// Create Redis client
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Function to reserve a seat
const reserveSeat = async (number) => {
    await setAsync('available_seats', number);
};

// Function to get the current available seats
const getCurrentAvailableSeats = async () => {
    const availableSeats = await getAsync('available_seats');
    return parseInt(availableSeats);
};

// Initialize number of available seats and reservation status
reserveSeat(50);
let reservationEnabled = true;

// Create Kue queue
const queue = kue.createQueue();

// Express server setup
const app = express();
const PORT = 1245;

// Middleware to parse JSON bodies
app.use(express.json());

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservation are blocked' });
    }
    queue.create('reserve_seat').save((err) => {
        if (err) {
            return res.json({ status: 'Reservation failed' });
        }
        res.json({ status: 'Reservation in process' });
    });
});

// Route to process the queue and reserve seats
app.get('/process', async (req, res) => {
    res.json({ status: 'Queue processing' });
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats === 0) {
        reservationEnabled = false;
    }
    if (availableSeats >= 0) {
        queue.process('reserve_seat', async (job, done) => {
            const currentAvailableSeats = await getCurrentAvailableSeats();
            if (currentAvailableSeats <= 0) {
                done(new Error('Not enough seats available'));
            } else {
                await reserveSeat(currentAvailableSeats - 1);
                if (currentAvailableSeats - 1 === 0) {
                    reservationEnabled = false;
                }
                done();
            }
        });
    }
});

// Start the Express server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});

