import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Object containing the Job data
const jobData = {
    phoneNumber: '1234567890',
    message: 'This is a notification message',
};

// Create a job and add it to the queue
const job = queue.create('push_notification_code', jobData);

// Event listeners
job.on('complete', () => {
    console.log('Notification job completed');
});

job.on('failed', () => {
    console.log('Notification job failed');
});

// Save the job to the queue
job.save((error) => {
    if (!error) {
        console.log(`Notification job created: ${job.id}`);
    }
});

// Process the queue
queue.process('push_notification_code', (job, done) => {
    // Simulate processing
    setTimeout(() => {
        console.log(`Processing job ${job.id}`);
        done();
    }, 2000);
});

