import kue from 'kue';

// Array of blacklisted phone numbers
const blacklistedNumbers = ['4153518780', '4153518781'];

// Function to send notification
function sendNotification(phoneNumber, message, job, done) {
    // Track progress of the job
    job.progress(0, 100);

    // Check if phone number is blacklisted
    if (blacklistedNumbers.includes(phoneNumber)) {
        const error = new Error(`Phone number ${phoneNumber} is blacklisted`);
        job.failed().error(error);
        done(error);
    } else {
        // Track progress to 50%
        job.progress(50, 100);

        // Log sending notification
        console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);

        // Simulate sending notification asynchronously
        setTimeout(() => {
            // Complete the job
            job.progress(100, 100);
            done();
        }, 1000);
    }
}

// Create a Kue queue with concurrency of 2
const queue = kue.createQueue({ concurrency: 2 });

// Process the queue for 'push_notification_code_2' jobs
queue.process('push_notification_code_2', 2, (job, done) => {
    const { phoneNumber, message } = job.data;
    sendNotification(phoneNumber, message, job, done);
});

