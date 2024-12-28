import time
# import queue

class RateLimiterWithQueue:
    def __init__(self, max_requests = 1, time_window = 2):
        """
        Initialize the rate limiter with a request queue.
        
        :param max_requests: Maximum allowed requests per IP per time window.
        :param time_window: Time window in seconds.
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.ip_requests = {}  # Tracks timestamps of requests per IP
        # self.ip_queues = {}    # Queues for excess requests per IP

    def is_allowed(self, ip = 'localhost'):
        """
        Check if the IP is allowed to make a request.
        
        :param ip: The client's IP address.
        :return: Boolean indicating if the request is allowed.
        """
        current_time = time.time()

        if ip not in self.ip_requests:
            # Initialize request tracking and queue for the IP
            self.ip_requests[ip] = []
            # self.ip_queues[ip] = queue.Queue()

        # Filter out timestamps outside the current time window
        self.ip_requests[ip] = [
            timestamp for timestamp in self.ip_requests[ip]
            if current_time - timestamp < self.time_window
        ]

        if len(self.ip_requests[ip]) < self.max_requests:
            # Allow the request and log the timestamp
            self.ip_requests[ip].append(current_time)
            return True
        else:
            for x in range(self.time_window, 0, -1):
                print(f"Processed queued request for IP: {ip}, witing time {x}s...") #, end='\r')
                time.sleep(1)
            return True
            # # Deny the request and enqueue it for the next window
            # self.ip_queues[ip].put(current_time)
            # return False

    # def process_queue(self, ip = 'localhost'):
    #     """
    #     Process queued requests for an IP when the time window resets.
        
    #     :param ip: The client's IP address.
    #     """
    #     current_time = time.time()
    #     while not self.ip_queues[ip].empty() and len(self.ip_requests[ip]) < self.max_requests:
    #         timestamp = self.ip_queues[ip].get()
    #         if current_time - timestamp < self.time_window:
    #             # Add the request to the current time window
    #             self.ip_requests[ip].append(timestamp)
    #             print(f"Processed queued request for IP {ip}")





