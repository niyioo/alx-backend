import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
    let queue;

    beforeEach(() => {
        // Create a new Kue queue in test mode
        queue = kue.createQueue({ disableSearch: true, redis: { db: 3 } });
        queue.testMode.enter();
    });

    afterEach(() => {
        // Clear the queue and exit test mode after each test
        queue.testMode.clear();
        queue.testMode.exit();
    });

    it('display a error message if jobs is not an array', () => {
        // Test for throwing an error if jobs is not an array
        const testFunction = () => createPushNotificationsJobs('not an array', queue);
        expect(testFunction).to.throw('Jobs is not an array');
    });

    it('create two new jobs to the queue', () => {
        // Test for creating two new jobs in the queue
        const jobs = [
            { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
            { phoneNumber: '4153518781', message: 'This is the code 5678 to verify your account' }
        ];
        createPushNotificationsJobs(jobs, queue);

        // Assert that two jobs were created in the queue
        expect(queue.testMode.jobs.length).to.equal(2);
        expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
        expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
    });
});
