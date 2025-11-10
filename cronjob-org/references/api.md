# Cronjob-Org - Api

**Pages:** 1

---

## REST API — cron-job.org documentation

**URL:** https://docs.cron-job.org/rest-api.html

**Contents:**
- REST API
- Introduction
- Limitations
- Requests
  - Endpoint
  - Authentication
  - Content Type
  - HTTP Status Codes
  - Examples
- API Methods

cron-job.org provides an API which enables users to programatically create, update, delete and view cron jobs. The API provides a REST-like interface with API-key based authorization and JSON request and response payload. Given this, the API should be easily usable from virtually any programming language.

In order to prevent abuse of our service, we enforce a daily usage limit. By default, this limit is 100 requests per day, but can be increased upon request. For sustaining members, a higher limit of 5,000 requests per day applies.

Apart from the daily request limit, individual rate limits might apply depending on the specific API call made. Those limits are mentioned in the documentation of the specific API method.

The API endpoint is reachable via HTTPS at:

All requests to the API must be authenticated via an API key supplied in the Authorization bearer token header. API keys can be retrieved/generated in the cron-job.org Console at “Settings”. An example header could look like:

Access via a specific API key might be restricted to certain IP addresses, if configured in the Console. In this case, requests from non-allowlisted IP addresses will be rejected with an HTTP error code of 403.

API keys are secrets, just like a password. They allow access to your cron-job.org account via the API and should always be treated confidentially. We highly recommend to also enable the IP address restriction whenever possible.

In case a request requires a payload, it must be JSON-encoded and the Content-Type header must be set to application/json. In case the Content-Type header is missing or contains a different value, the request payload will be ignored.

The following status codes can be returned by the API:

OK: Request succeeded

Bad request: Invalid request / invalid input data

Unauthorized: Invalid API key

Forbidden: API key cannot be used from this origin

Not found: The requested resource could not be found

Conflict, e.g. because a resource already exists

API key quota, resource quota or rate limit exceeded

Internal server error

Example request via curl:

Example request via Python:

List all jobs in this account:

List of jobs present in the account

true in case some jobs could not be retrieved because of internal errors and the list might be incomplete, otherwise false

Max. 5 requests per second.

Retrieve detailed information for a specific cron job identified by its jobId:

Max. 5 requests per second.

Creating a new cron job:

Job (only the url field is mandatory)

Identifier of the created job

Max. 1 request per second and 5 requests per minute.

Updating a cron job identified by its jobId:

Job delta (only include changed fields - unchanged fields can be left out)

Max. 5 requests per second.

Deleting a cron job identified by its jobId:

Max. 5 requests per second.

Retrieve the execution history for a specific cron job identified by its jobId:

The last execution history items

Unix timestamps (in seconds) of the predicted next executions (up to 3)

Please note that the headers and body fields of the HistoryItem objects will not be populated. In order to retrieve headers and body, see Retrieving Job Execution History Item Details.

Max. 5 requests per second.

Retrieve details for a specific history item identified by its identifier for a specific cron job identified by its jobId:

Max. 5 requests per second.

The Job object represents a cron job.

Job identifier (read only; ignored during job creation or update)

Whether the job is enabled (i.e. being executed) or not

Whether to save job response header/body or not

Last execution status (read only)

0 (Unknown / not executed yet)

Last execution duration in milliseconds (read only)

Unix timestamp of last execution (in seconds; read only)

Unix timestamp of predicted next execution (in seconds), null if no prediction available (read only)

Job timeout in seconds

-1 (i.e. use default timeout)

Whether to treat 3xx HTTP redirect status codes as success or not

The identifier of the folder this job resides in

* Value when field is omitted while creating a job.

The DetailedJob object represents a cron job with detailed settings. It consists of all members of the Job object plus the following additional fields.

HTTP authentication settings

JobNotificationSettings

Notification settings

Extended request data

The JobAuth object represents HTTP (basic) authentication settings for a job.

Whether to enable HTTP basic authentication or not.

HTTP basic auth username

HTTP basic auth password

* Value when field is omitted while creating a job.

The JobNotificationSettings specifies notification settings for a job.

Whether to send a notification on job failure or not.

How many failures are required before a notification is sent (min 1).

Whether to send a notification when the job succeeds after a prior failure or not.

Whether to send a notification when the job has been disabled automatically or not.

* Value when field is omitted while creating a job.

The JobExtendedData holds extended request data for a job.

Request headers (key-value dictionary)

* Value when field is omitted while creating a job.

Unknown / not executed yet

Failed (could not connect to host)

Failed (too much response data)

Failed (internal errors)

Failed (unknown reason)

Monitoring job (used in a status monitor)

The JobSchedule object represents the execution schedule of a job.

Schedule time zone (see here for a list of supported values)

Date/time (in job’s time zone) after which the job expires, i.e. after which it is not scheduled anymore (format: YYYYMMDDhhmmss, 0 = does not expire)

Hours in which to execute the job (0-23; [-1] = every hour)

Days of month in which to execute the job (1-31; [-1] = every day of month)

Minutes in which to execute the job (0-59; [-1] = every minute)

Months in which to execute the job (1-12; [-1] = every month)

Days of week in which to execute the job (0=Sunday - 6=Saturday; [-1] = every day of week)

* Value when field is omitted while creating a job.

The HistoryItem object represents a job history log entry corresponding to one execution of the job.

Identifier of the associated cron job

Identifier of the history item

Unix timestamp (in seconds) of the actual execution

Unix timestamp (in seconds) of the planned/ideal execution

Scheduling jitter in milliseconds

Job URL at time of execution

Actual job duration in milliseconds

Detailed job status Description

HTTP status code returned by the host, if any

Raw response headers returned by the host (null if unavailable)

Raw response body returned by the host (null if unavailable)

Additional timing information for this request

The HistoryItemStats object contains additional timing information for a job execution history item.

Time from transfer start until name lookups completed (in microseconds)

Time from transfer start until socket connect completed (in microseconds)

Time from transfer start until SSL handshake completed (n microseconds) - 0 if not using SSL

Time from transfer start until beginning of data transfer (in microseconds)

Time from transfer start until the first response byte is received (in microseconds)

Total transfer time (in microseconds)

---
