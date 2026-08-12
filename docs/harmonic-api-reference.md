# Harmonic API reference

## Introduction

Welcome to the Harmonic API. These guides are designed to help you get up and running quickly.

Harmonic's API is moving to V2. All new features (starting with the [Workspace API](/docs/api-reference/workspace/getting-started)) will be built exclusively on V2 — see [Migrating to V2](/docs/api-reference/workspace/migration) for what's changing and how to move over.

Most endpoints support both REST and GraphQL. If you're using GraphQL, you can explore available schemas, queries, and mutations with our [GraphQL Explorer](/docs/graphql-reference/explorer).

Detailed company funding rounds and investor data are available as a **paid add-on**.

For high-volume use cases, we also offer a weekly refreshed bulk dataset through Snowflake, Amazon S3, and BigQuery.

For questions, feedback, or to learn more about paid add-ons or bulk data offering, reach out at [support@harmonic.ai](mailto:support@harmonic.ai).

### Authentication

To authenticate your request, set the `apikey` header to your team's API key. Passing the key as a query parameter is also supported, but headers are more secure because they keep the key out of URLs, server logs, and browser history.

**Using headers (recommended)**

```bash
curl -X 'POST' \
  'https://api.harmonic.ai/companies?website_domain=harmonic.ai' \
  -H 'accept: application/json' \
  -H 'apikey: yourkey'
```

**Using query parameter**

```bash
curl -X 'POST' \
  'https://api.harmonic.ai/companies?website_domain=harmonic.ai&apikey=yourkey' \
  -H 'accept: application/json'
```

### Pagination

Endpoints that may return a large number of results accept pagination query parameters so you can request results in batches.

**Cursor-based pagination request params:**

| Parameter | Type    | Default value | Description                                                                                             |
| --------- | ------- | ------------- | ------------------------------------------------------------------------------------------------------- |
| `size`    | integer | 50            | The number of results to return. Default: 50                                                            |
| `cursor`  | string  | None          | Cursor indicating where to pick up returning results from. Default: none (returns first `size` results) |

**Cursor-based pagination response params:**

| Parameter              | Type   | Description                               |
| ---------------------- | ------ | ----------------------------------------- |
| `has_next` / `hasNext` | bool   | Whether there are more results to request |
| `cursor`               | string | Cursor indicating where to continue       |
| `next`                 | string | Token to pass as the next cursor value    |

#### REST

Request

```
GET https://api.harmonic.ai/saved_searches:results/48142?apikey=xyz&size=50
```

Response

```
{
  "count": 534,
  "page_info": {
    "current": "",
    "next": "abc",
    "has_next": true
  },
  ...
}
```

**Requesting subsequent pages**

Pass the **next** token from the response as the **cursor** into the next request

**Request**

```
GET https://api.harmonic.ai/saved_searches:results/48142?apikey=xyz&cursor=abc&size=50
```

#### GraphQL

Request

```
POST https://api.harmonic.ai/graphql
```

Query

```
query GetCompaniesWithMetadataInSavedSearchesByIdOrUrn($idOrUrn: String!, $cursor: String, $size: Int) {
  getCompaniesWithMetadataInSavedSearchesByIdOrUrn(idOrUrn: $idOrUrn, cursor: $cursor, size: $size) {
    pageInfo {
      current
      hasNext
      next
    }
    count
    companies {
      headcount
      name
      id
    }
  }
}
```

Response

```
{
  "data": {
    "getCompaniesWithMetadataInSavedSearchesByIdOrUrn": {
      "pageInfo": {
        "next": "def",
        "current": "abc",
        "hasNext": true
      },
      "count": 2157,
      "companies": {...}
    }
  }
}
```

**Requesting subsequent pages**

Pass the **next** token from the response as the **cursor** into the next request

**Subsequent call**

```
query GetCompaniesWithMetadataInSavedSearchesByIdOrUrn($idOrUrn: String!, $cursor: String, $size: Int) {
  getCompaniesWithMetadataInSavedSearchesByIdOrUrn(idOrUrn: "1", cursor: "def", size: 10) {
    pageInfo {
      current
      hasNext
      next
    }
    count
    companies {
      headcount
      name
      id
    }
  }
}
```

#### first / after cursor pagination

A few relay-style connection endpoints — the [network mapping](/docs/api-reference/network/companies-in-network) queries (`getCompaniesInNetwork`, `getPeopleInNetwork`) — paginate with `first` and `after` instead of `cursor` / `size`. Pass `first` to control the page size, then pass the `endCursor` from the previous response's `pageInfo` as `after` to fetch the next page. Repeat until `pageInfo.hasNextPage` is `false`.

**Request**

```
POST https://api.harmonic.ai/graphql
```

**First page**

```
query GetCompaniesInNetwork($first: Int, $after: String) {
  getCompaniesInNetwork(first: $first, after: $after) {
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      cursor
      node {
        ... on Company {
          id
          name
        }
      }
    }
  }
}
```

Variables

```
{
  "first": 10
}
```

**Next page**

Pass the `endCursor` from the previous response's `pageInfo` as `after`:

```
{
  "first": 10,
  "after": "YXJyYXljb25uZWN0aW9uOjk="
}
```

##### Nested People

The nested **people** field within a company will contain at most 60 active employees.

The ordering of the up to 60 returned is: founders → executives → employees, sorted by most to least tenured.

To paginate all active employees for a company, use the ["Get employees from company" endpoint](/docs/api-reference/fetch/employees).

### Rate limit

Harmonic rate limits API access to a maximum of 10 requests per second for most endpoints. If you exceed the limit for an endpoint, you receive an HTTP 429 response.

A few endpoints have their own, lower limits:

| Endpoint                                         | Rate limit                            |
| ------------------------------------------------ | ------------------------------------- |
| `/search/search_agent` (natural-language search) | 5 requests per minute                 |
| `/scout/tasks` (Scout task creation)             | 10 requests per minute (100 per hour) |

Every API response includes rate limit status headers:

| Header                         | Description                                                     |
| ------------------------------ | --------------------------------------------------------------- |
| `X-Ratelimit-Limit-Second`     | Maximum number of requests allowed per second                   |
| `X-Ratelimit-Remaining-Second` | Remaining number of requests you can make in the current second |

**Example Response:**

```
HTTP/1.1 200 OK
Content-Type: application/json
X-Ratelimit-Limit-Second: 10
X-Ratelimit-Remaining-Second: 5

{
  "message": "API response content"
}
```

### Responses & errors

Our API returns standard HTTP success or error status codes. For errors, we will also include extra information about what went wrong encoded in the response as JSON. The various HTTP status codes we might return are listed below.

**Note:** We only count successful 200 responses toward your API usage limit.

#### Status codes

|                                 |                                                                                                                                                                      |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **200 - OK**                    | Everything worked as expected. You have latest data.                                                                                                                 |
| **201 - Enrichment Triggered**  | Entity exists in our system and the enrichment was triggered to update the data. Please check back in few hours for the update.                                      |
| **400 - Bad request**           | The request was unacceptable, often due to missing a required parameter.                                                                                             |
| **402 - Over quota**            | Over plan quota on this endpoint.                                                                                                                                    |
| **403 - Forbidden**             | No valid API key provided or the entity being accessed is private. Make sure to set any list or search to Shared in the console before accessing via the API.        |
| **404 - Not Found**             | The requested resource doesn't exist. If this is an enrich endpoint, the enrichment was triggered to update the data. Please check back in few hours for the update. |
| **422 - Validation error**      | A validation error occurred.                                                                                                                                         |
| **429 - Too many requests**     | The rate limit was exceeded.                                                                                                                                         |
| **50X - Internal Server Error** | An error occurred with our API.                                                                                                                                      |

## Enrich

Enrich endpoints accept a company or person identifier and return a comprehensive data profile. Use these to pull data into your CRM, data warehouse, or internal tools.

### Enrich a company

This endpoint accepts the following identifiers for the same company as query params (and at most one of each type). Do not include identifiers for different companies. To enrich multiple companies you must call this API for each company separately.

**POST** `https://api.harmonic.ai/companies`

| Name | Type |
| --- | --- |
| `website_url` | string |
| `website_domain` | string |
| `linkedin_url` | string |
| `crunchbase_url` | string |
| `pitchbook_url` | string |
| `twitter_url` | string |
| `instagram_url` | string |
| `facebook_url` | string |
| `angellist_url` | string |
| `monster_url` | string |
| `indeed_url` | string |
| `stackoverflow_url` | string |

Response Codes:

- **200** = company exists; the company profile is returned. If the record hasn't been updated in ~2 weeks, a refresh is triggered automatically in the background — the response is still 200 with the existing data. The body includes a top-level `enrichment_urn` field: a URN when a refresh is pending for this company (whether your request triggered it or one was already in flight), or `null` when the record is fresh and nothing is pending. Either way the returned profile is the current data — a pending refresh only means updated data may land in a few hours
- **404** = company does not exist in our database yet. Enrichment has been triggered, and the response body contains the URN to track it:

```json
{
  "detail": {
    "message": "Company not found; scheduled for enrichment, check back in a few hours. Use /enrichment_status endpoint to get status of the enrichment.",
    "enrichment_urn": "urn:harmonic:enrichment:<id>"
  }
}
```

Please use the [enrichment status endpoint](/docs/api-reference/enrich/status) with the `enrichment_urn` from a 200 or 404 response to track the enrichment progress.

**GraphQL:** the `enrichCompanyByIdentifiers` mutation always responds with HTTP 200. A company not yet in our database is returned as `companyFound: false` with `company: null`, and the tracking URN is exposed as `enrichmentUrn` — make sure to include `enrichmentUrn` in your selection set, otherwise it will not appear in the response. When `companyFound` is `true`, `enrichmentUrn` mirrors the REST behavior above: set when a refresh is pending, `null` otherwise.

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/companies`

```json
{
    "entity_urn": "urn:harmonic:company:123456",
    "id": 123456,
    "initialized_date": "2020-10-27T08:07:20.940106",
    "website": {...},
    "customer_type": "B2C",
    "logo_url": "string",
    "name": "string",
    "legal_name": "string",
    "description": "string",
    "external_description": "string",
    "short_description": "string",
    "founding_date": {...},
    "headcount": 0,
    "ownership_status": "PRIVATE",
    "company_type": "UNKNOWN",
    "stage": "SEED",
    "location": {...},
    "contact": {...},
    "socials": {...},
    "funding": {...},
    "people": [...], // returns first 60. See "Pagination > Nested People"
    "tags": [...],
    "tags_v2": [...],
    "funding_attribute_null_status": "EXISTS_BUT_UNDISCLOSED",
    "highlights": [...],
    "snapshots": [...],
    "traction_metrics": [...],
    "website_domain_aliases": [...],
    "name_aliases":[...],
    "employee_highlights": [...],
    "num_notable_followers": 84,
    "notable_followers": [...],
    "funding_rounds": [...],
    "investor_urn": "urn:harmonic:investor:203005",
    "related_companies": {...}
}
```

**GraphQL query**

```graphql
mutation($identifiers: CompanyEnrichmentIdentifiersInput!) {
  enrichCompanyByIdentifiers(identifiers: $identifiers) {
    companyFound
    enrichmentUrn
    company {
      entityUrn
      website {
        url
      }
      funding {
        fundingTotal
        fundingStage
        numFundingRounds
        lastFundingAt
        investors {
          ... on Company {
            name
          }
          ... on Person {
            fullName
          }
        }
        fundingRounds {
          entityUrn
          announcementDate
          fundingRoundType
          fundingAmount
          fundingCurrency
          sourceUrl
          investors {
            investorName
            isLead
            entityUrn
          }
        }
      }
      numNotableFollowers
      notableFollowers(first: 2) {
        followerName
        followerUrn
        firmName
        firmUrn
        followedName
        followedUrn
        followObservedAt
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "identifiers": {"linkedinUrl": "https://www.linkedin.com/company/9fin"}
}
```

### Enrich a person

Pass in a person identifier and get back their profile with experiences, education and other information. This endpoint accepts the following identifiers as query params.

**POST** `https://api.harmonic.ai/persons`

| Name | Type |
| --- | --- |
| `linkedin_url` | string |
| `email` | string |

Response Codes:

- **200** = person exists and is fresh (refreshed within the last ~30 days); the person profile is returned
- **201** = person exists but an enrichment job for them is queued or in progress (typically because the record hasn't been refreshed in ~30 days and this request triggered a refresh). The body is identical to the 200 response — the existing profile; check back in a few hours for updates
- **404** = person does not exist in our database yet. Enrichment has been triggered, and the response body contains the URN to track it:

```json
{
  "detail": {
    "message": "Person not found; scheduled for enrichment, check back in a few hours. Use /enrichment_status endpoint to get status of the enrichment.",
    "enrichment_urn": "urn:harmonic:enrichment:<id>"
  }
}
```

Successful responses (200 and 201) also include a top-level `enrichment_urn` (the identifier of the most recent enrichment request for this person) and `merged_person_urn` (set when the person was merged into another profile, otherwise `null`).

Please use the [enrichment status endpoint](/docs/api-reference/enrich/status) with the `enrichment_urn` to track the enrichment progress.

**GraphQL:** the `enrichPersonByIdentifiers` mutation always responds with HTTP 200. A person not yet in our database is returned as `personFound: false` with `person: null`, and the tracking URN is exposed as `enrichmentUrn` on the payload — make sure to include `enrichmentUrn` in your selection set, otherwise it will not appear in the response.

**Note:** If a company ID is -1, that means we don't yet have a canonical company record for that company. The API will not return data for these companies.

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/persons`

```json
{
    "full_name": "Richard Hendricks",
    "first_name": "Richard",
    "last_name": "Hendricks",
    "profile_picture_url": "string",
    "contact": {...},
    "location": {...},
    "education": [...],
    "socials": {...},
    "experience": [...],
    "highlights": [...],
    "num_notable_followers": 42,
    "notable_followers": [...],
    "linkedin_headline": "General Manager Hotel Concorde Old Bucharest",
    "entity_urn": "urn:harmonic:person:1",
    "awards__beta": [...],
    "recommendations__beta": [...],
    "current_company_urns": [...],
    "linkedin_profile_visibility_type": "string",
    "last_refreshed_at": "string",
    "last_checked_at": "string",
    "languages": [...],
}
```

**GraphQL query**

```graphql
mutation EnrichPersonByIdentifiers($identifiers: PersonEnrichmentIdentifiersInput!) {
  enrichPersonByIdentifiers(identifiers: $identifiers) {
    personFound
    enrichmentUrn
    person {
      entityUrn
      id
      fullName
      firstName
      lastName
      about
      profilePictureUrl
      socials {
        linkedin {
          url
        }
      }
      highlights {
        category
        text
      }
      numNotableFollowers
      notableFollowers(first: 2) {
        followerName
        followerUrn
        firmName
        firmUrn
        followedName
        followedUrn
        followObservedAt
      }
      awardsBeta
      currentCompanyUrns
      enrichmentUrn
      linkedinHeadline
      linkedinProfileVisibilityType
      lastRefreshedAt
      lastCheckedAt
    }
  }
}
```

**GraphQL variables**

```json
{
  "identifiers": {"linkedinUrl": "https://www.linkedin.com/in/josh-chacona-31346317/"}
}
```

### Get enrichment status

Pass in a list of enrichment IDs or URNs, and get back a full picture of those statuses.

ID example:

```
242437b6-eb4d-476b-b348-3c1bcc2d7069
```

URN example:

```
urn:harmonic:enrichment:242437b6-eb4d-476b-b348-3c1bcc2d7069
```

**GET** `https://api.harmonic.ai/enrichment_status`

| Name | Type |
| --- | --- |
| `ids` | array[string] |
| `urns` | array[string] |

##### Example request

`ids` and `urns` are repeated for each value in the query string:

```bash
curl -G "https://api.harmonic.ai/enrichment_status" \
  -H "apikey: yourkey" \
  -d "ids=242437b6-eb4d-476b-b348-3c1bcc2d7069" \
  -d "urns=urn:harmonic:enrichment:242437b6-eb4d-476b-b348-3c1bcc2d7069"
```

This resolves to:

`GET https://api.harmonic.ai/enrichment_status?ids=242437b6-eb4d-476b-b348-3c1bcc2d7069&urns=urn:harmonic:enrichment:242437b6-eb4d-476b-b348-3c1bcc2d7069`

Response Statuses:

- **QUEUED**: Enrichment has been scheduled. Please check back in a few hours.
- **IN_PROGRESS**: Enrichment is in progress. Please check back in a few hours.
- **COMPLETE**: Enrichment is complete. The entity is updated or created.
- **FAILED**: Unfortunately, enrichment has failed. Our support team will look into this.
- **NOT_FOUND**: Unfortunately, the profile does not exist or is private and we are unable to get data.

Enriched entity urn in response can either be for company or person depending on original enrichment request type.

**REST**

`GET https://api.harmonic.ai/enrichment_status`

```json
[
  {
      "entity_urn": "urn:harmonic:enrichment:0d9aa949-235c-4d48-bb90-8cf716db0556",
      "status": "COMPLETE",
      "message": "Enrichment is complete. Please use entity endpoints: /company or /person, to get the results",
      "enriched_entity_urn": "urn:harmonic:company:1"
  },
  {
      "entity_urn": "urn:harmonic:enrichment:242437b6-eb4d-476b-b348-3c1bcc2d7069",
      "status": "QUEUED",
      "message": "Enrichment has been scheduled. Please check back in few hours",
      "enriched_entity_urn": null
  }
]
```

### Submit a bulk email enrichment job

Submit up to 5,000 people in a single call to enrich their emails. Inputs can be raw LinkedIn profile URLs or Harmonic person URNs (provide exactly one of the two arrays). The endpoint canonicalizes URLs, resolves identifiers, filters eligibility, reserves quota against your monthly limit, and returns a job ID you can poll with [Get bulk email job status](/docs/api-reference/enrich/bulk-email-status).

**POST** `https://api.harmonic.ai/email_enrichment/jobs`

Provide exactly one of the two arrays. Each accepts between 1 and 5,000 entries. Inputs that resolve to the same internal person are silently deduplicated.

| Name | Type |
| --- | --- |
| `person_linkedin_urls` | array[string] |
| `person_urns` | array[string] |

##### Example request

Provide exactly one of the two arrays:

```json
{
  "person_linkedin_urls": [
    "https://www.linkedin.com/in/jane-doe/",
    "https://www.linkedin.com/in/john-smith/"
  ]
}
```

Or, using Harmonic person URNs:

```json
{
  "person_urns": ["urn:harmonic:person:315637", "urn:harmonic:person:12345"]
}
```

#### Drop reasons

People filtered out at submit time are returned in the `dropped` array with one of:

- **NOT_FOUND**: the LinkedIn URL didn't resolve to any known person.
- **INVALID_URL**: the input wasn't a recognizable LinkedIn profile URL.
- **ALREADY_HAS_EMAIL**: the person already has an email recorded.
- **RECENTLY_ATTEMPTED**: the person was attempted within the 30-day cooldown window. Retry after the cooldown expires.

#### Errors

- **422 NO_ELIGIBLE_PEOPLE**: every submitted person was dropped. Response body includes the per-input `dropped` array explaining why.
- **429 MONTHLY_QUOTA_INSUFFICIENT**: the request requires more credits than remain in your monthly quota. Response body includes `needed`, `available`, and `submitted`. Retry with fewer inputs or wait for the next monthly reset.

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/email_enrichment/jobs`

```json
{
  "job_id": "0d9aa949-235c-4d48-bb90-8cf716db0556",
  "status": "PENDING",
  "accepted_count": 1,
  "dropped": [ ... ],
  "monthly_remaining": 4999,
  "created_at": "2026-05-07T15:30:00Z"
}
```

**GraphQL query**

```graphql
mutation SubmitBulkEmailEnrichmentJob($input: BulkEmailEnrichmentJobInput!) {
  submitBulkEmailEnrichmentJob(input: $input) {
    jobId
    status
    acceptedCount
    monthlyRemaining
    createdAt
    dropped {
      submittedIdentifier
      reason
    }
  }
}
```

**GraphQL variables**

```json
{
  "input": {
    "personLinkedinUrls": [
      "https://www.linkedin.com/in/josh-chacona-31346317/",
      "https://www.linkedin.com/in/satyanadella/"
    ]
  }
}
```

### Get bulk email job status

Poll a bulk email enrichment job by the `job_id` returned from [Submit a bulk email enrichment job](/docs/api-reference/enrich/bulk-email-submit). The response always includes per-status counts. The `results` array is `null` until the job reaches a terminal status (`COMPLETED` or `FAILED`); once terminal, all per-person results are returned in a single response.

**GET** `https://api.harmonic.ai/email_enrichment/jobs/{job_id}`

#### Job statuses

- **PENDING**: the job is queued and waiting to start.
- **IN_PROGRESS**: enrichment is running. Poll again in a few seconds.
- **COMPLETED**: the job finished. `results` is populated with one entry per accepted person.
- **FAILED**: the job hit a fatal error. `results` is populated with whatever items processed before the failure.

#### Per-item statuses

- **PENDING**: not yet processed.
- **SUCCESS**: an email was found and is now available on the person's profile.
- **NOT_FOUND**: no email could be found for this person.
- **FAILED**: enrichment errored for this person.
- **SKIPPED**: the person became ineligible after submit (rare — typically only on race conditions).

To fetch the resolved emails, call [Get a person](/docs/api-reference/fetch/person-by-id) with the returned `person_urn` once the job is `COMPLETED`.

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/email_enrichment/jobs/{job_id}`

```json
{
  "job_id": "0d9aa949-235c-4d48-bb90-8cf716db0556",
  "status": "COMPLETED",
  "counts": { ... },
  "results": [ ... ],
  "created_at": "2026-05-07T15:30:00Z",
  "completed_at": "2026-05-07T15:32:14Z"
}
```

**GraphQL query**

```graphql
query GetBulkEmailEnrichmentJob($jobId: ID!) {
  getBulkEmailEnrichmentJob(jobId: $jobId) {
    jobId
    status
    createdAt
    completedAt
    counts {
      totalProcessed
      totalSucceeded
      totalFailed
      totalSkipped
      totalNotFound
    }
    results {
      personUrn
      status
    }
  }
}
```

**GraphQL variables**

```json
{
  "jobId": "0d9aa949-235c-4d48-bb90-8cf716db0556"
}
```

### Get bulk email usage

Returns your team's current monthly email enrichment quota state. Use this before submitting a large batch to avoid 429 responses, or to surface remaining capacity in your tooling. The counters reset at the start of each calendar month.

**GET** `https://api.harmonic.ai/email_enrichment/usage`

#### Response fields

- **monthly_usage**: emails enriched so far this month.
- **monthly_limit**: total emails your team can enrich each month.
- **monthly_remaining**: `monthly_limit - monthly_usage`.

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/email_enrichment/usage`

```json
{
  "monthly_usage": 1247,
  "monthly_limit": 5000,
  "monthly_remaining": 3753
}
```

**GraphQL query**

```graphql
query GetBulkEmailEnrichmentUsage {
  getBulkEmailEnrichmentUsage {
    monthlyUsage
    monthlyLimit
    monthlyRemaining
  }
}
```

## Fetch

Fetch endpoints retrieve company and person records by their Harmonic ID. Use these when you already have an entity ID and need to look up its data.

### Get company by ID

Pass in a company ID, and get back a full picture of that company. You can use either the int ID, or the full URN.

ID example:

```
GET https://api.harmonic.ai/companies/123456
```

URN example:

```
GET https://api.harmonic.ai/companies/urn:harmonic:company:123456
```

**GET** `https://api.harmonic.ai/companies/{id_or_urn}`

| Name | Type | Description |
| --- | --- | --- |
| `include_fields` | array[string] | Optional. Specify which fields from the output schema should be included in the response for better performance. When used (e.g. ["id", "name", "website_url"]), only those fields have populated values — every other field in the profile is null. See the [list of valid field names](https://support.harmonic.ai/en/articles/10657032-company-and-people-lists-api-data-fields). |

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/companies/{id_or_urn}`

```json
{
    "entity_urn": "urn:harmonic:company:123456",
    "id": 123456,
    "initialized_date": "2020-10-27T08:07:20.940106",
    "website": {...},
    "customer_type": "B2C",
    "logo_url": "string",
    "name": "string",
    "legal_name": "string",
    "description": "string",
    "external_description": "string",
    "short_description": "string",
    "founding_date": {...},
    "headcount": 0,
    "ownership_status": "PRIVATE",
    "company_type": "UNKNOWN",
    "stage": "SEED",
    "location": {...},
    "contact": {...},
    "socials": {...},
    "funding": {...},
    "people": [...], // returns first 60. See "Pagination > Nested People"
    "tags": [...],
    "tags_v2": [...],
    "funding_attribute_null_status": "EXISTS_BUT_UNDISCLOSED",
    "highlights": [...],
    "snapshots": [...],
    "traction_metrics": [...],
    "website_domain_aliases": [...],
    "name_aliases":[...],
    "employee_highlights": [...],
    "num_notable_followers": 84,
    "notable_followers": [...],
    "funding_rounds": [...],
    "investor_urn": "urn:harmonic:investor:203005",
    "related_companies": {...}
}
```

**GraphQL query**

```graphql
query Query($getCompanyByIdId: Int!) {
  getCompanyById(id: $getCompanyByIdId) {
    companyType
    contact {
      emails
      phoneNumbers
    }
    description
    entityUrn
    foundingDate {
      date
      granularity
    }
    funding {
      fundingTotal
      numFundingRounds
      lastFundingAt
      lastFundingType
      lastFundingTotal
      investors {
        ... on Company {
          name
        }
        ... on Person {
          fullName
        }
      }
      fundingRounds {
        entityUrn
        announcementDate
        fundingRoundType
        fundingAmount
        fundingCurrency
        sourceUrl
        postMoneyValuation
        investors {
          investorName
          isLead
          entityUrn
        }
      }
    }
    websiteDomainAliases
    nameAliases
    fundingAttributeNullStatus
    id
    logoUrl
    legalName
    name
    ownershipStatus
    headcount
    stage
    highlights {
      text
      category
    }
    numNotableFollowers
    notableFollowers(first: 2) {
      followerName
      followerUrn
      firmName
      firmUrn
      followedName
      followedUrn
      followObservedAt
    }
    initializedDate
    location {
      country
      zip
      state
      city
      street
      location
      addressFormatted
    }
    employees {
      entityUrn
      fullName
      firstName
      lastName
      profilePictureUrl
      contact {
        phoneNumbers
        emails
      }
      location {
        country
        zip
        state
        city
        street
        location
        addressFormatted
      }
      education {
        endDate
        startDate
        grade
        field
        degree
        school {
          name
          websiteUrl
          linkedinUrl
          logoUrl
          entityUrn
        }
      }
      experience {
        location
        isCurrentPosition
        endDate
        startDate
        description
        title
        department
        contact {
          emails
          phoneNumbers
        }
      }
      awardsBeta
      recommendationsBeta
    }
    snapshots {
      name
    }
    socials {
       facebook {
        url
        followerCount
       }
       twitter {
        followerCount
        url
       }
       linkedin {
        followerCount
        url
       }
       instagram {
        followerCount
        url
       }
       crunchbase {
        url
        followerCount
       }
       pitchbook {
        followerCount
        url
       }
       angellist {
        followerCount
        url
       }
       indeed {
        followerCount
        url
       }
       youtube {
        followerCount
        url
       }
       monster {
        followerCount
        url
       }
       stackoverflow {
        url
        followerCount
       }
    }
    website {
      isBroken
      domain
      url
    }
    tags {
      type
      displayValue
      entityUrn
      dateAdded
    }
    userConnections {
      user {
        email
        name
      }
    }
    tractionMetrics {
      headcount {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      webTraffic {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountAdvisor {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountCustomerSuccess {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountMarketing {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountOther {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountProduct {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountSales {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountSupport {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountData {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountDesign {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountEngineering {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountFinance {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountOperations {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountLegal {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountPeople {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      facebookFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      linkedinFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      instagramFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      twitterFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
    }
    relatedCompanies {
      priorStealthAssociation {
        emergenceDate
        previouslyKnownAs
      }
    }
  }
}
```

**GraphQL variables**

```json
{"getCompanyByIdId": 1}
```

### Get companies by ID

Pass in a list of company IDs or URNs, and get back a full picture of those companies.

**GET** `https://api.harmonic.ai/companies`

| Name | Type | Description |
| --- | --- | --- |
| `ids` | array[integer] | - |
| `urns` | array[string] | - |
| `include_fields` | array[string] | Optional. Specify which fields from the output schema should be included in the response for better performance. When used (e.g. ["id", "name", "website_url"]), only those fields have populated values — every other field in the profile is null. See the [list of valid field names](https://support.harmonic.ai/en/articles/10657032-company-and-people-lists-api-data-fields). |

##### Example request

`ids` and `urns` are repeated for each value in the query string. Combine them with
`include_fields` to trim the payload:

```bash
curl -G "https://api.harmonic.ai/companies" \
  -H "apikey: yourkey" \
  -d "ids=2509609" \
  -d "ids=4923" \
  -d "urns=urn:harmonic:company:2509609" \
  -d "include_fields=id" \
  -d "include_fields=name" \
  -d "include_fields=website_url"
```

This resolves to:

`GET https://api.harmonic.ai/companies?ids=2509609&ids=4923&urns=urn:harmonic:company:2509609&include_fields=id&include_fields=name&include_fields=website_url`

**Limitations:** Endpoint has a limit of 50 companies.

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/companies`

```json
[
{
    "entity_urn": "urn:harmonic:company:123456",
    "id": 123456,
    "initialized_date": "2020-10-27T08:07:20.940106",
    "website": {...},
    "customer_type": "B2C",
    "logo_url": "string",
    "name": "string",
    "legal_name": "string",
    "description": "string",
    "external_description": "string",
    "short_description": "string",
    "founding_date": {...},
    "headcount": 0,
    "ownership_status": "PRIVATE",
    "company_type": "UNKNOWN",
    "stage": "SEED",
    "location": {...},
    "contact": {...},
    "socials": {...},
    "funding": {...},
    "people": [...], // returns first 60. See "Pagination > Nested People"
    "tags": [...],
    "tags_v2": [...],
    "funding_attribute_null_status": "EXISTS_BUT_UNDISCLOSED",
    "highlights": [...],
    "snapshots": [...],
    "traction_metrics": [...],
    "website_domain_aliases": [...],
    "name_aliases":[...],
    "employee_highlights": [...],
    "num_notable_followers": 84,
    "notable_followers": [...],
    "funding_rounds": [...],
    "investor_urn": "urn:harmonic:investor:203005",
    "related_companies": {...}
}]
```

**GraphQL query**

```graphql
query Query($getCompaniesByIdsIds: [Int!]!) {
  getCompaniesByIds(ids: $getCompaniesByIdsIds) {
    companyType
    contact {
      emails
      phoneNumbers
    }
    description
    entityUrn
    foundingDate {
      date
      granularity
    }
    funding {
      fundingTotal
      numFundingRounds
      lastFundingAt
      lastFundingType
      lastFundingTotal
      investors {
        ... on Company {
          name
        }
        ... on Person {
          fullName
        }
      }
      fundingRounds {
        entityUrn
        announcementDate
        fundingRoundType
        fundingAmount
        fundingCurrency
        sourceUrl
        postMoneyValuation
        investors {
          investorName
          isLead
          entityUrn
        }
      }
    }
    websiteDomainAliases
    nameAliases
    fundingAttributeNullStatus
    id
    logoUrl
    legalName
    name
    ownershipStatus
    headcount
    stage
    highlights {
      text
      category
    }
    numNotableFollowers
    notableFollowers(first: 2) {
      followerName
      followerUrn
      firmName
      firmUrn
      followedName
      followedUrn
      followObservedAt
    }
    initializedDate
    location {
      country
      zip
      state
      city
      street
      location
      addressFormatted
    }
    employees {
      entityUrn
      fullName
      firstName
      lastName
      profilePictureUrl
      contact {
        phoneNumbers
        emails
      }
      location {
        country
        zip
        state
        city
        street
        location
        addressFormatted
      }
      education {
        endDate
        startDate
        grade
        field
        degree
        school {
          name
          websiteUrl
          linkedinUrl
          logoUrl
          entityUrn
        }
      }
      experience {
        location
        isCurrentPosition
        endDate
        startDate
        description
        title
        department
        contact {
          emails
          phoneNumbers
        }
      }
      awardsBeta
      recommendationsBeta
    }
    snapshots {
      name
    }
    socials {
       facebook {
        url
        followerCount
       }
       twitter {
        followerCount
        url
       }
       linkedin {
        followerCount
        url
       }
       instagram {
        followerCount
        url
       }
       crunchbase {
        url
        followerCount
       }
       pitchbook {
        followerCount
        url
       }
       angellist {
        followerCount
        url
       }
       indeed {
        followerCount
        url
       }
       youtube {
        followerCount
        url
       }
       monster {
        followerCount
        url
       }
       stackoverflow {
        url
        followerCount
       }
    }
    website {
      isBroken
      domain
      url
    }
    tags {
      type
      displayValue
      entityUrn
      dateAdded
    }
    userConnections {
      user {
        email
        name
      }
    }
    tractionMetrics {
      headcount {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      webTraffic {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountAdvisor {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountCustomerSuccess {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountMarketing {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountOther {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountProduct {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountSales {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountSupport {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountData {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountDesign {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountEngineering {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountFinance {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountOperations {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountLegal {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountPeople {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      facebookFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      linkedinFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      instagramFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      twitterFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
    }
    relatedCompanies {
      priorStealthAssociation {
        emergenceDate
        previouslyKnownAs
      }
    }
  }
}
```

**GraphQL variables**

```json
{"getCompaniesByIdsIds": [1,7]}
```

### Batch get companies by ID

Pass in a list of company IDs or URNs, and get back a full picture of those companies.

**POST** `https://api.harmonic.ai/companies/batchGet`

| Name | Type | Description |
| --- | --- | --- |
| `ids` | array[integer] | - |
| `urns` | array[string] | - |
| `include_fields` | array[string] | Optional. Specify which fields from the output schema should be included in the response for better performance. When used (e.g. ["id", "name", "website_url"]), only those fields have populated values — every other field in the profile is null. See the [list of valid field names](https://support.harmonic.ai/en/articles/10657032-company-and-people-lists-api-data-fields). |

##### Example request

```json
{
  "ids": [2509609, 4923],
  "urns": ["urn:harmonic:company:2509609"],
  "include_fields": ["id", "name", "website_url"]
}
```

**Limitations:** Endpoint has a limit of 500 companies.

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/companies/batchGet`

```json
[
{
    "entity_urn": "urn:harmonic:company:123456",
    "id": 123456,
    "initialized_date": "2020-10-27T08:07:20.940106",
    "website": {...},
    "customer_type": "B2C",
    "logo_url": "string",
    "name": "string",
    "legal_name": "string",
    "description": "string",
    "external_description": "string",
    "short_description": "string",
    "founding_date": {...},
    "headcount": 0,
    "ownership_status": "PRIVATE",
    "company_type": "UNKNOWN",
    "stage": "SEED",
    "location": {...},
    "contact": {...},
    "socials": {...},
    "funding": {...},
    "people": [...], // returns first 60. See "Pagination > Nested People"
    "tags": [...],
    "tags_v2": [...],
    "funding_attribute_null_status": "EXISTS_BUT_UNDISCLOSED",
    "highlights": [...],
    "snapshots": [...],
    "traction_metrics": [...],
    "website_domain_aliases": [...],
    "name_aliases":[...],
    "employee_highlights": [...],
    "num_notable_followers": 84,
    "notable_followers": [...],
    "funding_rounds": [...],
    "investor_urn": "urn:harmonic:investor:203005",
    "related_companies": {...}
}]
```

**GraphQL query**

```graphql
query Query($getCompaniesByIdsIds: [Int!]!) {
  getCompaniesByIds(ids: $getCompaniesByIdsIds) {
    companyType
    contact {
      emails
      phoneNumbers
    }
    description
    entityUrn
    foundingDate {
      date
      granularity
    }
    funding {
      fundingTotal
      numFundingRounds
      lastFundingAt
      lastFundingType
      lastFundingTotal
      investors {
        ... on Company {
          name
        }
        ... on Person {
          fullName
        }
      }
      fundingRounds {
        entityUrn
        announcementDate
        fundingRoundType
        fundingAmount
        fundingCurrency
        sourceUrl
        postMoneyValuation
        investors {
          investorName
          isLead
          entityUrn
        }
      }
    }
    websiteDomainAliases
    nameAliases
    fundingAttributeNullStatus
    id
    logoUrl
    legalName
    name
    ownershipStatus
    headcount
    stage
    highlights {
      text
      category
    }
    numNotableFollowers
    notableFollowers(first: 2) {
      followerName
      followerUrn
      firmName
      firmUrn
      followedName
      followedUrn
      followObservedAt
    }
    initializedDate
    location {
      country
      zip
      state
      city
      street
      location
      addressFormatted
    }
    employees {
      entityUrn
      fullName
      firstName
      lastName
      profilePictureUrl
      contact {
        phoneNumbers
        emails
      }
      location {
        country
        zip
        state
        city
        street
        location
        addressFormatted
      }
      education {
        endDate
        startDate
        grade
        field
        degree
        school {
          name
          websiteUrl
          linkedinUrl
          logoUrl
          entityUrn
        }
      }
      experience {
        location
        isCurrentPosition
        endDate
        startDate
        description
        title
        department
        contact {
          emails
          phoneNumbers
        }
      }
      awardsBeta
      recommendationsBeta
    }
    snapshots {
      name
    }
    socials {
       facebook {
        url
        followerCount
       }
       twitter {
        followerCount
        url
       }
       linkedin {
        followerCount
        url
       }
       instagram {
        followerCount
        url
       }
       crunchbase {
        url
        followerCount
       }
       pitchbook {
        followerCount
        url
       }
       angellist {
        followerCount
        url
       }
       indeed {
        followerCount
        url
       }
       youtube {
        followerCount
        url
       }
       monster {
        followerCount
        url
       }
       stackoverflow {
        url
        followerCount
       }
    }
    website {
      isBroken
      domain
      url
    }
    tags {
      type
      displayValue
      entityUrn
      dateAdded
    }
    userConnections {
      user {
        email
        name
      }
    }
    tractionMetrics {
      headcount {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      webTraffic {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountAdvisor {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountCustomerSuccess {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountMarketing {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountOther {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountProduct {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountSales {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountSupport {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountData {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountDesign {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountEngineering {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountFinance {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountOperations {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountLegal {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountPeople {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      facebookFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      linkedinFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      instagramFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      twitterFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
    }
    relatedCompanies {
      priorStealthAssociation {
        emergenceDate
        previouslyKnownAs
      }
    }
  }
}
```

**GraphQL variables**

```json
{"getCompaniesByIdsIds": [1,7]}
```

### Get employees from company

This endpoint returns the urns of the employees from a given company.

**GET** `https://api.harmonic.ai/companies/{id_or_urn}/employees`

These are the parameters supported by the endpoint:

| Name | Type | Description |
| --- | --- | --- |
| `employee_group_type` | string | Represent specific group of employees to be retrieved. Supported values: ALL (default), FOUNDERS_AND_CEO, EXECUTIVES, FOUNDERS, LEADERSHIP, NON_LEADERSHIP, ADVISORS, NON_PARTNERS |
| `size` | number | The number of employees to return on each request. Default is 10. |
| `page` | number | The starting position from where to fetch the employees. Default is 0. |

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/companies/{id_or_urn}/employees`

```json
{
  "count": 53,
  "page_info": null,
  "results": [
    "urn:harmonic:person:155348322",
    "urn:harmonic:person:159049861",
    "urn:harmonic:person:182482",
    "urn:harmonic:person:102287",
    "urn:harmonic:person:369105",
    "urn:harmonic:person:168299092",
    "urn:harmonic:person:130139057",
    "urn:harmonic:person:70274429",
    "urn:harmonic:person:180603641",
    "urn:harmonic:person:114375482"
  ]
}
```

**GraphQL query**

```graphql
query GetCompanyEmployees($companyUrn: CompanyUrn!, $page: Int!, $size: Int!, $employeeGroupType: EmployeeGroupType!, $userConnectionStatus: UserConnectionStatus, $employeeStatus: EmployeeStatus) {
  getEmployeesByCompanyId(
    companyUrn: $companyUrn
    page: $page
    size: $size
    employeeGroupType: $employeeGroupType
    userConnectionStatus: $userConnectionStatus
    employeeStatus: $employeeStatus
  ) {
    totalCount
    edges {
      cursor
      node {
        ... on Person {
          id
          fullName
          firstName
          experience {
            title
            company {
              id
              name
              logoUrl
            }
            isCurrentPosition
            startDate
            endDate
          }
          education {
            school {
              name
            }
          }
        }
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "companyUrn": "urn:harmonic:company:1",
  "page": 0,
  "size": 50,
  "employeeGroupType": "ALL"
}
```

### Get person by ID

Pass in a person ID, and get back a full picture of that person. You can use either the int ID, or the full URN.

ID example:

```
GET https://api.harmonic.ai/persons/123456
```

URN example:

```
GET https://api.harmonic.ai/persons/urn:harmonic:person:123456
```

**Note:** If a company ID is -1, that means we don't yet have a canonical company record for that company. The API will not return data for these companies.

**GET** `https://api.harmonic.ai/persons/{id_or_urn}`

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/persons/{id_or_urn}`

```json
{
    "full_name": "Richard Hendricks",
    "first_name": "Richard",
    "last_name": "Hendricks",
    "profile_picture_url": "string",
    "contact": {...},
    "location": {...},
    "education": [...],
    "socials": {...},
    "experience": [...],
    "highlights": [...],
    "num_notable_followers": 42,
    "notable_followers": [...],
    "linkedin_headline": "General Manager Hotel Concorde Old Bucharest",
    "entity_urn": "urn:harmonic:person:1",
    "awards__beta": [...],
    "recommendations__beta": [...],
    "current_company_urns": [...],
    "linkedin_profile_visibility_type": "string",
    "last_refreshed_at": "string",
    "last_checked_at": "string",
    "languages": [...],
}
```

**GraphQL query**

```graphql
query Query($getPersonByIdId: Int!) {
  getPersonById(id: $getPersonByIdId) {
    fullName
    firstName
    lastName
    profilePictureUrl
    linkedinHeadline
    contact {
      emails
      phoneNumbers
    }
    location {
      addressFormatted
      location
      street
      city
      state
      zip
      country
    }
    education {
      school {
        name
        websiteUrl
        linkedinUrl
        logoUrl
        entityUrn
      }
      degree
      field
      grade
      startDate
      endDate
    }
    experience {
      location
      isCurrentPosition
      endDate
      startDate
      description
      title
      department
      contact {
        emails
        phoneNumbers
      }
      company {
        name
        funding {
          fundingTotal
        }
        foundingDate {
          date
        }
        socials {
          linkedin {
            url
          }
        }
      }
    }
    numNotableFollowers
    notableFollowers(first: 2) {
      followerName
      followerUrn
      firmName
      firmUrn
      followedName
      followedUrn
      followObservedAt
    }
    awardsBeta
    recommendationsBeta
    currentCompanyUrns
    entityUrn
    socials {
       facebook {
        url
        followerCount
       }
       twitter {
        followerCount
        url
       }
       linkedin {
        followerCount
        url
       }
       instagram {
        followerCount
        url
       }
       crunchbase {
        url
        followerCount
       }
       pitchbook {
        followerCount
        url
       }
       angellist {
        followerCount
        url
       }
       indeed {
        followerCount
        url
       }
       youtube {
        followerCount
        url
       }
       monster {
        followerCount
        url
       }
       stackoverflow {
        url
        followerCount
       }
    }
    recentJobUpdateStatus {
      date
      helperText
      type
    }
    linkedinProfileVisibilityType
    lastRefreshedAt
    lastCheckedAt
    languages {
      name
    }
  }
}
```

**GraphQL variables**

```json
{"getPersonByIdId": 1}
```

### Get persons by ID

Pass in a list of person IDs or URNs, and get back a full picture of those persons.

**Note:** If a company ID is -1, that means we don't yet have a canonical company record for that company. The API will not return data for these companies.

**GET** `https://api.harmonic.ai/persons`

| Name | Type |
| --- | --- |
| `ids` | array[integer] |
| `urns` | array[string] |

##### Example request

`ids` and `urns` are repeated for each value in the query string:

```bash
curl -G "https://api.harmonic.ai/persons" \
  -H "apikey: yourkey" \
  -d "ids=315637" \
  -d "ids=12345" \
  -d "urns=urn:harmonic:person:315637"
```

This resolves to:

`GET https://api.harmonic.ai/persons?ids=315637&ids=12345&urns=urn:harmonic:person:315637`

**Limitations:** Endpoint has a limit of 50 people.

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/persons`

```json
[
{
    "full_name": "Richard Hendricks",
    "first_name": "Richard",
    "last_name": "Hendricks",
    "profile_picture_url": "string",
    "contact": {...},
    "location": {...},
    "education": [...],
    "socials": {...},
    "experience": [...],
    "highlights": [...],
    "num_notable_followers": 42,
    "notable_followers": [...],
    "linkedin_headline": "General Manager Hotel Concorde Old Bucharest",
    "entity_urn": "urn:harmonic:person:1",
    "awards__beta": [...],
    "recommendations__beta": [...],
    "current_company_urns": [...],
    "linkedin_profile_visibility_type": "string",
    "last_refreshed_at": "string",
    "last_checked_at": "string",
    "languages": [...],
}]
```

**GraphQL query**

```graphql
query Query($getPersonByIdsIds: [Int!]!) {
  getPersonsByIds(ids: $getPersonByIdsIds) {
    fullName
    firstName
    lastName
    profilePictureUrl
    linkedinHeadline
    contact {
      emails
      phoneNumbers
    }
    location {
      addressFormatted
      location
      street
      city
      state
      zip
      country
    }
    education {
      school {
        name
        websiteUrl
        linkedinUrl
        logoUrl
        entityUrn
      }
      degree
      field
      grade
      startDate
      endDate
    }
    experience {
      location
      isCurrentPosition
      endDate
      startDate
      description
      title
      department
      contact {
        emails
        phoneNumbers
      }
      company {
        name
        funding {
          fundingTotal
        }
        foundingDate {
          date
        }
        socials {
          linkedin {
            url
          }
        }
      }
    }
    numNotableFollowers
    notableFollowers(first: 2) {
      followerName
      followerUrn
      firmName
      firmUrn
      followedName
      followedUrn
      followObservedAt
    }
    awardsBeta
    recommendationsBeta
    currentCompanyUrns
    entityUrn
    socials {
       facebook {
        url
        followerCount
       }
       twitter {
        followerCount
        url
       }
       linkedin {
        followerCount
        url
       }
       instagram {
        followerCount
        url
       }
       crunchbase {
        url
        followerCount
       }
       pitchbook {
        followerCount
        url
       }
       angellist {
        followerCount
        url
       }
       indeed {
        followerCount
        url
       }
       youtube {
        followerCount
        url
       }
       monster {
        followerCount
        url
       }
       stackoverflow {
        url
        followerCount
       }
    }
    recentJobUpdateStatus {
      date
      helperText
      type
    }
    linkedinProfileVisibilityType
    lastRefreshedAt
    lastCheckedAt
    languages {
      name
    }
   }
}
```

**GraphQL variables**

```json
{"getPersonByIdsIds": [1,2]}
```

### Batch get persons by ID

Pass in a list of person IDs or URNs, and get back a full picture of those persons.

**Note:** If a company ID is -1, that means we don't yet have a canonical company record for that company. The API will not return data for these companies.

**POST** `https://api.harmonic.ai/persons/batchGet`

| Name | Type |
| --- | --- |
| `ids` | array[integer] |
| `urns` | array[string] |

##### Example request

```json
{
  "ids": [315637, 12345],
  "urns": ["urn:harmonic:person:315637"]
}
```

**Limitations:** Endpoint has a limit of 500 people.

**REST**

`POST https://api.harmonic.ai/persons/batchGet`

```json
[
{
    "full_name": "Richard Hendricks",
    "first_name": "Richard",
    "last_name": "Hendricks",
    "profile_picture_url": "string",
    "contact": {...},
    "location": {...},
    "education": [...],
    "socials": {...},
    "experience": [...],
    "highlights": [...],
    "num_notable_followers": 42,
    "notable_followers": [...],
    "linkedin_headline": "General Manager Hotel Concorde Old Bucharest",
    "entity_urn": "urn:harmonic:person:1",
    "awards__beta": [...],
    "recommendations__beta": [...],
    "current_company_urns": [...],
    "linkedin_profile_visibility_type": "string",
    "last_refreshed_at": "string",
    "last_checked_at": "string",
    "languages": [...],
}]
```

## Deal data

Deal data endpoints return information about investors and their investments. These endpoints are available only through the GraphQL API, and are part of a paid add-on — contact support@harmonic.ai to learn more.

### Get investor by URN

Pass in an investor URN, and get back a full picture of that investor.

The "partners" field supports cursor pagination ("first" and "after" parameters), while the "investments" and "coInvestors" fields support offset pagination ("first" and "offset" parameters).

**Note:** If expanding the "details" field on an investor, conflicting fields between Company and People will need to be aliased. This is shown in the expanded example ("companyEntityUrn: entityUrn").

**Note:** This is supported in the GraphQL API only.

**GraphQL query**

```graphql
query Query($urn: String!, $coInvestorsFirst: Int!, $coInvestorsOffset: Int, $partnersFirst: Int!, $partnersAfter: String, $partnersUserConnectionStatus: UserConnectionStatus, $investmentsFirst: Int!, $investmentsOffset: Int) {
  getInvestorByUrn(urn: $urn) {
    aumAmountUsd
  checkSizeMaxUsd
  checkSizeMinUsd
  coInvestors(first: $coInvestorsFirst, offset: $coInvestorsOffset) {
    nodes {
      coInvestor {
        entityUrn
        type # Deprecated: Use investorType instead. Will be removed after April 1, 2025.
        investorType {
          primaryType
          secondaryTypes
        }
        aumAmountUsd
        checkSizeMaxUsd
        checkSizeMinUsd
        details {
          ... on Company {
            companyEntityUrn: entityUrn
            name
          }
          ... on Person {
            entityUrn
            fullName
          }
        }
      }
      coInvestedCompanies
    }
    hasNext
    totalCount
  }
  details {
    ... on Company {
      companyEntityUrn: entityUrn
      name
      socials {
        linkedin {
          url
        }
        pitchbook {
          url
        }
      }
      investorUrn
    }
    ... on Person {
      entityUrn
      investorUrn
      linkedinHeadline
      fullName
      socials {
        linkedin {
          url
        }
      }
    }
  }
  partners(first: $partnersFirst, after: $partnersAfter, userConnectionStatus: $partnersUserConnectionStatus) {
    nodes {
      entityUrn
      fullName
    }
    pageInfo {
      current
      hasNext
      next
    }
    totalCount
  }
  entityUrn
  type # Deprecated: Use investorType instead. Will be removed after April 1, 2025.
  investorType {
    primaryType
    secondaryTypes
  }
  exitCount
  followOnRate
  investmentCount
  investmentActivity {
    ago180d {
      categoryValue
      companiesCount
      percentageInvested
    }
    ago365d {
      categoryValue
      companiesCount
      percentageInvested
    }
    ago90d {
      categoryValue
      companiesCount
      percentageInvested
    }
    category
  }
  topGeographies {
    categoryValue
    companiesCount
    percentageInvested
  }
  topSectors {
    categoryValue
    companiesCount
    percentageInvested
  }
  topStages {
    categoryValue
    companiesCount
    percentageInvested
  }
  mostRecentInvestmentDate
  investments(first: $investmentsFirst, offset: $investmentsOffset) {
    hasNext
    totalCount
    nodes {
      entityUrn
      announcementDate
      companyUrn
      company {
        entityUrn
        name
      }
      fundingAmount
      fundingCurrency
      fundingRoundType
      postMoneyValuation
      sourceUrl
    }
  }
  numUnicorns
  unicorns {
    entityUrn
    name
  }
  entryStageFocus
  countryFocus
  sectorFocus
  subsectorFocus
  headcount
  usersInNetwork {
    userUrn
    user {
      email
    }
  }
  correspondenceSummary {
    lastEmailAt
    lastEmailContactPersonUrn
    lastEmailContactPersonEmail
    lastMeetingAt
    lastMeetingContactPersonUrn
    lastMeetingContactPersonEmail
  }
  location {
    addressFormatted
    location
    street
    city
    state
    zip
    country
    metroAreas
  }
  }
}
```

**GraphQL variables**

```json
{
  "urn": "urn:harmonic:investor:19",
  "coInvestorsFirst": 2,
  "partnersFirst": 2,
  "investmentsFirst": 2,
  "investmentsOffset": 0
}
```

### Get investors by URNs

Pass in a list of investor URNs, and get back a full picture of those investors.

The "partners" field supports cursor pagination ("first" and "after" parameters), while the "investments" and "coInvestors" fields support offset pagination ("first" and "offset" parameters).

**Note:** If expanding the "details" field on an investor, conflicting fields between Company and People will need to be aliased. This is shown in the expanded example ("companyEntityUrn: entityUrn").

**Note:** This is supported in the GraphQL API only.

**GraphQL query**

```graphql
query Query($urns: [String!]!, $coInvestorsFirst: Int!, $coInvestorsOffset: Int, $partnersFirst: Int!, $partnersAfter: String, $partnersUserConnectionStatus: UserConnectionStatus, $investmentsFirst: Int!, $investmentsOffset: Int) {
  getInvestorsByUrns(urns: $urns) {
    aumAmountUsd
  checkSizeMaxUsd
  checkSizeMinUsd
  coInvestors(first: $coInvestorsFirst, offset: $coInvestorsOffset) {
    nodes {
      coInvestor {
        entityUrn
        type # Deprecated: Use investorType instead. Will be removed after April 1, 2025.
        investorType {
          primaryType
          secondaryTypes
        }
        aumAmountUsd
        checkSizeMaxUsd
        checkSizeMinUsd
        details {
          ... on Company {
            companyEntityUrn: entityUrn
            name
          }
          ... on Person {
            entityUrn
            fullName
          }
        }
      }
      coInvestedCompanies
    }
    hasNext
    totalCount
  }
  details {
    ... on Company {
      companyEntityUrn: entityUrn
      name
      socials {
        linkedin {
          url
        }
        pitchbook {
          url
        }
      }
      investorUrn
    }
    ... on Person {
      entityUrn
      investorUrn
      linkedinHeadline
      fullName
      socials {
        linkedin {
          url
        }
      }
    }
  }
  partners(first: $partnersFirst, after: $partnersAfter, userConnectionStatus: $partnersUserConnectionStatus) {
    nodes {
      entityUrn
      fullName
    }
    pageInfo {
      current
      hasNext
      next
    }
    totalCount
  }
  entityUrn
  type # Deprecated: Use investorType instead. Will be removed after April 1, 2025.
  investorType {
    primaryType
    secondaryTypes
  }
  exitCount
  followOnRate
  investmentCount
  investmentActivity {
    ago180d {
      categoryValue
      companiesCount
      percentageInvested
    }
    ago365d {
      categoryValue
      companiesCount
      percentageInvested
    }
    ago90d {
      categoryValue
      companiesCount
      percentageInvested
    }
    category
  }
  topGeographies {
    categoryValue
    companiesCount
    percentageInvested
  }
  topSectors {
    categoryValue
    companiesCount
    percentageInvested
  }
  topStages {
    categoryValue
    companiesCount
    percentageInvested
  }
  mostRecentInvestmentDate
  investments(first: $investmentsFirst, offset: $investmentsOffset) {
    hasNext
    totalCount
    nodes {
      entityUrn
      announcementDate
      companyUrn
      company {
        entityUrn
        name
      }
      fundingAmount
      fundingCurrency
      fundingRoundType
      postMoneyValuation
      sourceUrl
    }
  }
  numUnicorns
  unicorns {
    entityUrn
    name
  }
  entryStageFocus
  countryFocus
  sectorFocus
  subsectorFocus
  headcount
  usersInNetwork {
    userUrn
    user {
      email
    }
  }
  correspondenceSummary {
    lastEmailAt
    lastEmailContactPersonUrn
    lastEmailContactPersonEmail
    lastMeetingAt
    lastMeetingContactPersonUrn
    lastMeetingContactPersonEmail
  }
  location {
    addressFormatted
    location
    street
    city
    state
    zip
    country
    metroAreas
  }
  }
}
```

**GraphQL variables**

```json
{
  "urns": ["urn:harmonic:investor:213580", "urn:harmonic:investor:19", "urn:harmonic:investor:245357"],
  "coInvestorsFirst": 2,
  "partnersFirst": 2,
  "investmentsFirst": 2,
  "investmentsOffset": 0
}
```

### Get investor by canonical

Pass in an investor canonical URL, and get back a full picture of that investor.

The "partners" field supports cursor pagination ("first" and "after" parameters), while the "investments" and "coInvestors" fields support offset pagination ("first" and "offset" parameters).

**Note:** If expanding the "details" field on an investor, conflicting fields between Company and People will need to be aliased. This is shown in the expanded example ("companyEntityUrn: entityUrn").

**Note:** This is supported in the GraphQL API only.

| Name | Type |
| --- | --- |
| `url` * | string |

**GraphQL query**

```graphql
query Query($url: String!, $coInvestorsFirst: Int!, $coInvestorsOffset: Int, $partnersFirst: Int!, $partnersAfter: String, $partnersUserConnectionStatus: UserConnectionStatus, $investmentsFirst: Int!, $investmentsOffset: Int) {
  getInvestorByCanonical(url: $url) {
    aumAmountUsd
  checkSizeMaxUsd
  checkSizeMinUsd
  coInvestors(first: $coInvestorsFirst, offset: $coInvestorsOffset) {
    nodes {
      coInvestor {
        entityUrn
        type # Deprecated: Use investorType instead. Will be removed after April 1, 2025.
        investorType {
          primaryType
          secondaryTypes
        }
        aumAmountUsd
        checkSizeMaxUsd
        checkSizeMinUsd
        details {
          ... on Company {
            companyEntityUrn: entityUrn
            name
          }
          ... on Person {
            entityUrn
            fullName
          }
        }
      }
      coInvestedCompanies
    }
    hasNext
    totalCount
  }
  details {
    ... on Company {
      companyEntityUrn: entityUrn
      name
      socials {
        linkedin {
          url
        }
        pitchbook {
          url
        }
      }
      investorUrn
    }
    ... on Person {
      entityUrn
      investorUrn
      linkedinHeadline
      fullName
      socials {
        linkedin {
          url
        }
      }
    }
  }
  partners(first: $partnersFirst, after: $partnersAfter, userConnectionStatus: $partnersUserConnectionStatus) {
    nodes {
      entityUrn
      fullName
    }
    pageInfo {
      current
      hasNext
      next
    }
    totalCount
  }
  entityUrn
  type # Deprecated: Use investorType instead. Will be removed after April 1, 2025.
  investorType {
    primaryType
    secondaryTypes
  }
  exitCount
  followOnRate
  investmentCount
  investmentActivity {
    ago180d {
      categoryValue
      companiesCount
      percentageInvested
    }
    ago365d {
      categoryValue
      companiesCount
      percentageInvested
    }
    ago90d {
      categoryValue
      companiesCount
      percentageInvested
    }
    category
  }
  topGeographies {
    categoryValue
    companiesCount
    percentageInvested
  }
  topSectors {
    categoryValue
    companiesCount
    percentageInvested
  }
  topStages {
    categoryValue
    companiesCount
    percentageInvested
  }
  mostRecentInvestmentDate
  investments(first: $investmentsFirst, offset: $investmentsOffset) {
    hasNext
    totalCount
    nodes {
      entityUrn
      announcementDate
      companyUrn
      company {
        entityUrn
        name
      }
      fundingAmount
      fundingCurrency
      fundingRoundType
      postMoneyValuation
      sourceUrl
    }
  }
  numUnicorns
  unicorns {
    entityUrn
    name
  }
  entryStageFocus
  countryFocus
  sectorFocus
  subsectorFocus
  headcount
  usersInNetwork {
    userUrn
    user {
      email
    }
  }
  correspondenceSummary {
    lastEmailAt
    lastEmailContactPersonUrn
    lastEmailContactPersonEmail
    lastMeetingAt
    lastMeetingContactPersonUrn
    lastMeetingContactPersonEmail
  }
  location {
    addressFormatted
    location
    street
    city
    state
    zip
    country
    metroAreas
  }
  }
}
```

**GraphQL variables**

```json
{
  "url": "a16z.com",
  "coInvestorsFirst": 2,
  "partnersFirst": 2,
  "investmentsFirst": 2,
  "investmentsOffset": 0
}
```

## Saved searches

Use saved searches to find companies, people, and investors.

### Get saved searches

Get all company and people saved searches accessible to your account.

**GET** `https://api.harmonic.ai/savedSearches`

**GraphQL query**

```graphql
query {
  getSavedSearchesForTeam {
    entityUrn
    isPrivate
    name
    type
  }
}
```

### Get company saved search results with metadata

Get all the companies matching a saved search. Only saved searches that are shared with your team can be accessed via API. Recommended size of 100 companies per request.

**GET** `https://api.harmonic.ai/savedSearches:results/{id_or_urn}`

| Name | Type | Description |
| --- | --- | --- |
| `id_or_urn` * | string | ID or URN of the saved search, passed in the URL path. |
| `size` | integer | Number of results to return per page. Recommended: 100. |
| `cursor` | string | Cursor indicating where to continue from — pass the next token from the previous response. |

This endpoint supports cursor pagination (with `cursor` and `size` query params). See [Pagination](/docs/api-reference/introduction#pagination) for details.

This GraphQL query supports cursor pagination (with `cursor` and `size` variables). See [Pagination](/docs/api-reference/introduction#pagination) for details.

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/savedSearches:results/{id_or_urn}`

```json
{
  "count": 1,
  "results": [
    "urn:harmonic:company:123456"
  ]
}
```

**GraphQL query**

```graphql
query GetCompaniesWithMetadataInSavedSearchesByIdOrUrn($idOrUrn: String!, $cursor: String, $size: Int) {
  getCompaniesWithMetadataInSavedSearchesByIdOrUrn(idOrUrn: $idOrUrn, cursor: $cursor, size: $size) {
    pageInfo {
      current
      hasNext
      next
    }
    count
    companies {
      headcount
      name
      id
    }
  }
}
```

### Get people saved search results with metadata

Get all the people matching a saved search. Only saved searches that are shared with your team can be accessed via API. Recommended size of 100 people per request.

**GET** `https://api.harmonic.ai/savedSearches:results/{id_or_urn}`

| Name | Type | Description |
| --- | --- | --- |
| `id_or_urn` * | string | ID or URN of the saved search, passed in the URL path. |
| `size` | integer | Number of results to return per page. Recommended: 100. |
| `cursor` | string | Cursor indicating where to continue from — pass the next token from the previous response. |

This endpoint supports cursor pagination (with `cursor` and `size` query params). See [Pagination](/docs/api-reference/introduction#pagination) for details.

This GraphQL query supports cursor pagination (with `cursor` and `size` variables). See [Pagination](/docs/api-reference/introduction#pagination) for details.

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/savedSearches:results/{id_or_urn}`

```json
{
  "count": 1,
  "page_info": { "next": "Wzc1MjAwXQ==", "current": null, "has_next": true },
  "results": [
    "urn:harmonic:person:123456"
  ]
}
```

**GraphQL query**

```graphql
query GetPeopleWithMetadataInSavedSearchesByIdOrUrn($idOrUrn: String!, $cursor: String, $size: Int) {
  getPeopleWithMetadataInSavedSearchesByIdOrUrn(idOrUrn: $idOrUrn, cursor: $cursor, size: $size) {
    pageInfo {
      current
      hasNext
      next
    }
    count
    people {
      id
      fullName
      profilePictureUrl
    }
  }
}
```

### Get investor saved search results with metadata

Get all the investors matching a saved search. Only saved searches that are shared with your team can be accessed via API. Recommended size of 100 investors per request.

**GET** `https://api.harmonic.ai/savedSearches:results/{id_or_urn}`

| Name | Type | Description |
| --- | --- | --- |
| `id_or_urn` * | string | ID or URN of the saved search, passed in the URL path. |
| `size` | integer | Number of results to return per page. Recommended: 100. |
| `cursor` | string | Cursor indicating where to continue from — pass the next token from the previous response. |

This endpoint supports cursor pagination (with `cursor` and `size` query params). See [Pagination](/docs/api-reference/introduction#pagination) for details.

This GraphQL query supports cursor pagination (with `cursor` and `size` variables). See [Pagination](/docs/api-reference/introduction#pagination) for details.

### Get company saved search net new results

Get new results matching a company saved search you've subscribed to. This endpoint returns companies that have newly become matches for your subscribed saved search's criteria. For example, if your search looks for companies with &gt;100 headcount, this will return companies that have grown to exceed 100 headcount within the specified timeframe.

**Note:** Relevance score filters are not supported via API and will be ignored while fetching net new results.

**GET** `https://api.harmonic.ai/savedSearches/{id_or_urn}/net_new_results`

This endpoint supports the following optional query parameters:

| Name | Type | Description |
| --- | --- | --- |
| `id_or_urn` * | string | ID or URN of the saved search, passed in the URL path. |
| `new_results_since` | DateTime | DateTime in UTC (For example: 2024-09-21T00:00:00Z, 2024-09-21) since when companies have become matches. If provided, this endpoint will return companies that have become matches since the specified date. Otherwise, it will return companies that have become matches since the saved search was subscribed to (or September 21, 2024, whichever is later). |

This query supports cursor pagination routes (with cursor, and size params). See [Pagination](/docs/api-reference/introduction#pagination) for details.

At present, we can pull net new results for only subscribed saved searches. Please visit the Harmonic console to subscribe to a saved search.

**GraphQL query**

```graphql
query GetNetNewCompaniesInSavedSearchByIdOrUrn($idOrUrn: String!, $size: Int, $cursor: String, $newResultsSince: DateTimeUTC) {
  getNetNewCompaniesInSavedSearchByIdOrUrn(idOrUrn: $idOrUrn, size: $size, cursor: $cursor, newResultsSince: $newResultsSince) {
    pageInfo {
      current
      hasNext
      next
    }
    companies {
      id
      name
      headcount
    }
  }
}
```

### Get people saved search net new results

Get new results matching a people saved search you've subscribed to. This endpoint returns people that have newly become matches for your subscribed saved search's criteria. For example, if your search looks for people with &gt;10 years of experience, this will return people updated to have more than 10 years of experience within the specified timeframe.

**GET** `https://api.harmonic.ai/savedSearches/{id_or_urn}/net_new_results`

This endpoint supports the following optional query parameters:

| Name | Type | Description |
| --- | --- | --- |
| `id_or_urn` * | string | ID or URN of the saved search, passed in the URL path. |
| `new_results_since` | DateTime | DateTime in UTC (For example: 2024-09-21T00:00:00Z, 2024-09-21) since when people have become matches. If provided, this endpoint will return people that have become matches since the specified date. Otherwise, it will return people that have become matches since the saved search was subscribed to (or September 21, 2024, whichever is later). |

This query supports cursor pagination routes (with cursor, and size params). See [Pagination](/docs/api-reference/introduction#pagination) for details.

At present, we can pull net new results for only subscribed saved searches. Please visit the Harmonic console to subscribe to a saved search.

**GraphQL query**

```graphql
query GetNetNewPeopleInSavedSearchByIdOrUrn($idOrUrn: String!, $size: Int, $cursor: String, $newResultsSince: DateTimeUTC) {
  getNetNewPeopleInSavedSearchByIdOrUrn(idOrUrn: $idOrUrn, size: $size, cursor: $cursor, newResultsSince: $newResultsSince) {
    pageInfo {
      current
      hasNext
      next
    }
    people {
      entityUrn
      fullName
    }
  }
}
```

### Save a keyword search

Pass in a string of keywords and name of the search in the request body and get urn of the saved search.

**POST** `https://api.harmonic.ai/savedSearches`

| Name | Type | Description |
| --- | --- | --- |
| `keywords` * | string | Space-delimited string of keywords to search for (uses contains_all_of semantics). |
| `name` * | string | Display name for the saved search. |

##### Example request

```json
{
  "keywords": "software healthcare",
  "name": "Software and healthcare companies"
}
```

## Get similar companies

Pass in a company ID, and get back a list of similar companies. You can use either the int ID, or the full URN.

ID example:

```
GET https://api.harmonic.ai/search/similar_companies/123456
```

URN example:

```
GET https://api.harmonic.ai/search/similar_companies/urn:harmonic:company:123456
```

**GET** `https://api.harmonic.ai/search/similar_companies/{id_or_urn}`

| Name | Type |
| --- | --- |
| `size` | integer |

**Limitations:** Size has a limit of 1000 companies.

**REST**

`GET https://api.harmonic.ai/search/similar_companies/{id_or_urn}`

```json
{
  "count": 3,
  "results": [
    "urn:harmonic:company:123456",
    "urn:harmonic:company:123457",
    "urn:harmonic:company:123458"
  ]
}
```

## Get search typeahead results

Pass in a string of keywords and get back a list of typeahead search results for companies, people, or investors.

**Note:** Results are returned rank ordered by strength of match — if you only need the best match, take the first result.

**GET** `https://api.harmonic.ai/search/typeahead`

| Name | Type | Description |
| --- | --- | --- |
| `query` * | string | The query to search for. This can be a name, a partial name, or a domain/URL. |
| `search_type` | string | The type of search to perform. Supports: COMPANY, PERSON, INVESTOR |

#### Example request

```
GET https://api.harmonic.ai/search/typeahead?query=langchain&search_type=COMPANY
```

**Limitations:** Only returns results for entities that have been seen by Harmonic.

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/search/typeahead`

```json
{
  "count": 1,
  "results": [
    {
      "entity_urn": "urn:harmonic:company:123456",
      "type": "string",
      "source": "string",
      "text": "string",
      "alt_text": null,
      "index_field": null,
      "index_id": null,
      "ranking_score": 6.337293455870422,
      "index_method": 1,
      "subtype": null
    }
  ]
}
```

**GraphQL query**

```graphql
query GetCompaniesWithTypeahead($query: String!) {
  getCompaniesWithTypeahead(query: $query) {
    companyType
    contact {
      emails
      phoneNumbers
    }
    description
    entityUrn
    foundingDate {
      date
      granularity
    }
    funding {
      fundingTotal
      numFundingRounds
      lastFundingAt
      lastFundingType
      lastFundingTotal
      investors {
        ... on Company {
          name
        }
        ... on Person {
          fullName
        }
      }
      fundingRounds {
        entityUrn
        announcementDate
        fundingRoundType
        fundingAmount
        fundingCurrency
        sourceUrl
        postMoneyValuation
        investors {
          investorName
          isLead
          entityUrn
        }
      }
    }
    websiteDomainAliases
    nameAliases
    fundingAttributeNullStatus
    id
    logoUrl
    legalName
    name
    ownershipStatus
    headcount
    stage
    highlights {
      text
      category
    }
    numNotableFollowers
    notableFollowers(first: 2) {
      followerName
      followerUrn
      firmName
      firmUrn
      followedName
      followedUrn
      followObservedAt
    }
    initializedDate
    location {
      country
      zip
      state
      city
      street
      location
      addressFormatted
    }
    employees {
      entityUrn
      fullName
      firstName
      lastName
      profilePictureUrl
      contact {
        phoneNumbers
        emails
      }
      location {
        country
        zip
        state
        city
        street
        location
        addressFormatted
      }
      education {
        endDate
        startDate
        grade
        field
        degree
        school {
          name
          websiteUrl
          linkedinUrl
          logoUrl
          entityUrn
        }
      }
      experience {
        location
        isCurrentPosition
        endDate
        startDate
        description
        title
        department
        contact {
          emails
          phoneNumbers
        }
      }
      awardsBeta
      recommendationsBeta
    }
    snapshots {
      name
    }
    socials {
       facebook {
        url
        followerCount
       }
       twitter {
        followerCount
        url
       }
       linkedin {
        followerCount
        url
       }
       instagram {
        followerCount
        url
       }
       crunchbase {
        url
        followerCount
       }
       pitchbook {
        followerCount
        url
       }
       angellist {
        followerCount
        url
       }
       indeed {
        followerCount
        url
       }
       youtube {
        followerCount
        url
       }
       monster {
        followerCount
        url
       }
       stackoverflow {
        url
        followerCount
       }
    }
    website {
      isBroken
      domain
      url
    }
    tags {
      type
      displayValue
      entityUrn
      dateAdded
    }
    userConnections {
      user {
        email
        name
      }
    }
    tractionMetrics {
      headcount {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      webTraffic {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountAdvisor {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountCustomerSuccess {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountMarketing {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountOther {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountProduct {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountSales {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountSupport {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountData {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountDesign {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountEngineering {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountFinance {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountOperations {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountLegal {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      headcountPeople {
        ago14d {
          value
          change
          percentChange
        }
        ago30d {
          value
        }
        ago90d {
          value
        }
        ago180d {
          value
        }
        ago365d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      facebookFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      linkedinFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      instagramFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
      twitterFollowerCount {
        ago14d {
          value
        }
        metrics {
          timestamp
          metricValue
        }
        latestMetricValue
      }
    }
    relatedCompanies {
      priorStealthAssociation {
        emergenceDate
        previouslyKnownAs
      }
    }
  }
}
```

**GraphQL variables**

```json
{"query": "langchain"}
```

## Search companies by natural language

Pass in a natural language query and get back a list of relevant companies from Harmonic's database.

**Note:** Handles basic searches and returns companies only. For complex queries across companies, people, and investors — plus research reports, Q&A, and more — [Ask Scout](/docs/api-reference/scout/tasks).

---

**Usage:** Reference companies by name ("companies like Harmonic"), domain ("similar to harmonic.ai"), or URL. Include criteria like company stage, funding, sector, or growth indicators for better results. [More info](https://support.harmonic.ai/en/articles/10504491-natural-language-search-api).

**GET** `https://api.harmonic.ai/search/search_agent`

| Name | Type | Description |
| --- | --- | --- |
| `query` | string | Natural language search query describing the companies you want to find. Can reference companies by name, domain, or URL. |
| `similarity_threshold` | float | Minimum similarity score for results (0.0 to 1.0). Default: dynamically determined. Note: Setting this parameter disables automatic threshold optimization. |
| `size` | integer | Maximum number of results to return. Default: 25. Range: 1-1000. |
| `cursor` | string | Cursor for pagination. Use the next token from page_info in the response to retrieve additional results. |

**Example Queries:**

- "Series B software companies with &gt;$10M in funding focused on financial services"
- "climate tech startups with employees from GE Renewable Energy"
- "robotics companies building automation like covariant.ai"

**Limitations**

- Maximum result size: 1000 companies.

**REST**

`GET https://api.harmonic.ai/search/search_agent`

```json
{
  "count": 885,
  "page_info": {
    "next": "page_2_token",
    "current": null,
    "has_next": true
  },
  "results": [
    {
      "urn": "urn:harmonic:company:123456",
      "cursor": "result_1_position"
    },
    {
      "urn": "urn:harmonic:company:789012",
      "cursor": "result_2_position"
    }
  ],
  "query_interpretation": {
    "semantic": "payment processing startups offering innovative solutions for secure transactions, fraud prevention, and seamless integration with e-commerce platforms",
    "faceted": [
      {
        "field_name": "funding_total",
        "operator": "greaterThanOrEquals",
        "filter_value": 5000000,
        "parsed_text": "at least 5m in funding"
      }
    ],
    "preserved_semantic_input": "payment processing startups",
    "companies": null,
    "unprocessable_query_part": "",
    "parser_version": "v1"
  }
}
```

## Ask Scout

Scout is Harmonic's AI research agent, available programmatically through the same engine that powers Scout in the product. Send a natural-language prompt and get back a markdown answer — or structured JSON when you supply a schema.

### Overview

> Every account starts with **$250 in free Scout API credits** so you can test the API before committing spend. See the [Scout via API guide](https://support.harmonic.ai/en/articles/15058239-scout-via-api-alpha) to get started.

Scout API usage is billed on token consumption &mdash; see [Scout consumption pricing](https://support.harmonic.ai/en/articles/15063167-scout-consumption-pricing) for how usage is metered and priced. When your team's budget or contracted cap is exhausted, task creation returns `429` with an explanatory error body; contact your account manager to raise the cap. **Scout task creation is rate-limited to 10 requests per minute and 100 per hour &mdash; the general [10 requests/second](/docs/api-reference/introduction#rate-limit) account limit does _not_ apply to task creation.** See [Rate limits and quotas](#rate-limits-and-quotas) below.

#### Tasks

A Scout request runs as a **task**. The same prompt works for every endpoint &mdash; what differs is
_how you wait for the answer_. Pick the endpoint that matches how long the research will take and how you
want to consume the result:

- **Run and wait** &mdash; [`POST /scout/tasks/wait`](/docs/api-reference/scout/run-and-wait). One call
  that **blocks until Scout finishes** and returns the completed answer. Use it for quick lookups in
  scripts, notebooks, or cron jobs where holding the connection open for the duration is fine.
  _Example prompt:_ `"What is Peec AI's most recent funding round and who led it?"`
- **Create a task** &mdash; [`POST /scout/tasks`](/docs/api-reference/scout/create-task). Returns a
  `task_id` **immediately**, then you poll [`GET /scout/tasks/{task_id}`](/docs/api-reference/scout/get-task)
  until the status is terminal. Use it for **longer or batched research** where you don't want to hold a
  connection open &mdash; kick off the task, do other work, and collect the result later.
  _Example prompt:_ `"Build me a profile of the 20 most active seed-stage AI investors in Europe, with their recent deals."`
- **Stream a task** &mdash; [`POST /scout/tasks/stream`](/docs/api-reference/scout/stream-task). Emits
  server-sent events as the agent thinks and answers. Best for **interactive, real-time UIs** where you
  want to show progress token by token.
  _Example prompt:_ `"Prep me for an intro call with Peec AI — cover the company, its founders, and the major players in their space."`

The endpoints differ only in delivery, not capability: **Run and wait** and **Create a task** accept the
same body (including an optional `json_schema` for structured output); **Stream a task** accepts the same
prompt but does not support `json_schema`.

All Scout endpoints are REST only and live under `https://api.harmonic.ai/scout`.

#### Authentication

Scout uses the same API key as the rest of the Harmonic API &mdash; pass it in the `apikey` header. See [Authentication](/docs/api-reference/introduction#authentication) for details.

#### Task lifecycle

Every task endpoint returns a task object with a `status`. Poll or stream until the status is **terminal**.

| Status        | Terminal | Meaning                                                   |
| ------------- | -------- | --------------------------------------------------------- |
| `pending`     | No       | Task accepted, not yet started.                           |
| `running`     | No       | The agent is working on the task.                         |
| `success`     | Yes      | Finished successfully &mdash; `content` holds the result. |
| `error`       | Yes      | The task failed.                                          |
| `timeout`     | Yes      | The task exceeded its time budget.                        |
| `interrupted` | Yes      | The task was cancelled before completing.                 |

`content` is populated only when `status` is `success`; it is `null` for every other status.

#### Structured output

By default `content` is markdown text. Supply a [JSON Schema](https://json-schema.org/) as `json_schema` and Scout returns `content` as an object matching that schema instead &mdash; useful for writing results straight into a database or spreadsheet. `json_schema` is supported on `POST /scout/tasks/wait` and `POST /scout/tasks`, but not on the streaming endpoints.

```bash
curl -X POST "https://api.harmonic.ai/scout/tasks/wait" \
  -H "apikey: $HARMONIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Find early engineers at Profound",
    "json_schema": {
      "type": "object",
      "properties": {
        "people": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "linkedin_url": { "type": "string" },
              "one_liner": { "type": "string" }
            },
            "required": ["name", "linkedin_url", "one_liner"]
          }
        }
      },
      "required": ["people"]
    }
  }'
```

#### End-to-end example

Create a task and poll until it finishes:

```bash
# 1. Start the task
TASK=$(curl -s -X POST "https://api.harmonic.ai/scout/tasks" \
  -H "apikey: $HARMONIC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": "Prep me for an intro call with Peec AI. Cover the company, its founders, and the major players in their space."}')
TASK_ID=$(echo "$TASK" | jq -r .task_id)
echo "Started task $TASK_ID"

# 2. Poll until the status is terminal, then print the result
while true; do
  RESULT=$(curl -s "https://api.harmonic.ai/scout/tasks/$TASK_ID" \
    -H "apikey: $HARMONIC_API_KEY")
  STATUS=$(echo "$RESULT" | tr -d '\000-\037' | jq -r .status)
  echo "  status: $STATUS"
  case "$STATUS" in
    success|error|timeout|interrupted) break ;;
  esac
  sleep 5
done
echo "$RESULT" | jq -r .content
```

#### Rate limits and quotas

Task creation (across `wait`, `tasks`, and `stream`) is limited to **10 requests per minute and 100 per hour**. Exceeding either returns `429 Too many requests`.

Beyond rate limits, usage is billed on token consumption and capped by your team's budget &mdash; see [Scout consumption pricing](https://support.harmonic.ai/en/articles/15063167-scout-consumption-pricing). When the cap is exhausted, task creation returns `429` with an explanatory error body; contact your account manager to raise it. The general [10 requests/second](/docs/api-reference/introduction#rate-limit) account limit applies to other Harmonic API endpoints, but Scout task creation uses the 10/min, 100/hour limit above.

### Run a task and wait

Run a Scout task synchronously. The request blocks until the agent finishes, then returns the completed task with its `content`.

**When to use this:** quick lookups in scripts, notebooks, or cron jobs where a single blocking call is fine. For longer or batched research &mdash; or anything where you don't want to hold a connection open &mdash; [create a task](/docs/api-reference/scout/create-task) and poll instead.

_Example prompt:_ `"What is Peec AI's most recent funding round and who led it?"`

**POST** `https://api.harmonic.ai/scout/tasks/wait`

| Name | Type | Description |
| --- | --- | --- |
| `input` * | string | The natural-language prompt for Scout. |
| `json_schema` | object | Optional JSON Schema. When provided, the result content is an object matching the schema instead of markdown text. |
| `request_origin` | string | Optional client-surface label, either "API" or "MCP". Defaults to "API"; direct callers can omit it. |

##### Example request

```json
{
  "input": "What is Peec AI's most recent funding round and who led it?"
}
```

##### Example request with a JSON schema

Supply `json_schema` to get structured `content` back instead of markdown:

```json
{
  "input": "Find early engineers at Profound",
  "json_schema": {
    "type": "object",
    "properties": {
      "people": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "linkedin_url": { "type": "string" },
            "one_liner": { "type": "string" }
          },
          "required": ["name", "linkedin_url", "one_liner"]
        }
      }
    },
    "required": ["people"]
  }
}
```

Returns the completed task with `status` `success` and the answer in `content` (markdown, or an object when `json_schema` was supplied). See the [task lifecycle](/docs/api-reference/scout/overview#task-lifecycle) for the full list of statuses.

### Create a task

Start a Scout task asynchronously. Returns immediately with a `task_id` and a non-terminal status; poll [`GET /scout/tasks/{task_id}`](/docs/api-reference/scout/get-task) until the status is terminal to retrieve the result.

**When to use this:** longer or batched research where you don't want to hold a connection open &mdash; kick off the task, do other work, then collect the result. For quick lookups where a single blocking call is simpler, use [run and wait](/docs/api-reference/scout/run-and-wait) instead.

_Example prompt:_ `"Build me a profile of the 20 most active seed-stage AI investors in Europe, with their recent deals."`

**POST** `https://api.harmonic.ai/scout/tasks`

| Name | Type | Description |
| --- | --- | --- |
| `input` * | string | The natural-language prompt for Scout. |
| `json_schema` | object | Optional JSON Schema. When provided, the result content is an object matching the schema instead of markdown text. |
| `request_origin` | string | Optional client-surface label, either "API" or "MCP". Defaults to "API"; direct callers can omit it. |

##### Example request

```json
{
  "input": "Build me a profile of the 20 most active seed-stage AI investors in Europe, with their recent deals."
}
```

##### Example request with a JSON schema

Supply `json_schema` to get structured `content` back instead of markdown:

```json
{
  "input": "Find early engineers at Profound",
  "json_schema": {
    "type": "object",
    "properties": {
      "people": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "linkedin_url": { "type": "string" },
            "one_liner": { "type": "string" }
          },
          "required": ["name", "linkedin_url", "one_liner"]
        }
      }
    },
    "required": ["people"]
  }
}
```

Returns the new task. `status` is `pending` or `running` and `content` is `null` until the task completes.

### Get a task

Poll a task created with [`POST /scout/tasks`](/docs/api-reference/scout/create-task) using the `task_id` from that response. Call this on an interval (every few seconds is plenty) until `status` is terminal; the answer is in `content` once `status` is `success`.

**GET** `https://api.harmonic.ai/scout/tasks/{task_id}`

| Name | Type | Description |
| --- | --- | --- |
| `task_id` * | string | The opaque task identifier returned when the task was created. Pass it back unchanged. |

An unknown `task_id` returns `404 Not found`.

While the task is in progress, `content` is `null`. Once `status` is `success`, `content` holds the answer (markdown, or an object when `json_schema` was supplied on creation).

### Stream a task

Start a Scout task and stream its progress as [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events). The response is a `text/event-stream` of the agent's thinking steps and answer tokens as they are produced &mdash; ideal for interactive UIs. `json_schema` is not supported on this endpoint; supplying it returns `400`.

**POST** `https://api.harmonic.ai/scout/tasks/stream`

| Name | Type | Description |
| --- | --- | --- |
| `input` * | string | The natural-language prompt for Scout. |
| `request_origin` | string | Optional client-surface label, either "API" or "MCP". Defaults to "API"; direct callers can omit it. |

##### Example request

```json
{
  "input": "Prep me for an intro call with Peec AI — cover the company, its founders, and the major players in their space."
}
```

Streaming does **not** accept `json_schema`; including it returns `400`. The response is a
`text/event-stream`, not JSON &mdash; see the event types below.

#### Events

Each event is an SSE `data:` line with a JSON payload of `{ "type": ..., "content": ... }`.

| `type`    | `content`      | Description                                                                                                                                               |
| --------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `task_id` | The task's id  | Always emitted first. Save it to reconnect via [`GET /scout/tasks/{task_id}/stream`](/docs/api-reference/scout/reconnect-stream) if the connection drops. |
| `step`    | Status message | A human-readable update on what the agent is doing.                                                                                                       |
| `content` | Answer chunk   | A token of the markdown answer. Concatenate these in order to assemble the full response.                                                                 |
| `error`   | Error message  | A terminal failure occurred.                                                                                                                              |
| `done`    | `null`         | The stream is complete. No further events follow.                                                                                                         |

### Reconnect to a task stream

Reattach to the event stream of a task started with [`POST /scout/tasks/stream`](/docs/api-reference/scout/stream-task), using the `task_id` from that stream's first event. Use this to resume after a dropped connection. The stream picks up from the current point &mdash; events emitted before you reconnect are **not** replayed &mdash; and ends with a `done` event like the original stream.

**GET** `https://api.harmonic.ai/scout/tasks/{task_id}/stream`

| Name | Type | Description |
| --- | --- | --- |
| `task_id` * | string | The id emitted as the first task_id event of the initial stream. Pass it back unchanged. |

A `text/event-stream` of the same [event types](/docs/api-reference/scout/stream-task#events) as the original stream, resuming from wherever the task currently is.

## Getting started

### Overview

Workspace is where your team tracks the companies, people, and investors you care about — your sourcing pipelines, your portfolio, your research lists. The Workspace API lets you do all of that programmatically: pull a list into your own tools, push new companies in from another system, keep a CRM in sync, or automate the busywork of moving deals through stages.

The API is a single GraphQL endpoint. Every operation — reading a list, adding entries, defining a field, saving a view — is one `POST` to `api.harmonic.ai/graphql/v2`.

The endpoint supports GraphQL introspection, so interactive explorers, client codegen, and coding agents can load the full, typed schema directly.

Your whole account lives under one **workspace**, scoped to your team and resolved from your API key.

#### Usage limits

A few limits to design around:

| Limit                        | Value                             | Notes                                                                          |
| ---------------------------- | --------------------------------- | ------------------------------------------------------------------------------ |
| Query depth                  | 15 levels                         | Deeper queries are rejected before execution.                                  |
| Import size (`createImport`) | 1,000 rows per request            | Split larger imports across multiple requests. See **Import and Enrich Data**. |
| Filter-based bulk operations | 10,000 items per request          | Applies to bulk operations using filters. See **Manage a Sourcing Workflow**.  |
| Large reads                  | Cursor-based pagination           | Results are paginated rather than returned all at once. See **Pagination**.    |
| Workspace size               | 1,000,000 records per record type | Maximum number of records per record type in a workspace.                      |

### Authentication

Authenticate with your team's API key in the `apikey` header — the same key used elsewhere in the Harmonic API.

```bash
curl -X POST "https://api.harmonic.ai/graphql/v2" \
  -H "apikey: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ workspace { urn name } }"}'
```

An API key can read and write any list or saved search that is **shared with your entire team** — see [Permissions and shared access](#permissions-and-shared-access) below for what to do when a resource isn't reachable.

#### Your first request

This call confirms your key works and returns the basics of your account:

```bash
curl -X POST "https://api.harmonic.ai/graphql/v2" \
  -H "apikey: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ workspace { urn name } }"}'
```

The `workspace` query takes no arguments — it resolves from your API key, so it always returns _your_ team's account. Once that works, ask for the URNs you'll reuse throughout: your built-in record types.

```graphql
query StarterQuery {
  workspace {
    urn
    name
    companyRecordType {
      urn # use for company lists & records
      name
    }
    personRecordType {
      urn # use for people lists & records
      name
    }
  }
}
```

The built-in record types resolve to stable, fixed URNs: `urn:harmonic:record_type:company`, `urn:harmonic:record_type:person`, and `urn:harmonic:record_type:investor`.

#### Permissions and shared access

An API key can read and write any **list or saved search that is shared with your entire team**. Private resources are not reachable through the API.

If a request can't find a list, view, or search you expect, the resource is most likely private — share it with your team in the Harmonic console first, then retry with the same key.

#### Reading responses

Unlike REST, partial success is a core design feature of the GraphQL Specification. Any request that reaches execution returns HTTP `200` — even when parts of it fail — so always check the response body for errors, not just the status code. (Requests rejected before execution use conventional statuses: schema-validation failures return `422` with the same `errors` body shape; missing or invalid auth returns `401`/`403`.) A successful response carries your data under `data`; a failed one carries a non-empty `errors` array (and `data: null`).

A successful request — `{ workspace { urn name } }`:

```json
{
  "data": {
    "workspace": {
      "urn": "urn:harmonic:workspace:00000000-0000-0000-0000-000000000001",
      "name": "Harmonic.ai"
    }
  }
}
```

A failed request — here `record` was called without its required `recordTypeUrn`. Schema violations (an unknown field, a missing required argument, an invalid enum value) are rejected before execution:

```json
{
  "errors": [
    {
      "message": "Field \"record\" argument \"recordTypeUrn\" of type \"RecordTypeURN!\" is required, but it was not provided.",
      "locations": [{ "line": 1, "column": 3 }],
      "extensions": { "code": "GRAPHQL_VALIDATION_FAILED" }
    }
  ],
  "data": null
}
```

Each error gives you a human-readable `message`, the `locations` in your query, and an `extensions.code` you can branch on programmatically. Errors that happen during execution (rather than schema validation) come back in the same `errors` shape — sometimes alongside a partially-populated `data`, so always check both.

With a request working, move on to [Pagination](#pagination) for reading large result sets, or jump to a workflow like [Manage a Sourcing Workflow](/docs/api-reference/workspace/common-workflows#manage-a-sourcing-workflow).

### Pagination

Lists, records, entries, views, and other collections can be large, so the API never returns them all at once. Instead it returns one page at a time and hands you a cursor to fetch the next. This section shows how to read through a full result set efficiently.

Every collection — `entries`, `records`, `lists`, `users`, `namedViews`, and the rest — uses the same Relay-style `Connection` shape: `edges { node }`, a `pageInfo`, and a `totalCount`. The `node` is the underlying entity from the collection.

#### Connection arguments

| Argument | Type     | Description                                 |
| -------- | -------- | ------------------------------------------- |
| `first`  | `Int`    | Number of items to return (forward paging)  |
| `after`  | `String` | Cursor to start after (forward paging)      |
| `last`   | `Int`    | Number of items to return (backward paging) |
| `before` | `String` | Cursor to start before (backward paging)    |

`pageInfo` returns `hasNextPage`, `hasPreviousPage`, `startCursor`, and `endCursor`.

#### Read forward through pages

Request the first page, then pass the returned `endCursor` back as `after` to get the next page. Repeat while `pageInfo.hasNextPage` is `true`.

```graphql
query Page($urn: ListURN!, $first: Int, $after: String) {
  list(urn: $urn) {
    entries(first: $first, after: $after) {
      totalCount
      edges {
        node {
          urn
          record {
            name
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

**First page variables:**

```json variables
{ "urn": "urn:harmonic:list:YOUR_LIST_UUID", "first": 50, "after": null }
```

**Next page variables** — use `endCursor` from the previous response:

```json
{
  "urn": "urn:harmonic:list:YOUR_LIST_UUID",
  "first": 50,
  "after": "CURSOR_FROM_PREVIOUS_RESPONSE"
}
```

#### Paging with filters and sorting

`filter` and `orderBy` compose with pagination. Keep them stable across pages so cursors stay consistent.

```graphql
query FilteredPage(
  $urn: ListURN!
  $first: Int
  $after: String
  $filter: AttributeFilterInput
  $orderBy: [SortInput!]
) {
  list(urn: $urn) {
    entries(first: $first, after: $after, filter: $filter, orderBy: $orderBy) {
      totalCount
      edges {
        node {
          urn
          record {
            name
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

```json variables
{
  "urn": "urn:harmonic:list:YOUR_LIST_UUID",
  "first": 25,
  "after": null,
  "filter": {
    "status": {
      "attributeURN": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
      "in": ["OPTION_KEY_1", "OPTION_KEY_2"]
    }
  },
  "orderBy": [{ "metadataField": "UPDATED_AT", "descending": true }]
}
```

#### Best practices and limits

- **Treat cursors as opaque.** Pass `endCursor` / `startCursor` back verbatim; don't construct or parse them.
- **Keep `filter` and `orderBy` stable** across a paging run, or cursors may not line up.
- **Filter server-side** rather than fetching everything and trimming locally — it's faster and cheaper.
- **Mind query depth.** Nested connections still count against the 15-level depth limit.

## Core concepts

### Records

A **record** is a single entity your team tracks — a specific company, person, or investor. This is the reference for what records are, how they're typed, and the data attached to them. For task-based guides, see [Add your own context to companies](/docs/api-reference/workspace/common-workflows#add-your-own-context-to-companies) and [Import and enrich data](/docs/api-reference/workspace/common-workflows#import-and-enrich-data).

#### Record types

A **record type** defines the schema for a kind of entity. Every workspace ships with three built-in types, each with a stable, fixed URN:

| Record type | URN                                 |
| ----------- | ----------------------------------- |
| Company     | `urn:harmonic:record_type:company`  |
| Person      | `urn:harmonic:record_type:person`   |
| Investor    | `urn:harmonic:record_type:investor` |

A record type owns its attributes (the fields available on its records) and gives access to its records, the lists built on it, and its named views. Read one with its fields:

```graphql
query RecordType($urn: RecordTypeURN!) {
  recordType(urn: $urn) {
    urn
    name
    attributes {
      urn
      fieldName
      fieldType
    }
  }
}
```

#### Record

A record carries core details about an entity plus its attribute values. The same record can appear in many lists; its record-level values travel with it everywhere. Alongside its attributes, a record also holds a shared **`teamNote`** and a connection of file **`attachments`** — both visible to your whole workspace, both traveling with the record across every list. See [Add your own context to companies](/docs/api-reference/workspace/common-workflows#add-your-own-context-to-companies) for how to set notes and upload, list, or remove attachments. The record also exposes `updateEvents`, which show the last major events captured for that entity - for example, on a person entity, the person's job updates would be available here.

```graphql
query Record($urn: RecordURN!, $recordTypeUrn: RecordTypeURN!) {
  record(urn: $urn, recordTypeUrn: $recordTypeUrn) {
    urn
    name
    harmonicUrn # links back to the Harmonic entity, e.g. urn:harmonic:company:1
    avatarUrl
    createdAt
    updatedAt
    teamNote # shared note, visible across the workspace
    attachments(first: 10) {
      # files on the record (pitch decks, memos, …)
      totalCount
      edges {
        node {
          urn
          name
          extension
          contentUrl # signed, short-lived download URL
        }
      }
    }
    updateEvents {
      eventType
      eventDate
      detectedAt
    }
  }
}
```

> `recordTypeUrn` is required on both `record` and `records`. A query that omits it is rejected before execution.

New records aren't created with a standalone mutation — they enter through an import (`createImport`) or by adding a `harmonicUrn` to a list with `createListEntry`. See [Import and enrich data](/docs/api-reference/workspace/common-workflows#import-and-enrich-data).

#### Attributes

Records hold data in **attributes** (fields). There are two scopes:

- **Record attributes** live on the record type. Their values follow the record into every list it joins — use them for data that should be the same everywhere (an "Owner," a permanent score).
- **List attributes** live on a single list and apply only to that list's entries — use them for pipeline-specific data (a per-deal "Stage"). See [Lists](#lists).

There are two types of Record attributes you can use: Harmonic attributes and custom attributes. Harmonic attributes include data points on the Record such as "description", "last funding amount" and also workspace specific metadata such as "Date added to workspace". These are defined and maintained by Harmonic's database. Custom record attributes are attributes that you can create and customize to your workflows. In contrast, List attributes are always created and defined by you and specific for that list.

Both List and Record attributes share the same field types. Attribute **values** are opt-in when reading: pass the attribute URNs you want in `include`, and each comes back as a typed value you select by type.

| Value type         | Field                                 | Holds                                          |
| ------------------ | ------------------------------------- | ---------------------------------------------- |
| `StringValue`      | `stringValue`                         | Text, URL, email, single-select/status keys    |
| `NumberValue`      | `numberValue`                         | Number, currency, percent, traction, relevance |
| `DateValue`        | `dateValue`                           | Date                                           |
| `BooleanValue`     | `booleanValue`                        | Boolean                                        |
| `ArrayValue`       | `arrayConnectionValue(first, after)`  | Multi-select / string array — paginated        |
| `RecordArrayValue` | `recordConnectionValue(first, after)` | Record references — paginated                  |
| `UserArrayValue`   | `userConnectionValue(first, after)`   | User / owner references — paginated            |
| `UserValue`        | `userValue { … }`                     | Single user                                    |

##### Field types

The `fieldType` of an attribute determines how its value is stored and which filter operators apply. The same set applies to record and list attributes:

| Field type                                   | Value field (input) | Notes                                |
| -------------------------------------------- | ------------------- | ------------------------------------ |
| `STRING`                                     | `stringValue`       | Short text (max 500 characters)      |
| `NUMBER`                                     | `numberValue`       | `min`, `max`, `precision`            |
| `DATE`                                       | `dateValue`         | RFC 3339 timestamp                   |
| `BOOLEAN`                                    | `booleanValue`      | true/false                           |
| `URL` / `EMAIL`                              | `stringValue`       | URL / email string                   |
| `CURRENCY`                                   | `numberValue`       | Requires `currencyCode` (ISO 4217)   |
| `PERCENT`                                    | `numberValue`       | Percentage                           |
| `TRACTION`                                   | `numberValue`       | `metricType`, `unit`                 |
| `SINGLE_SELECT`                              | `stringValue`       | Value is an option **key**           |
| `MULTI_SELECT`                               | `arrayValue`        | Values are option **keys**           |
| `STATUS`                                     | `stringValue`       | Value is an option **key**           |
| `USER_REFERENCE` / `OWNER_REFERENCE`         | `arrayValue`        | User URNs                            |
| `RECORD_REFERENCE`                           | `arrayValue`        | Record URNs                          |
| `STRING_ARRAY` / `URL_ARRAY` / `EMAIL_ARRAY` | `arrayValue`        | Array of strings/URLs/emails         |
| `RELEVANCE`                                  | `numberValue`       | Harmonic relevance score (read-only) |
| `LIST_MEMBERSHIP`                            | —                   | System; reflects list membership     |

> For single-select, multi-select, and status fields you always work with an option's **key** (a UUID), never the on-screen label. However, the API allows you to create new options on the fly using labels. Read the field's metadata to map labels to keys.

#### Relationship to lists and views

A record's appearance in a list is an **entry**, which carries that list's attribute values. A record can belong to many lists at once. **Named views** are saved filters and sorts over a record type (or a list); see [Lists](#lists) and [Named views](#named-views).

### Lists

A **list** groups records for a purpose — a sourcing pipeline, a portfolio, a research shortlist. This is the reference for what lists are and how they're structured. For the end-to-end pipeline guide, see [Manage a sourcing workflow](/docs/api-reference/workspace/common-workflows#manage-a-sourcing-workflow).

#### What a list is

A list tracks a single record type — a company list holds companies, a people list holds people. A record can belong to many lists at once. This is how workflows are organized:

```
List (one record type)
├── List attributes → values stored on entries
├── Entries (a record's membership in this list)
└── Named views
```

Read a list's metadata and its fields:

```graphql
query List($urn: ListURN!) {
  list(urn: $urn) {
    urn
    name
    recordType {
      name
      urn
    }
    createdBy {
      email
    }
  }
}
```

Create a list by passing a `recordTypeUrn` and a `name` — the list is saved to your workspace automatically:

```graphql
mutation CreateList($input: CreateListInput!) {
  createList(input: $input) {
    list {
      urn
      name
      recordType {
        name
      }
    }
  }
}
```

```json variables
{
  "input": {
    "recordTypeUrn": "urn:harmonic:record_type:company",
    "name": "Active Pipeline"
  }
}
```

#### List entries

A **list entry** is a record's membership in a specific list. Entries hold the values for that list's attributes; the underlying record holds record-level values. Reading and writing entries is the day-to-day of working with a list. Entries are a connection on `list`, and you `include` the attribute values you want (record-level and list-level URNs can be mixed):

```graphql
query ListEntries($urn: ListURN!, $include: [AttributeURN!], $after: String) {
  list(urn: $urn) {
    name
    entries(first: 50, after: $after) {
      totalCount
      edges {
        node {
          urn
          record {
            name
            urn
            harmonicUrn
          }
          attributeValues(include: $include) {
            attributeUrn
            value {
              union {
                ... on StringValue {
                  stringValue
                }
              }
            }
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

The `entries` connection also accepts `filter` and `orderBy`. Add a single entry with `createListEntry`, change one with `updateListEntry`, and remove one with `deleteListEntry` (which removes the record from the list without deleting the record). To act on many at once, use the bulk mutations covered in [Manage a sourcing workflow](/docs/api-reference/workspace/common-workflows#manage-a-sourcing-workflow).

#### List attributes

A **list attribute** is a field defined on a single list. Its values live on that list's entries and apply only there — a per-deal "Stage," "Priority," or "Deal Size." For data that should follow a record across every list, use a record attribute instead; see [Records](#records).

List attributes and record attributes share the same field types and metadata shapes. Create one with `createListAttribute`:

```graphql
mutation CreateListAttribute($input: CreateListAttributeInput!) {
  createListAttribute(input: $input) {
    listAttribute {
      urn
      fieldName
      fieldType
    }
  }
}
```

```json variables
{
  "input": {
    "listUrn": "urn:harmonic:list:YOUR_LIST_UUID",
    "fieldName": "Priority",
    "fieldType": "SINGLE_SELECT",
    "fieldMetadata": {
      "select": {
        "options": [
          { "label": "High", "color": 1 },
          { "label": "Medium", "color": 5 },
          { "label": "Low", "color": 10 }
        ]
      }
    }
  }
}
```

> Each select option gets a stable `key` (a UUID) from Harmonic. That key — not the label — is what you use to set or filter the value, so read the field back to get its keys. The per-list field budget is **30 fields per kind**, separate from the record type's own budget.

#### Relationship to records and views

Each entry points at one record; that record can appear in many lists. A list can carry saved **named views** — reusable filter, sort, and column configurations — see [Named views](#named-views).

### Named views

A **named view** is a saved filter, sort, and column configuration over a list or a record type. This is the reference for how views are structured and the operators they support. For the how-to guide, see [Drive Workflows with named views](/docs/api-reference/workspace/common-workflows#drive-workflows-with-named-views).

#### What a named view holds

A named view belongs to either a **list** or a **record type** — exactly one. Reading one back shows everything it applies:

```graphql
query NamedView($urn: NamedViewUnionURN!) {
  namedView(urn: $urn) {
    urn
    name
    description
    isDefault
    filter # serialized filter (JSON)
    columns {
      attributeUrn
      displayOrder
      columnWidth
    }
    sorts {
      sortOrderUrn
      descending
      priority
    }
    list {
      name
      urn
    }
    recordType {
      name
      urn
    }
  }
}
```

`list` is populated for list views and `recordType` for record-type views; the other is `null`. Setting a view's `isDefault` to `true` makes it the default for its list or record type (and unsets the previous default).

#### Saved filters

A view's filter is an `AttributeFilterInput`. Each leaf condition picks a **condition key** for the field-type family, then provides `attributeURN` plus one or more operators:

```
filter: {
  <conditionKey>: {
    attributeURN: "<attribute URN>"
    <operator>: <value>
  }
}
```

Two things to get right: the key is `attributeURN` (capital `URN`) and its value is the attribute's **full URN**, not a field name; and the condition key is the field-type _family_, not the literal type (text fields use `text`; the built-in record name uses `name`).

| Condition key                                                                                         | Use for                  | Operators (in addition to `isNull`)                                                                         |
| ----------------------------------------------------------------------------------------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| `name`, `text`, `email`                                                                               | String fields            | `equals`/`notEquals`, `contains`/`notContains`, `startsWith`, `endsWith`, `in`/`notIn`, lexical comparisons |
| `number`, `currency`, `percent`, `traction`, `relevance`                                              | Numeric fields           | `equals`/`notEquals`, `lessThan(OrEqual)`, `greaterThan(OrEqual)`, `in`/`notIn`                             |
| `date`                                                                                                | `DATE`                   | `equals`, `before(OrEqual)`, `after(OrEqual)` — each takes a `preset`, `time`, or `offsetDays` operand      |
| `checkbox`                                                                                            | `BOOLEAN`                | `equals`                                                                                                    |
| `singleSelect`, `status`                                                                              | Select fields            | `equals`/`notEquals`, `in`/`notIn` (match on option **key**)                                                |
| `multiSelect`, `record`, `user`, `list`, `harmonicReference`, `stringArray`, `urlArray`, `emailArray` | Multi-value & references | `containsAnyOf`, `containsAllOf`, `excludesAnyOf`, `excludesAllOf`, `equals`/`notEquals`                    |
| `owner`                                                                                               | `OWNER_REFERENCE`        | `equals`/`notEquals`, `in`/`notIn`                                                                          |
| `harmonicUrn`                                                                                         | Match by Harmonic entity | `in`/`notIn`                                                                                                |

Conditions at the same level combine with **AND**. Use `and` / `or` (arrays of `AttributeFilterInput`) for nested logic. Array conditions (`stringArray`, `urlArray`, `emailArray`) also support `contains` / `notContains` on elements.

> **Saved views require the wrapper:** views only accept "flat" conditions, meaning you can either `and` or `or` a list of conditions together in the view's `filter`. You must provide a list of conditions (even if it's empty), wrapping them in a single `and` or `or` — e.g. `{ "and": [ { … } ] }`. Inline `entries(filter:)` accepts bare leaves.

> Filter and sort against single-select/status fields by the option's **key**, not the label.

#### Sorting

A view's sort is an `orderBy` array of `SortInput`. List several for a multi-level sort — earlier entries take precedence. Each entry provides **one** of:

- `metadataField` — a built-in field: `ID`, `NAME`, `CREATED_AT`, `UPDATED_AT`, `CREATED_BY`, `SEARCH_RANK`.
- `sortOrderUrn` — an attribute URN, or a metadata-field URN.

plus an optional `descending` (defaults to `false`). `SortOrderURN` accepts:

| Form             | Example                                                    |
| ---------------- | ---------------------------------------------------------- |
| Record attribute | `urn:harmonic:record_attribute:company:external_headcount` |
| List attribute   | `urn:harmonic:list_attribute:{list_uuid}:NUMB000`          |
| Metadata field   | `urn:harmonic:metadata_field:created_at` · `:id`           |

Saved views store sorts in the `sortOrderUrn` form. When you save a view, each sort also takes a required `priority` (0-based).

#### View configuration

A view's `columns` define which attributes appear and in what order — each column takes an `attributeUrn` and an optional `columnWidth`; column order comes from the array order; `displayOrder` appears on read responses. Updating a view's `columns` or `sorts` **replaces** the whole set rather than merging.

#### Relationship to records and lists

A named view is always scoped to one [list](#lists) or one [record type](#records). List views curate that list's entries; record-type views curate every record of that type. The filter and sort defined here are the same constructs you pass inline when reading entries or records — a named view just saves them under a name for reuse.

## Common Workflows

### Manage a sourcing workflow

A sourcing pipeline is a list of companies you're evaluating, each moving through stages — sourced, evaluating, passed — with an owner and notes attached. This section walks the full loop: stand up a pipeline, add companies, track their stage and owner, review what's active, and update many at once as deals move.

In Workspace terms, a pipeline is a **list**, each company in it is an **entry**, and the columns you track (Stage, Owner, Priority) are **list attributes** — fields scoped to that one pipeline. A field you'd rather share across every list a company appears in is a **record attribute** instead; see [Build a Company Database](#add-your-own-context-to-companies).

#### Create the pipeline

A pipeline is a list that tracks one record type — here, companies. Use a `recordTypeUrn` from your [first request](/docs/api-reference/workspace/getting-started#authentication) — the list is saved to your workspace automatically.

```graphql
mutation CreateList {
  createList(
    input: {
      recordTypeUrn: "urn:harmonic:record_type:company"
      name: "Active Pipeline"
    }
  ) {
    list {
      urn
      name
    }
  }
}
```

Keep the returned list `urn` — every step below references it.

#### Add a Stage field

Add a "Stage" field to the pipeline so each company has a place in the funnel. Use the **`STATUS`** field type — it's purpose-built for tracking where something sits in a workflow, and is the preferred way to model a stage or status (rather than a generic single-select). This is a list attribute (specific to this pipeline):

```graphql
mutation AddStageField {
  createListAttribute(
    input: {
      listUrn: "urn:harmonic:list:YOUR_LIST_UUID"
      fieldName: "Stage"
      fieldType: STATUS
      fieldMetadata: {
        status: {
          options: [
            { label: "Sourced", color: 0 }
            { label: "Evaluating", color: 5 }
            { label: "Passed", color: 1 }
          ]
        }
      }
    }
  ) {
    listAttribute {
      urn # the AttributeURN you'll set values against
      fieldName
      fieldType
    }
  }
}
```

You set each option's `label` and `color`; Harmonic returns a stable `key` (a UUID) for each. When you set or filter by an option, you use the **key**, not the label — so read the attribute back to get the keys. (`color` is an integer `0`–`16`.)

To track who owns each deal, add an owner field the same way with `fieldType: OWNER_REFERENCE` — its values are user URNs.

#### Add companies to the pipeline

Add a company and set its Stage in one call. Reference an existing record by `recordUrn`, or pass a `harmonicUrn` to drop in a Harmonic company directly — Harmonic creates the underlying record if one doesn't exist yet.

```graphql
mutation AddEntry {
  createListEntry(
    input: {
      selection: {
        listUrn: "urn:harmonic:list:YOUR_LIST_UUID"
        harmonicUrn: "urn:harmonic:company:1"
      }
      attributeValues: [
        {
          attributeUrn: "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000"
          stringValue: "OPTION_KEY_FOR_SOURCED"
        }
      ]
    }
  ) {
    listEntry {
      urn
      record {
        name
        urn
      }
    }
    recordCreated # true if a new record was created for the harmonicUrn
  }
}
```

`createListEntry` adds one company at a time. To add **many** at once — including companies not yet in your workspace, resolved by website or LinkedIn — use a bulk import; see [Import and Enrich Data](#import-and-enrich-data).

#### Move a company through stages

As a deal progresses, update its entry. Identify the entry by its `urn`, or by `selection` (list + record). Only the values you pass change.

```graphql
mutation UpdateListEntry($input: UpdateListEntryInput!) {
  updateListEntry(input: $input) {
    listEntry {
      urn
      updatedAt
    }
  }
}
```

**By entry URN** — advance the stage and set a score:

```json variables
{
  "input": {
    "urn": "urn:harmonic:list_entry:YOUR_ENTRY_UUID",
    "attributeValues": [
      {
        "attributeUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
        "stringValue": "OPTION_KEY_FOR_EVALUATING"
      },
      {
        "attributeUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:NUMB000",
        "numberValue": 100
      }
    ]
  }
}
```

**By selection** (when you know the company but not the entry URN):

```json
{
  "input": {
    "selection": {
      "listUrn": "urn:harmonic:list:YOUR_LIST_UUID",
      "recordUrn": "urn:harmonic:record:YOUR_RECORD_UUID"
    },
    "attributeValues": [
      {
        "attributeUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
        "stringValue": "OPTION_KEY_FOR_EVALUATING"
      }
    ]
  }
}
```

#### Review what's active

Read the pipeline back, filtered to the stage you're reviewing and sorted newest-first. Pass the attribute values you want via `include` — nothing comes back unless you ask for it.

```graphql
query ReadList($listUrn: ListURN!, $stageUrn: AttributeURN!) {
  list(urn: $listUrn) {
    name
    entries(
      first: 25
      filter: {
        status: { attributeURN: $stageUrn, equals: "OPTION_KEY_FOR_EVALUATING" }
      }
      orderBy: [{ metadataField: CREATED_AT, descending: true }]
    ) {
      totalCount
      edges {
        node {
          urn
          record {
            name
            harmonicUrn
          }
          attributeValues(include: [$stageUrn]) {
            attributeUrn
            value {
              union {
                ... on StringValue {
                  stringValue
                }
              }
            }
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

```json variables
{
  "listUrn": "urn:harmonic:list:YOUR_LIST_UUID",
  "stageUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000"
}
```

When you filter a single-select or status field, match on the option's **key**, not the label. The full operator set and multi-condition logic live in [Drive workflows with named views](#drive-workflows-with-named-views) and [Views](/docs/api-reference/workspace/core-concepts#named-views); page through results with [Pagination](/docs/api-reference/workspace/getting-started#pagination).

#### Update many companies at once

When a batch of deals moves together, don't loop one at a time. Bulk mutations take a **selection** that targets entries either explicitly (by URN) or dynamically (by filter):

| Selection field           | Targets                                      |
| ------------------------- | -------------------------------------------- |
| `entryUrns`               | Specific list entries, by `ListEntryURN`     |
| `recordUrns`              | Specific records, by `RecordURN`             |
| `harmonicUrns`            | Specific Harmonic entities, by `Urn`         |
| `fromListSelection`       | Entries from a source list matching a filter |
| `fromRecordTypeSelection` | Records of a record type matching a filter   |

##### Bulk update pipeline entries

Move everything currently in one stage to another in a single request:

```graphql
mutation UpdateListEntries($input: UpdateListEntriesInput!) {
  updateListEntries(input: $input) {
    success
    updatedCount
  }
}
```

**By entry URNs:**

```json variables
{
  "input": {
    "targetListUrn": "urn:harmonic:list:YOUR_LIST_UUID",
    "selection": {
      "entryUrns": [
        "urn:harmonic:list_entry:UUID_1",
        "urn:harmonic:list_entry:UUID_2"
      ]
    },
    "attributeValues": [
      {
        "attributeUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
        "stringValue": "EVALUATING_OPTION_KEY"
      }
    ]
  }
}
```

**By filter** — advance every "Sourced" entry at once:

```json
{
  "input": {
    "targetListUrn": "urn:harmonic:list:YOUR_LIST_UUID",
    "selection": {
      "fromListSelection": {
        "fromListUrn": "urn:harmonic:list:YOUR_LIST_UUID",
        "filter": {
          "status": {
            "attributeURN": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
            "equals": "SOURCED_OPTION_KEY"
          }
        },
        "limit": 500
      }
    },
    "attributeValues": [
      {
        "attributeUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
        "stringValue": "EVALUATING_OPTION_KEY"
      }
    ]
  }
}
```

##### Bulk update companies

To change record-level data (data that follows the company across every list), use `updateRecords` with a record selection:

```graphql
mutation UpdateRecords($input: UpdateRecordsInput!) {
  updateRecords(input: $input) {
    success
    updatedCount
  }
}
```

```json variables
{
  "input": {
    "recordTypeUrn": "urn:harmonic:record_type:company",
    "selection": {
      "fromRecordTypeSelection": {
        "fromRecordTypeUrn": "urn:harmonic:record_type:company",
        "filter": {
          "number": {
            "attributeURN": "urn:harmonic:record_attribute:company:external_headcount",
            "greaterThanOrEqual": 1000
          }
        }
      }
    },
    "attributeValues": [
      {
        "attributeUrn": "urn:harmonic:record_attribute:company:BOOL001",
        "booleanValue": true
      }
    ]
  }
}
```

##### Promote top prospects to another list

`createListEntries` copies a selection into another list — for example, the highest-scoring prospects into a "Shortlist." Companies already in the target are skipped (counted in `skippedCount`).

```graphql
mutation CreateListEntries($input: CreateListEntriesInput!) {
  createListEntries(input: $input) {
    success
    createdCount
    skippedCount # records already in the target list
    notFoundCount
    createdEntryUrns
  }
}
```

```json variables
{
  "input": {
    "targetListUrn": "urn:harmonic:list:TARGET_UUID",
    "selection": {
      "fromListSelection": {
        "fromListUrn": "urn:harmonic:list:SOURCE_UUID",
        "filter": {
          "number": {
            "attributeURN": "urn:harmonic:list_attribute:SOURCE_UUID:NUMB000",
            "greaterThanOrEqual": 80
          }
        },
        "sort": [
          {
            "sortOrderUrn": "urn:harmonic:list_attribute:SOURCE_UUID:NUMB000",
            "descending": true
          }
        ],
        "limit": 100
      }
    },
    "attributeValues": []
  }
}
```

To clear out stale entries, `deleteListEntries` takes the same selection shape and removes the records from the list without deleting the records themselves.

> **Bulk limits.** A filter-based selection (`fromListSelection` / `fromRecordTypeSelection`) caps at **10,000 items** per request (`limit`, default 10,000). For larger jobs, page through with successive filtered calls.

#### Save as a named view

Once you've landed on a useful filter and sort — say, "Evaluating, newest first" — save it as a named view so you and your team return to the same view every time. See [Drive workflows with named views](#drive-workflows-with-named-views).

### Add your own context to companies

Create a clean, structured dataset of companies that you can filter, sort, and keep current: your own scoring, your own tags, your own notes, sitting alongside Harmonic's enrichment data. This section shows how to shape that dataset, add the custom fields you need, and query it.

The companies themselves are **records** of the company record type. Data you attach here lives on the record and travels with the company into every list it ever joins — which is exactly what you want for a shared, canonical dataset. (Data that should be specific to one pipeline belongs on a list instead; see [Manage a sourcing workflow](#manage-a-sourcing-workflow).)

#### See what fields you already have

Before adding anything, look at the company record type and its current fields, so you don't duplicate one:

```graphql
query RecordType($urn: RecordTypeURN!) {
  recordType(urn: $urn) {
    urn
    name
    description
    attributes {
      urn
      fieldName
      fieldType
      readOnly
      enriched
    }
  }
}
```

```json variables
{ "urn": "urn:harmonic:record_type:company" }
```

#### Add a custom attribute

To capture your own data — a score, an investment stage, a check size — create a record attribute. Pass the record type, a unique `fieldName`, a `fieldType`, and the matching `fieldMetadata` block (the metadata key matches the field type).

```graphql
mutation CreateRecordAttribute($input: CreateRecordAttributeInput!) {
  createRecordAttribute(input: $input) {
    recordAttribute {
      urn
      fieldName
      fieldType
    }
  }
}
```

**A single-select stage:**

```json variables
{
  "input": {
    "recordTypeUrn": "urn:harmonic:record_type:company",
    "fieldName": "Investment Stage",
    "fieldType": "SINGLE_SELECT",
    "fieldMetadata": {
      "select": {
        "options": [
          { "label": "Seed", "color": 0 },
          { "label": "Series A", "color": 5 },
          { "label": "Series B", "color": 10 }
        ]
      }
    }
  }
}
```

**A numeric score:**

```json
{
  "input": {
    "recordTypeUrn": "urn:harmonic:record_type:company",
    "fieldName": "Score",
    "fieldType": "NUMBER",
    "fieldMetadata": { "number": { "min": 0, "max": 100, "precision": 0 } }
  }
}
```

**A currency field** (requires an ISO 4217 `currencyCode`):

```json
{
  "input": {
    "recordTypeUrn": "urn:harmonic:record_type:company",
    "fieldName": "Check Size",
    "fieldType": "CURRENCY",
    "fieldMetadata": { "currency": { "currencyCode": "USD", "precision": 2 } }
  }
}
```

For select fields, you set each option's `label` and `color`; Harmonic returns a stable `key` (a UUID) per option. Read the attribute back to get the keys — the key is what you use to set or filter a value, not the label.

> **Field budget.** You can add up to **30 fields of each kind** per record type (and, separately, per list). Related types share a kind: short text, URLs, emails, single-selects, and statuses all draw from one pool of 30; numbers/currency/percent/traction share another; multi-value types share another. Field names must be unique within the type, and text values can be up to 500 characters. The configured limits are exposed on `recordType.storageLimits`.

#### Query the database

Read companies of the type with `records`, narrowing with a `filter` and ordering with `orderBy`. Filter server-side rather than pulling everything down.

```graphql
query RecordsOfType(
  $urn: RecordTypeURN!
  $filter: AttributeFilterInput
  $orderBy: [SortInput!]
  $first: Int
  $after: String
) {
  recordType(urn: $urn) {
    name
    records(first: $first, after: $after, filter: $filter, orderBy: $orderBy) {
      totalCount
      edges {
        node {
          urn
          name
          harmonicUrn
          createdAt
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

```json variables
{
  "urn": "urn:harmonic:record_type:company",
  "first": 25,
  "after": null,
  "orderBy": [{ "metadataField": "CREATED_AT", "descending": true }],
  "filter": {
    "number": {
      "attributeURN": "urn:harmonic:record_attribute:company:external_headcount",
      "greaterThanOrEqual": 1000
    }
  }
}
```

A filter targets one attribute by its URN and applies operators that depend on the field type (`number` for numeric fields, `text` for strings, `singleSelect` for selects, and so on). The full operator set and `and` / `or` nesting are in [Views](/docs/api-reference/workspace/core-concepts#named-views). Page large results with [Pagination](/docs/api-reference/workspace/getting-started#pagination).

#### Read a company's data

Get a single company and the specific fields you need. Attribute values are **opt-in**: pass the URNs you want in `include`, and each comes back as a typed value, so you select the field matching its type.

```graphql
query RecordValues(
  $urn: RecordURN!
  $recordTypeUrn: RecordTypeURN!
  $include: [RecordAttributeURN!]
) {
  record(urn: $urn, recordTypeUrn: $recordTypeUrn) {
    name
    harmonicUrn
    attributeValues(include: $include) {
      attributeUrn
      value {
        union {
          __typename
          ... on StringValue {
            stringValue
          }
          ... on NumberValue {
            numberValue
          }
          ... on DateValue {
            dateValue
          }
          ... on BooleanValue {
            booleanValue
          }
        }
      }
    }
  }
}
```

```json variables
{
  "urn": "urn:harmonic:record:a78e2221-721e-55e3-95e6-b5398c3c74bd",
  "recordTypeUrn": "urn:harmonic:record_type:company",
  "include": ["urn:harmonic:record_attribute:company:external_headcount"]
}
```

For a quick, untyped read while debugging, `attributeValueMap(include: [...])` returns a plain JSON object keyed by display name. Use `attributeValues` when you need typed, stable access. The full set of value types is summarized in [Records](/docs/api-reference/workspace/core-concepts#records).

> **`recordTypeUrn` is required** on both `record` and `records`. A query that omits it is rejected before execution.

#### Keep records current

Update a company's fields with `updateRecord` — only the fields you pass change. `teamNote` sets a shared note visible to your whole team.

```graphql
mutation UpdateRecord($input: UpdateRecordInput!) {
  updateRecord(input: $input) {
    record {
      urn
      name
      updatedAt
      teamNote
    }
  }
}
```

```json variables
{
  "input": {
    "urn": "urn:harmonic:record:YOUR_RECORD_UUID",
    "attributeValues": [
      {
        "attributeUrn": "urn:harmonic:record_attribute:company:TEXT001",
        "stringValue": "Updated"
      }
    ],
    "teamNote": "Shared note visible to the whole team"
  }
}
```

To bring companies in from outside, or to keep records synced with fresh Harmonic data, see [Import and Enrich Data](#import-and-enrich-data). To update thousands of records at once by filter, see [Update many companies at once](#update-many-companies-at-once).

#### Add notes

A record carries a **`teamNote`** — a shared free-text note visible to everyone in your workspace — that travels with the company across every list it joins. Set it inline with any field update via `updateRecord` (shown in [Keep records current](#keep-records-current) above), and read it back as an ordinary field on a record (`record { teamNote }` — no `include` needed).

When you know the company but not its record URN, the dedicated `updateTeamNote` mutation takes a **selection** instead — so you can write a note straight against a `harmonicUrn`, and Harmonic resolves (or creates) the underlying record for you:

```graphql
mutation UpdateTeamNote($input: UpdateTeamNoteInput!) {
  updateTeamNote(input: $input) {
    record {
      urn
      name
      teamNote
    }
  }
}
```

```json variables
{
  "input": {
    "note": "Met the founders at the summit — strong technical team, revisiting next quarter.",
    "selection": {
      "recordTypeUrn": "urn:harmonic:record_type:company",
      "harmonicUrn": "urn:harmonic:company:1"
    }
  }
}
```

A selection takes the `recordTypeUrn` plus **exactly one** of `recordUrn` or `harmonicUrn`. The note is a plain string; passing an empty string clears it.

#### Add attachments

Beyond notes, you can attach **files** — pitch decks, memos, diligence docs — to a company (or person) record. Attachments hang off the **record**, so they travel with the company across every list, and they're the same files your team sees in the Harmonic app. First resolve the record URN (from a list entry's `record.urn`, or from `records(urns: […], recordTypeUrn: …)`); every attachment call targets it.

##### Upload a file

`createRecordAttachment` is the one call in the Workspace API that isn't plain JSON: uploading bytes means sending a **multipart request** per the [GraphQL multipart request spec](https://github.com/jaydenseric/graphql-multipart-request-spec), so post it as `multipart/form-data` with `curl -F` rather than a JSON body. A single request replaces the legacy three-step (initiate → upload bytes → complete) flow — Harmonic runs all three server-side and returns the finalized attachment.

```bash
curl -X POST "https://api.harmonic.ai/graphql/v2" \
  -H "apikey: YOUR_API_KEY" \
  -F operations='{"query":"mutation CreateRecordAttachment($record: RecordURN!, $file: Upload!) { createRecordAttachment(input: { record: $record, file: $file }) { attachment { urn name extension sizeBytes contentUrl uploadedAt createdAt updatedAt } } }","variables":{"record":"urn:harmonic:record:550e8400-e29b-41d4-a716-446655440000","file":null}}' \
  -F map='{"0":["variables.file"]}' \
  -F 0=@./pitch-deck.pdf
```

The `map` wires the uploaded file part (`0`) to the `file` variable; `operations` carries the query and the rest of the variables. One file per request, up to **500 MB**.

##### List a company's attachments

`Record.attachments` is a paginated connection. `contentUrl` is a **signed, short-TTL download URL** minted lazily — it's only generated for rows where you actually request the field, and it expires, so fetch it when you're ready to download rather than caching it.

```graphql
query RecordAttachments($urn: RecordURN!, $recordTypeUrn: RecordTypeURN!) {
  record(urn: $urn, recordTypeUrn: $recordTypeUrn) {
    name
    attachments(first: 25) {
      totalCount
      edges {
        node {
          urn # urn:harmonic:user_uploaded_content:… — pass to update/delete
          name
          extension
          sizeBytes
          contentUrl # signed, short-lived download URL
          uploadedAt
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
}
```

##### Rename or delete an attachment

Both take the attachment `urn` (from the connection above) plus the `record` it belongs to. `updateRecordAttachment` currently changes the display name; `deleteRecordAttachment` removes the file and returns its `deletedUrn`.

```graphql
mutation RenameAttachment($input: UpdateRecordAttachmentInput!) {
  updateRecordAttachment(input: $input) {
    attachment {
      urn
      name
    }
  }
}

# Same input, minus `name`, on deleteRecordAttachment(input: DeleteRecordAttachmentInput!) { deletedUrn } to remove it.
```

```json variables
{
  "input": {
    "attachment": "urn:harmonic:user_uploaded_content:YOUR_ATTACHMENT_UUID",
    "record": "urn:harmonic:record:YOUR_RECORD_UUID",
    "name": "Q3 Board Deck"
  }
}
```

### Import and enrich data

When your companies or people live somewhere else — a spreadsheet, a CRM, another internal system — you bring them into Workspace with an import. Each row is matched to a Harmonic entity automatically, so the data arrives already enriched with headcount, funding, web traffic, and more. This section covers importing, matching against records you already have, and keeping enriched data fresh.

One mutation does the heavy lifting: `createImport` bulk-loads **records and list entries**. Each row resolves to a Harmonic entity — by **canonical identifiers** (website/LinkedIn for companies; email/LinkedIn for people), or by an explicit Harmonic URN — and any record not already in your workspace is created on the fly. Imports run asynchronously, so you submit a job and poll it for progress. (There is no separate "create record" mutation; this is the create path.)

Two modes of targeting:

- Pass a **`listURN`** to add the resolved companies or people to that list as **entries** (creating any missing records). This is the bulk way to fill a list.
- Pass a **`recordTypeURN`** instead to create or update records only, with no list membership.

With **`mode: UPSERT`**, rows that match an existing record update it (and its attribute values) rather than creating a duplicate — this is how you match against data you already have.

#### Submit an import

```graphql
mutation CreateImport($input: CreateImportInput!) {
  createImport(input: $input) {
    importTask {
      urn
      status # PROCESSING | SUCCESS | FAILED
      totalRecords
      successRecords
      failedRecords
      processingRecords
      progressPercent
      createdAt
      list {
        name
        urn
      }
    }
  }
}
```

`CreateImportInput` fields:

| Field           | Type                   | Notes                                      |
| --------------- | ---------------------- | ------------------------------------------ |
| `sourceSystem`  | `SourceSystem!`        | use value `API` for this field.            |
| `rows`          | `[ImportEntryInput!]!` | The rows to import (max 1,000 per request) |
| `listURN`       | `ListURN`              | Import into a list (creates entries)       |
| `recordTypeURN` | `RecordTypeURN`        | Record-only import (no list membership)    |
| `fileName`      | `String`               | Optional label                             |
| `mode`          | `ImportMode`           | `INSERT` or `UPSERT`                       |

Each `ImportEntryInput` takes a `rowIndex` (required) and one of `harmonicUrn` or `canonicalInput`, plus optional `attributeValues` and `externalRowID`.

##### Import companies by canonical identifiers

Most often you'll have a website or LinkedIn URL rather than a Harmonic URN. Harmonic resolves each row to a company from those:

```json variables
{
  "input": {
    "listURN": "urn:harmonic:list:YOUR_LIST_UUID",
    "sourceSystem": "API",
    "fileName": "company_import_canonical.csv",
    "rows": [
      {
        "rowIndex": 0,
        "canonicalInput": {
          "companyCanonicals": {
            "websiteURL": "https://example.com",
            "linkedinURL": "https://linkedin.com/company/example"
          }
        },
        "attributeValues": []
      }
    ]
  }
}
```

`WorkspaceCompanyCanonicalInput` also accepts `twitterURL`, `facebookURL`, `instagramURL`, `crunchbaseURL`, `pitchbookURL`, and `angellistURL`.

##### Import companies by Harmonic URN

If you already hold Harmonic URNs, reference them directly and set initial field values per row:

```json
{
  "input": {
    "listURN": "urn:harmonic:list:YOUR_LIST_UUID",
    "sourceSystem": "API",
    "fileName": "company_import.csv",
    "rows": [
      {
        "rowIndex": 0,
        "harmonicUrn": "urn:harmonic:company:1",
        "attributeValues": [
          {
            "attributeUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
            "stringValue": "High priority target"
          }
        ]
      },
      {
        "rowIndex": 1,
        "harmonicUrn": "urn:harmonic:company:1234",
        "attributeValues": []
      }
    ]
  }
}
```

##### Import people by canonical identifiers

For people, `PersonCanonicalInput` accepts `primaryEmail` and `linkedinURL`:

```json
{
  "input": {
    "listURN": "urn:harmonic:list:YOUR_PEOPLE_LIST_UUID",
    "sourceSystem": "API",
    "fileName": "people_import.csv",
    "rows": [
      {
        "rowIndex": 0,
        "canonicalInput": {
          "personCanonicals": {
            "primaryEmail": "jane@example.com",
            "linkedinURL": "https://linkedin.com/in/janedoe"
          }
        },
        "attributeValues": []
      }
    ]
  }
}
```

##### Import records without a list

Pass `recordTypeURN` instead of `listURN` to create or resolve records with no list membership — useful for seeding the company database itself:

```json
{
  "input": {
    "recordTypeURN": "urn:harmonic:record_type:company",
    "sourceSystem": "API",
    "rows": [{ "rowIndex": 0, "harmonicUrn": "urn:harmonic:company:1" }]
  }
}
```

#### Track import progress

Imports are asynchronous. Poll `importTask` until `status` is `SUCCESS` or `FAILED`:

```graphql
query ImportTask($urn: ImportTaskURN!) {
  importTask(urn: $urn) {
    urn
    status
    target # LIST_IMPORT | RECORD_IMPORT | NETWORK_IMPORT
    sourceSystem
    totalRecords
    successRecords
    failedRecords
    processingRecords
    progressPercent # 0.0 – 100.0
    fileName
    createdAt
    updatedAt
    lastProcessUpdateAt
    recordType {
      name
      urn
    }
    list {
      name
      urn
    }
  }
}
```

```json variables
{ "urn": "urn:harmonic:import_task:YOUR_IMPORT_TASK_UUID" }
```

When rows fail, inspect them individually through the `importEntries` connection, optionally filtered by `RowStatus` (`PROCESSING`, `SUCCESS`, `FAILED`):

```graphql
query ImportEntries($urn: ImportTaskURN!) {
  importTask(urn: $urn) {
    importEntries(status: FAILED, paginationInput: { first: 50 }) {
      totalCount
      edges {
        node {
          urn
          rowIndex
          status
          errorMessage
          errorCode
          harmonicUrn
          resolvedAt
          record {
            urn
            name
          }
          fieldStatuses {
            fieldName
            status
            errorMessage
            isMatchedCanonical
          }
        }
      }
    }
  }
}
```

#### Enrich what you've imported

Imported records automatically carry Harmonic's enrichment fields — headcount, funding, web traffic, social links, and more. Discover the catalog per record type, then read, filter, or sort against any field using its `recordAttributeUrn`:

```graphql
query HarmonicAttributes {
  workspace {
    companyHarmonicAttributes {
      harmonicAttributeKey # e.g. "company.external_headcount"
      fieldType
      defaultDisplayName
      recordAttributeUrn # the AttributeURN to filter/sort/include against
      isFilterable
      isSortable
      categories
    }
    personHarmonicAttributes {
      harmonicAttributeKey
      fieldType
      defaultDisplayName
      recordAttributeUrn
    }
    investorHarmonicAttributes {
      harmonicAttributeKey
      fieldType
      defaultDisplayName
      recordAttributeUrn
    }
  }
}
```

#### Keep imported data current

To re-sync rows you've already imported, run the import again with `mode: UPSERT` — matched records update in place. If `mode: UPSERT` is not specified and your input contains rows that already exist in your list, the row will be marked as duplicate and provided attribute values will be ignored to prevent against accidental overwrites.

```json
{
  "input": {
    "listURN": "urn:harmonic:list:YOUR_LIST_UUID",
    "sourceSystem": "API",
    "fileName": "company_import.csv",
    "mode": "UPSERT" /* Set mode to UPSERT explictly to update any existing attribute values */,
    "rows": [
      {
        "rowIndex": 0,
        "harmonicUrn": "urn:harmonic:company:1",
        "attributeValues": [
          {
            "attributeUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
            "stringValue": "Very High priority target"
          }
        ]
      },
      {
        "rowIndex": 1,
        "harmonicUrn": "urn:harmonic:company:1234",
        "attributeValues": []
      }
    ]
  }
}
```

`eventType` is one of `PERSON_HEADLINE_UPDATE`, `PERSON_DESCRIPTION_UPDATE`, `PERSON_JOB_STARTED`, `PERSON_JOB_ENDED`, `COMPANY_STEALTH_EMERGENCE` — useful for keeping an external CRM in sync.

#### Import constraints

- A single `createImport` accepts at most **1,000 rows**. Split larger jobs across multiple requests.
- Imports are **asynchronous** — always poll `importTask` rather than assuming immediate completion.
- Tag each row with `externalRowID` to correlate import results with your source system across retries.

### Drive workflows with named views

A **named view** is a saved filter, sort, and set of columns over a **list** or **record type** — a reusable definition of exactly the records that matter for a given workflow. Settle on a filter and sort, save them as a view, and your integration can return to that same focused set on every run to drive what comes next: automations, notifications, CRM syncs, or other API-driven actions. Because the view owns the definition of "what matches," you tune the criteria in one place and every downstream workflow follows. The sections below cover shaping the filter, saving the view, and polling it to drive those actions.

#### Shape the filter and sort first

A view stores a filter and a sort, so it helps to settle on those by reading the data before you save. A filter targets one attribute by its URN and applies operators based on the field type; combine conditions with `and` / `or`.

```json
{
  "and": [
    {
      "or": [
        {
          "status": {
            "attributeURN": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
            "equals": "NEW_KEY"
          }
        },
        {
          "status": {
            "attributeURN": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
            "equals": "IN_PROGRESS_KEY"
          }
        }
      ]
    },
    {
      "number": {
        "attributeURN": "urn:harmonic:record_attribute:company:external_headcount",
        "greaterThan": 50
      }
    }
  ]
}
```

Sorting is an `orderBy` array — list multiple entries for multi-level sorts, earlier entries taking precedence. Each entry provides either a `metadataField` (`ID`, `NAME`, `CREATED_AT`, `UPDATED_AT`, `CREATED_BY`, `SEARCH_RANK`) or a `sortOrderUrn` (an attribute URN or a metadata-field URN like `urn:harmonic:metadata_field:created_at`). The complete operator and sort reference lives in [Views](/docs/api-reference/workspace/core-concepts#named-views).

> When filtering or sorting a single-select or status field, match on the option's **key** (a UUID), not the label. Read the field's `selectMetadata.options` / `statusMetadata.options` to map labels to keys.

#### See the views a list already has

```graphql
query ListNamedViews($urn: ListURN!) {
  list(urn: $urn) {
    name
    namedViews(first: 25) {
      totalCount
      edges {
        node {
          urn
          name
          description
          isDefault
        }
      }
    }
  }
}
```

Record-type views are read the same way via `recordType { namedViews { … } }`.

#### Save a view

`createNamedView` persists the filter, sort, and columns. Provide exactly one of `listUrn` or `recordTypeUrn`.

```graphql
mutation CreateNamedView($input: CreateNamedViewInput!) {
  createNamedView(input: $input) {
    namedView {
      urn
      name
      isDefault
      createdAt
    }
  }
}
```

**For a list** — a shared "high priority" review with chosen columns and a newest-first sort:

```json variables
{
  "input": {
    "listUrn": "urn:harmonic:list:YOUR_LIST_UUID",
    "name": "High priority companies",
    "description": "Active, high-priority entries",
    "filter": {
      "and": [
        {
          "status": {
            "attributeURN": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000",
            "equals": "ACTIVE_OPTION_KEY"
          }
        }
      ]
    },
    "columns": [
      {
        "attributeUrn": "urn:harmonic:record_attribute:company:external_headcount",
        "columnWidth": 200
      },
      { "attributeUrn": "urn:harmonic:list_attribute:YOUR_LIST_UUID:TEXT000" }
    ],
    "sorts": [
      {
        "sortOrderUrn": "urn:harmonic:metadata_field:created_at",
        "descending": true,
        "priority": 0
      }
    ]
  }
}
```

**For a record type** — order the whole company dataset by headcount, largest first:

```json
{
  "input": {
    "recordTypeUrn": "urn:harmonic:record_type:company",
    "name": "All companies by headcount",
    "sorts": [
      {
        "sortOrderUrn": "urn:harmonic:record_attribute:company:external_headcount",
        "descending": true,
        "priority": 0
      }
    ]
  }
}
```

Input notes:

- `columns` — each takes `attributeUrn` and an optional `columnWidth`. The array order is the display order; read responses return each column with a read-only `displayOrder` index reflecting its position.
- `sorts` — each takes a `sortOrderUrn` and a required `priority` (0-based); `descending` defaults to `false`.
- `filter` — an `AttributeFilterInput`; wrap the conditions in a single `and` / `or` list (required for saved views, and it makes the intent clear).

#### Update a view, or make it the team default

Only provided fields change. Providing `columns` or `sorts` **replaces** the whole set. Setting `isDefault: true` makes this the view the list or record type opens with — and unsets any previous default.

```graphql
mutation UpdateNamedView($input: UpdateNamedViewInput!) {
  updateNamedView(input: $input) {
    namedView {
      urn
      name
      isDefault
      updatedAt
      columns {
        attributeUrn
        displayOrder
      }
      sorts {
        sortOrderUrn
        descending
        priority
      }
    }
  }
}
```

```json variables
{
  "input": {
    "urn": "urn:harmonic:named_view:YOUR_VIEW_UUID",
    "name": "Renamed view",
    "columns": [
      {
        "attributeUrn": "urn:harmonic:record_attribute:company:external_headcount",
        "columnWidth": 250
      }
    ],
    "sorts": [
      {
        "sortOrderUrn": "urn:harmonic:record_attribute:company:external_headcount",
        "descending": true,
        "priority": 0
      }
    ]
  }
}
```

For the full structure of a saved view and how it relates to records and lists, see [Views](/docs/api-reference/workspace/core-concepts#named-views).

## Reference

Everything in the Workspace API on one page. Use this to look things up; the numbered guides ([Getting started](/docs/api-reference/workspace/getting-started), [Core concepts](/docs/api-reference/workspace/core-concepts), [Common workflows](/docs/api-reference/workspace/common-workflows)) walk through the same material with full examples.

### At a glance

|             |                                                                                                                                   |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Endpoint    | `POST https://api.harmonic.ai/graphql/v2`                                                                                         |
| Protocol    | GraphQL (single endpoint, introspection enabled)                                                                                  |
| Auth        | `apikey: YOUR_API_KEY` header                                                                                                     |
| Scope       | One **workspace** per team, resolved from your API key                                                                            |
| Access      | Team-shared lists and saved searches only — private resources are not reachable                                                   |
| Errors      | Execution errors: HTTP `200` + `errors` array, branch on `extensions.code`; pre-execution: `422` (validation), `401`/`403` (auth) |
| Pagination  | Relay-style cursors everywhere: `first`/`after`, `edges { node }`, `pageInfo`, `totalCount`                                       |
| File upload | `createRecordAttachment` only — multipart request per the GraphQL multipart spec                                                  |

**GraphQL Schema Introspection:**

```bash
curl -X POST 'https://api.harmonic.ai/graphql/v2' \
  -H "apikey: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'

# This should give you a response like:
# {"data":{"__schema":{"types":[{"name":"Acquisition"},{"name":"AddCompaniesToWatchlistWithCanonicalsPayload"} ...
```

### Object model

```
Workspace (one per team, from your API key)
├── Record types (company / person / investor)
│   ├── Record attributes ──── values live on records, follow them everywhere
│   ├── Records ────────────── one entity each; holds teamNote + attachments
│   └── Named views ────────── saved filter/sort/columns over all records of the type
└── Lists (each tracks one record type)
    ├── List attributes ────── values live on entries, scoped to this list
    ├── Entries ────────────── one record's membership in this list
    └── Named views ────────── saved filter/sort/columns over this list
```

The two-scope rule in one line: **record attributes** travel with the record into every list; **list attributes** exist only on one list's entries. Details in [Core concepts → Attributes](/docs/api-reference/workspace/core-concepts#attributes).

### URN reference

| Object                     | URN shape                                                                          |
| -------------------------- | ---------------------------------------------------------------------------------- |
| Workspace                  | `urn:harmonic:workspace:{uuid}`                                                    |
| Record type (built-in)     | `urn:harmonic:record_type:company` · `:person` · `:investor` (stable, hardcodable) |
| Record                     | `urn:harmonic:record:{uuid}`                                                       |
| Record attribute           | `urn:harmonic:record_attribute:{record_type}:{col}`                                |
| List                       | `urn:harmonic:list:{uuid}`                                                         |
| List entry                 | `urn:harmonic:list_entry:{uuid}`                                                   |
| List attribute             | `urn:harmonic:list_attribute:{list_uuid}:{col}`                                    |
| Named view                 | `urn:harmonic:named_view:{uuid}`                                                   |
| Import task                | `urn:harmonic:import_task:{uuid}`                                                  |
| Attachment                 | `urn:harmonic:user_uploaded_content:{uuid}`                                        |
| Metadata field (for sorts) | `urn:harmonic:metadata_field:created_at` · `:id`                                   |
| Harmonic entity            | `urn:harmonic:company:{id}` · `urn:harmonic:person:{id}`                           |

`harmonicUrn` on a record links back to the Harmonic entity it enriches from.

### Queries

| Query        | Key arguments                          | Use it for                                                                                                       |
| ------------ | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `workspace`  | — (resolves from API key)              | Your account: `urn`, `name`, `customerUrn`, built-in record types, `lists`, `users`, Harmonic attribute catalogs |
| `recordType` | `urn`                                  | A type's `attributes`, `records`, `namedViews`, `storageLimits`                                                  |
| `record`     | `urn`, `recordTypeUrn` (both required) | One record: fields, `attributeValues(include:)`, `teamNote`, `attachments`, `updateEvents(since:)`               |
| `records`    | `urns`, `recordTypeUrn`                | Batch-fetch records by URN                                                                                       |
| `list`       | `urn`                                  | A list's metadata, `entries`, `namedViews`, `importTasks`                                                        |
| `listEntry`  | `urn`, `listUrn`                       | One entry directly                                                                                               |
| `namedView`  | `urn`                                  | A saved view's `filter`, `sorts`, `columns`, `isDefault`                                                         |
| `importTask` | `urn`                                  | Import job status, progress, `importEntries(status:)`                                                            |

**Connections that accept `filter` + `orderBy`:** `list.entries`, `recordType.records`. Keep both stable across a paging run. See [Pagination](/docs/api-reference/workspace/getting-started#pagination).

**Discover enrichment fields:** `workspace.companyHarmonicAttributes` / `personHarmonicAttributes` / `investorHarmonicAttributes` — each row gives the `recordAttributeUrn` to filter, sort, or `include` against. See [Enrich what you've imported](/docs/api-reference/workspace/common-workflows#enrich-what-youve-imported).

### Mutations

#### Lists

| Mutation     | Input essentials        | Notes                                 |
| ------------ | ----------------------- | ------------------------------------- |
| `createList` | `recordTypeUrn`, `name` | Saved to your workspace automatically |
| `updateList` | `urn`, changed fields   |                                       |
| `deleteList` | `urn`                   |                                       |

#### List entries — single

| Mutation          | Input essentials                                                              | Notes                                                                                       |
| ----------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `createListEntry` | `selection` (`listUrn` + `recordUrn` **or** `harmonicUrn`), `attributeValues` | Creates the record if the `harmonicUrn` isn't in your workspace yet (`recordCreated: true`) |
| `updateListEntry` | `urn` **or** `selection`, `attributeValues`                                   | Only passed values change                                                                   |
| `deleteListEntry` | `urn` **or** `selection`                                                      | Removes from the list; the record survives                                                  |

#### List entries — bulk

All three take a `targetListUrn` (except `updateRecords`) plus a **selection**:

| Selection field           | Targets                                                                   |
| ------------------------- | ------------------------------------------------------------------------- |
| `entryUrns`               | Specific entries by URN                                                   |
| `recordUrns`              | Specific records by URN                                                   |
| `harmonicUrns`            | Specific Harmonic entities                                                |
| `fromListSelection`       | Entries in a source list matching a `filter` (+ optional `sort`, `limit`) |
| `fromRecordTypeSelection` | Records of a type matching a `filter`                                     |

| Mutation            | Does                                                                    | Returns                                                             |
| ------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `createListEntries` | Copies a selection into a list; skips records already there             | `createdCount`, `skippedCount`, `notFoundCount`, `createdEntryUrns` |
| `updateListEntries` | Sets attribute values on every selected entry                           | `success`, `updatedCount`                                           |
| `deleteListEntries` | Removes selected entries from the list                                  | `deletedCount`                                                      |
| `updateRecords`     | Sets **record-level** values across a selection (takes `recordTypeUrn`) | `success`, `updatedCount`                                           |

Filter-based selections cap at **10,000 items** per request. Full walkthrough: [Update many companies at once](/docs/api-reference/workspace/common-workflows#update-many-companies-at-once).

#### Records

| Mutation         | Input essentials                                                         | Notes                                                    |
| ---------------- | ------------------------------------------------------------------------ | -------------------------------------------------------- |
| `updateRecord`   | `urn`, `attributeValues`, optional `teamNote`                            | Only passed fields change                                |
| `updateTeamNote` | `note`, `selection` (`recordTypeUrn` + `recordUrn` **or** `harmonicUrn`) | Resolves/creates the record for you; empty string clears |

There is **no standalone create-record mutation** — records enter via `createImport` or `createListEntry` with a `harmonicUrn`.

#### Attributes (fields)

| Mutation                                          | Scope       | Input essentials                                           |
| ------------------------------------------------- | ----------- | ---------------------------------------------------------- |
| `createRecordAttribute`                           | Record type | `recordTypeUrn`, `fieldName`, `fieldType`, `fieldMetadata` |
| `updateRecordAttribute` / `deleteRecordAttribute` | Record type | `urn`                                                      |
| `createListAttribute`                             | One list    | `listUrn`, `fieldName`, `fieldType`, `fieldMetadata`       |
| `updateListAttribute` / `deleteListAttribute`     | One list    | `urn`                                                      |

Select/status options: you set `label` + `color` (integer `0`–`16`, or `"inverse"`); Harmonic returns a stable option **key** (UUID). Set and filter by the key, never the label.

#### Named views

| Mutation          | Input essentials                                                                      | Notes                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `createNamedView` | exactly one of `listUrn` / `recordTypeUrn`, plus `name`, `filter`, `columns`, `sorts` |                                                                                            |
| `updateNamedView` | `urn`, changed fields                                                                 | `columns`/`sorts` **replace** the whole set; `isDefault: true` unsets the previous default |
| `deleteNamedView` | `urn`                                                                                 |                                                                                            |

#### Imports

| Mutation       | Input essentials                                                                         | Notes                                                                            |
| -------------- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `createImport` | `sourceSystem`, `rows` (max 1,000), one of `listURN` / `recordTypeURN`, optional `mode`. | Async — poll `importTask`. `mode: UPSERT` updates matches instead of duplicating |

To set attribute values for each entry in your import payload, also include attributeValues which represents a list of values to append. The values will be rejected by default if an existing row already exists. Switch to `UPSERT` import mode to overwrite values for matching entities.

Each row: `rowIndex` (required) + `harmonicUrn` **or** `canonicalInput`, plus optional `attributeValues` and `externalRowID`. Canonicals: companies match by `websiteURL`, `linkedinURL`, and other social/data URLs; people by `primaryEmail`, `linkedinURL`. See [Import and enrich data](/docs/api-reference/workspace/common-workflows#import-and-enrich-data).

#### Attachments

| Mutation                 | Input essentials               | Notes                              |
| ------------------------ | ------------------------------ | ---------------------------------- |
| `createRecordAttachment` | `record`, `file` (multipart)   | One file per request, up to 500 MB |
| `updateRecordAttachment` | `attachment`, `record`, `name` | Rename                             |
| `deleteRecordAttachment` | `attachment`, `record`         | Returns `deletedUrn`               |

Read them via `record.attachments`; `contentUrl` is a signed, short-lived download URL — fetch it when you're ready to download. See [Add attachments](/docs/api-reference/workspace/common-workflows#add-attachments).

### Field types

Set exactly **one** value field per attribute in any `attributeValues` input:

| Field type                                   | Write with     | Notes                                            |
| -------------------------------------------- | -------------- | ------------------------------------------------ |
| `STRING`                                     | `stringValue`  | Max 500 characters                               |
| `URL` / `EMAIL`                              | `stringValue`  |                                                  |
| `NUMBER`                                     | `numberValue`  | Metadata: `min`, `max`, `precision`              |
| `CURRENCY`                                   | `numberValue`  | Metadata requires `currencyCode` (ISO 4217)      |
| `PERCENT`                                    | `numberValue`  |                                                  |
| `TRACTION`                                   | `numberValue`  | Metadata: `metricType`, `unit`                   |
| `DATE`                                       | `dateValue`    | RFC 3339 timestamp                               |
| `BOOLEAN`                                    | `booleanValue` |                                                  |
| `SINGLE_SELECT` / `STATUS`                   | `stringValue`  | Value is an option **key** (UUID), not the label |
| `MULTI_SELECT`                               | `arrayValue`   | Option keys                                      |
| `USER_REFERENCE` / `OWNER_REFERENCE`         | `arrayValue`   | User URNs                                        |
| `RECORD_REFERENCE`                           | `arrayValue`   | Record URNs                                      |
| `STRING_ARRAY` / `URL_ARRAY` / `EMAIL_ARRAY` | `arrayValue`   |                                                  |
| `RELEVANCE`                                  | —              | Harmonic relevance score, read-only              |
| `LIST_MEMBERSHIP`                            | —              | System field                                     |

**Reading values back:** values are opt-in — pass attribute URNs via `include` to `attributeValues`, then select the typed member (`StringValue.stringValue`, `NumberValue.numberValue`, `DateValue.dateValue`, `BooleanValue.booleanValue`; array-shaped values are paginated connections: `arrayConnectionValue`, `recordConnectionValue`, `userConnectionValue`; single user via `userValue`). `attributeValueMap(include:)` returns an untyped JSON object keyed by display name — fine for debugging, use `attributeValues` in production. See [Core concepts → Attributes](/docs/api-reference/workspace/core-concepts#attributes).

### Filtering

Shape of every leaf condition:

```
filter: {
  <conditionKey>: {
    attributeURN: "<full attribute URN>"   # capital URN
    <operator>: <value>
  }
}
```

Conditions at the same level combine with **AND**; nest with `and` / `or` arrays of `AttributeFilterInput`.

| Condition key                                                                                         | Field types              | Operators (all also support `isNull`)                                                                                                        |
| ----------------------------------------------------------------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`, `text`, `email`                                                                               | Strings                  | `equals`/`notEquals`, `contains`/`notContains`, `startsWith`, `endsWith`, `in`/`notIn`, lexical comparisons                                  |
| `number`, `currency`, `percent`, `traction`, `relevance`                                              | Numerics                 | `equals`/`notEquals`, `lessThan(OrEqual)`, `greaterThan(OrEqual)`, `in`/`notIn`                                                              |
| `date`                                                                                                | `DATE`                   | `equals`, `before(OrEqual)`, `after(OrEqual)` — operands: `preset`, `time`, or `offsetDays`                                                  |
| `checkbox`                                                                                            | `BOOLEAN`                | `equals`                                                                                                                                     |
| `singleSelect`, `status`                                                                              | Selects                  | `equals`/`notEquals`, `in`/`notIn` — match on option **key**                                                                                 |
| `multiSelect`, `record`, `user`, `list`, `harmonicReference`, `stringArray`, `urlArray`, `emailArray` | Multi-value & references | `containsAnyOf`, `containsAllOf`, `excludesAnyOf`, `excludesAllOf`, `equals`/`notEquals` (arrays also: `contains`/`notContains` on elements) |
| `owner`                                                                                               | `OWNER_REFERENCE`        | `equals`/`notEquals`, `in`/`notIn`                                                                                                           |
| `harmonicUrn`                                                                                         | Harmonic entity match    | `in`/`notIn`                                                                                                                                 |

Two classic mistakes: writing `attributeUrn` instead of `attributeURN`, and using the literal field type as the condition key (a `STRING` field filters under `text`; the built-in record name under `name`). Full guide: [Views → Saved filters](/docs/api-reference/workspace/core-concepts#saved-filters).

### Sorting

`orderBy` is an array of `SortInput` — earlier entries take precedence. Each entry has **one** of:

- `metadataField`: `ID`, `NAME`, `CREATED_AT`, `UPDATED_AT`, `CREATED_BY`, `SEARCH_RANK`
- `sortOrderUrn`: an attribute URN or a metadata-field URN (`urn:harmonic:metadata_field:created_at`)

plus optional `descending` (default `false`). Saved views store sorts as `sortOrderUrn` and additionally require a 0-based `priority` per sort.

### Exports

The Synapse GraphQL service exposes CSV export as **REST endpoints** (not GraphQL mutations) so responses can be streamed as chunked `text/csv` rather than buffered into a GraphQL payload.

| Endpoint                               | Input essentials                                       | Notes                                                                                                   |
| -------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `POST /api/export-service`             | `listUrn`, `columns`, optional `filter`, `sorts`       | Ad-hoc list export. Body is `CreateNamedViewInput` (name/description ignored).                          |
| `POST /api/export-service/view`        | `viewUrn`                                              | Export from a saved named view. Dispatches to list vs. record-type by `:record_named_view:` in the URN. |
| `POST /api/export-service/record-type` | `recordTypeUrn`, `columns`, optional `filter`, `sorts` | Ad-hoc record-type export. Same input shape as `/api/export-service`, keyed by record type.             |

- Responses are `Content-type: text/csv`
- `maxColumnsLimit = 100` columns per request; over that returns HTTP 400 `Too many columns requested`
- 5-minute hard timeout. bounds the entire request

These endpoints are REST, so they aren't covered by GraphQL introspection. Grab the OpenAPI spec for them — handy for LLM agents:

```yaml
openapi: 3.0.3
info:
  title: Synapse Export API
  description: |
    Streaming CSV export endpoints hosted by the Synapse GraphQL service. These
    are REST endpoints (not GraphQL) because CSV needs to stream row-by-row.

    All endpoints:
      - Require the same authentication as the GraphQL API.
        The caller's workspace must own the referenced list
        / record type / view.
      - Accept `POST` only.
      - Stream `text/csv` on success (`Transfer-Encoding: chunked`,
        `Content-Disposition: attachment`).
      - Return a JSON error payload with HTTP 400 when the export exceeds the
        row limit.
      - Are bounded by a 5-minute stream timeout.
  version: "1.0.0"

servers:
  - url: https://api.harmonic.ai/graphql/v2
    description: PROD (paths below are relative to this base, e.g. POST https://api.harmonic.ai/graphql/v2/api/export-service)

paths:
  /api/export-service:
    post:
      summary: Export a list to CSV
      description: |
        Streams a CSV export of a list. The request body reuses the
        `CreateNamedViewInput` shape from the GraphQL schema: only `listUrn`,
        `columns`, `filter`, and `sorts` are honoured. `name`, `description`,
        `layout`, `groupByAttributeUrn`, `cardProperties`, `kanbanColumns`,
        and `category` are ignored.
      operationId: exportList
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ListExportRequest"
      responses:
        "200":
          $ref: "#/components/responses/CsvStream"
        "400":
          $ref: "#/components/responses/BadRequestOrRowLimit"
        "401": { $ref: "#/components/responses/Unauthorized" }
        "403": { $ref: "#/components/responses/Forbidden" }
        "405": { $ref: "#/components/responses/MethodNotAllowed" }
        "500": { $ref: "#/components/responses/ServerError" }

  /api/export-service/record-type:
    post:
      summary: Export a record type to CSV
      description: |
        Streams a CSV export scoped to a record type (workspace-level records,
        e.g. all companies or all people). Body reuses `CreateNamedViewInput`;
        only `recordTypeUrn`, `columns`, `filter`, and `sorts` are honoured.
      operationId: exportRecordType
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/RecordTypeExportRequest"
      responses:
        "200":
          $ref: "#/components/responses/CsvStream"
        "400":
          $ref: "#/components/responses/BadRequestOrRowLimit"
        "401": { $ref: "#/components/responses/Unauthorized" }
        "403": { $ref: "#/components/responses/Forbidden" }
        "405": { $ref: "#/components/responses/MethodNotAllowed" }
        "500": { $ref: "#/components/responses/ServerError" }

  /api/export-service/view:
    post:
      summary: Export a named view to CSV
      description: |
        Streams a CSV export driven by a saved named view. The handler
        dispatches on the URN kind: URNs containing `:record_named_view:` are
        treated as record-type views; all others are treated as list views.
        Columns / filters / sorts are loaded from the stored view; the caller
        supplies only the view URN.
      operationId: exportView
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ExportViewRequest"
      responses:
        "200":
          $ref: "#/components/responses/CsvStream"
        "400":
          $ref: "#/components/responses/BadRequestOrRowLimit"
        "401": { $ref: "#/components/responses/Unauthorized" }
        "403": { $ref: "#/components/responses/Forbidden" }
        "405": { $ref: "#/components/responses/MethodNotAllowed" }
        "500": { $ref: "#/components/responses/ServerError" }

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Authorization
      description: Bearer token API key

  responses:
    CsvStream:
      description: Streaming CSV response.
      headers:
        Content-Type:
          schema: { type: string, example: "text/csv; charset=utf-8" }
        Content-Disposition:
          schema: { type: string, example: "attachment" }
        Transfer-Encoding:
          schema: { type: string, example: "chunked" }
        X-Content-Type-Options:
          schema: { type: string, example: "nosniff" }
      content:
        text/csv:
          schema:
            type: string
            format: binary

    BadRequestOrRowLimit:
      description: |
        Malformed request (plain text) or row-limit exceeded (structured JSON).
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/RowLimitError"
        text/plain:
          schema:
            type: string
            example: "listUrn is required"

    Unauthorized:
      description: Missing or invalid auth.
      content:
        text/plain: { schema: { type: string } }

    Forbidden:
      description: Resource does not belong to the authenticated workspace.
      content:
        text/plain: { schema: { type: string } }

    MethodNotAllowed:
      description: Only POST is accepted.
      content:
        text/plain: { schema: { type: string, example: "Method not allowed" } }

    ServerError:
      description: Unhandled server-side failure.
      content:
        text/plain: { schema: { type: string, example: "Export failed" } }

  schemas:
    ListExportRequest:
      type: object
      required: [listUrn]
      properties:
        listUrn:
          type: string
          description: URN of the list to export.
          example: "urn:harmonic:list:018f..."
        columns:
          type: array
          maxItems: 100
          items: { $ref: "#/components/schemas/NamedViewColumnInput" }
        filter:
          $ref: "#/components/schemas/AttributeFilterInput"
        sorts:
          type: array
          items: { $ref: "#/components/schemas/NamedViewSortInput" }

    RecordTypeExportRequest:
      type: object
      required: [recordTypeUrn]
      properties:
        recordTypeUrn:
          type: string
          description: URN of the record type to export.
          example: "urn:harmonic:record_type:company"
        columns:
          type: array
          maxItems: 100
          items: { $ref: "#/components/schemas/NamedViewColumnInput" }
        filter:
          $ref: "#/components/schemas/AttributeFilterInput"
        sorts:
          type: array
          items: { $ref: "#/components/schemas/NamedViewSortInput" }

    ExportViewRequest:
      type: object
      required: [viewUrn]
      properties:
        viewUrn:
          type: string
          description: |
            Named-view URN. If it contains `:record_named_view:` the handler
            uses the record-type export service; otherwise the list export
            service.
          example: "urn:harmonic:named_view:018f..."

    NamedViewColumnInput:
      type: object
      required: [attributeUrn]
      properties:
        attributeUrn:
          type: string
          example: "urn:harmonic:record_attribute:018f..."

    NamedViewSortInput:
      type: object
      required: [sortOrderUrn]
      properties:
        sortOrderUrn:
          type: string
          description: Attribute or metadata-field URN to sort by.
        descending:
          type: boolean
          default: false

    AttributeFilterInput:
      type: object
      description: |
        GraphQL `AttributeFilterInput` — mirrors the shape used in
        `createNamedView` / `updateNamedView`. See the GraphQL schema for the
        full recursive definition (attribute clauses, and/or groups, etc.).
      additionalProperties: true

    RowLimitError:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              enum: [EXPORT_ROW_LIMIT_EXCEEDED]
            message:
              type: string
              example: "Export too large. Please apply filters to reduce the number of rows."
            max_rows:
              type: integer
            total_rows:
              type: integer

security:
  - ApiKeyAuth: []
```

### Limits

| Limit                          | Value                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Query depth                    | 15 levels of nesting                                                                                                      |
| Page size (`first`)            | 100 max                                                                                                                   |
| Import rows per `createImport` | 1,000                                                                                                                     |
| Filter-based bulk selection    | 10,000 items per request                                                                                                  |
| Records per record type        | 1,000,000                                                                                                                 |
| Custom fields                  | 30 per kind, per record type — and separately per list (related types share a kind: text-like, numeric-like, multi-value) |
| Text values                    | 500 characters                                                                                                            |
| Attachment upload              | 500 MB, one file per request                                                                                              |

The configured limits are exposed on `recordType.storageLimits`.

### Recipes

One-line pointers into the workflow guides:

| I want to…                                     | Use                                                  | Guide                                                                                                                 |
| ---------------------------------------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Set up a pipeline with stages                  | `createList` + `createListAttribute` (`STATUS`)      | [Manage a sourcing workflow](/docs/api-reference/workspace/common-workflows#manage-a-sourcing-workflow)               |
| Add many companies (by website/LinkedIn)       | `createImport` with `listURN`                        | [Import and enrich data](/docs/api-reference/workspace/common-workflows#import-and-enrich-data)                       |
| Promote top prospects to another list          | `createListEntries` with filtered + sorted selection | [Promote top prospects](/docs/api-reference/workspace/common-workflows#promote-top-prospects-to-another-list)         |
| Add my own fields to every company             | `createRecordAttribute`                              | [Add your own context to companies](/docs/api-reference/workspace/common-workflows#add-your-own-context-to-companies) |
| Write a shared note against a Harmonic company | `updateTeamNote` with `harmonicUrn` selection        | [Add notes](/docs/api-reference/workspace/common-workflows#add-notes)                                                 |
| Attach a pitch deck to a company               | `createRecordAttachment` (multipart)                 | [Add attachments](/docs/api-reference/workspace/common-workflows#add-attachments)                                     |
| Sync a CRM without creating duplicates         | `createImport` with `mode: UPSERT`                   | [Keep imported data current](/docs/api-reference/workspace/common-workflows#keep-imported-data-current)               |
| Watch for job changes / stealth emergence      | `record.updateEvents(since:)`                        | [Keep imported data current](/docs/api-reference/workspace/common-workflows#keep-imported-data-current)               |
| Migrate off legacy watchlists                  | Migration manifest + agent prompt                    | [Migrating to V2](/docs/api-reference/workspace/migration)                                                            |

## Migrating to V2

Harmonic's API is moving to V2. All new features (starting with the Workspace API) will be built exclusively on V2.

### What's changing

- **Legacy watchlist and custom-field APIs sunset on November 5th, 2026.** If you use these today, you must migrate to the Workspace API on V2. The rest of this page walks you through that migration; for the full list of what's going away, see [Deprecated endpoints](#deprecated-endpoints).
- **All other V1 APIs (enrichment, company/people data) are fully forward-compatible on V2.** Your existing queries work as-is on the /graphql/v2 endpoint. We highly encourage migrating to gain access to Workspace and future features, but there is no forced sunset for these endpoints.

Beyond the required migration, the Workspace API also gives you a simpler data model and more powerful querying capabilities:

- **One model, less code.** Company and people watchlists are now a single `list` type, distinguished by record type. The parallel company-vs-people code paths collapse into one.
- **Fetch exactly what you need.** GraphQL lets you request just the fields and attribute values you want, in one round-trip — instead of over-fetching fixed REST payloads and discarding most of them.
- **Built for tools and AI agents.** A single, introspectable endpoint (`/graphql/v2`) with a typed, self-describing schema. Coding agents (Claude Code, Cursor) can explore it and validate every call against the live schema before sending it — which is exactly how the migration prompt in this package works.
- **Lists that drive action.** Server-side filtering and sorting, plus saved named views your integration can poll to trigger downstream work — automations, alerts, CRM syncs. Cursor pagination keeps it fast as lists grow.
- **Bulk by default.** `createImport` resolves entities by website / LinkedIn / email and creates any missing records in a single job — no manual pre-resolution, no per-row round-trips.

### **What to expect during migration**

Migrating your code is only half the story — moving your account from the legacy to v2 is a coordinated cutover that we will run together with you. You'll hear from us well before you need to migrate, and nothing changes for your account until you've scheduled a migration with us.

#### **1. Before migration: both APIs are live**

Until your migration runs, your existing V1 integration keeps working exactly as it does today. At the same time, you have access to the V2 API, which points at your new **workspace** — pre-loaded with a copy of your data as of the date noted in your migration notice email.

Treat this workspace as a **playground**: it's a frozen snapshot, so changes you make in your legacy workspace after that date will *not* appear in it (and changes you make in the playground don't affect your real data). It exists so you can do the migration work safely:

- Rewrite your integration against V2 (see Migrate with an agent).
- Run your migrated code against the playground and verify it behaves the same as your V1 integration — same lists, same fields, same shapes.
- Decide your cutover strategy. This depends on how your integration is deployed: a recurring job might get a new V2 version you leave switched off until migration day, while an internal portal might get a config flag that routes traffic to V2 when flipped. Either way, aim to arrive at migration day with a tested V2 path that's ready to turn on.

You can check which state your account is in at any time via the `workspace_migration_phase` field on the migration manifest.

#### **2. Migration day: a scheduled cutover with brief downtime**

When your V2 integration is tested and ready, email us at support@harmonic.ai, and we'll coordinate a date and time for your migration. While the migration runs, expect **downtime**: Harmonic Console and the APIs will be unavailable for your account as we move your workspace from the old world to the new one.

#### **3. After migration: V2 is live, legacy watchlist APIs stop working**

Once the migration completes, your account is fully migrated:

- The V2 API now operates on your **real, live workspace data** — the playground state is replaced by your up-to-date workspace.
- The **legacy watchlist and custom-field APIs stop working for your account.** (Non-deprecated V1 endpoints — enrichment, entity fetch, search — are unaffected.)
- This is the moment to flip your cutover switch: turn on your V2 jobs, redeploy with the V2 flag enabled, or however you chose to route your workload to V2.

### The model, side by side

The short version: **a watchlist becomes a list, a custom field becomes an attribute, a field value becomes an attribute value, and a watchlist member becomes a list entry.** Company and people watchlists collapse into one model — a list distinguished by its **record type** — so the company-vs-people branching goes away. Most things carry over cleanly; a few have no v2 home and stay where they are. This page tells you which is which, and the order to do it in.

| You have today (legacy)        | It becomes (Workspace v2)                            | URN                                                 |
| ------------------------------ | ---------------------------------------------------- | --------------------------------------------------- |
| Company / People **watchlist** | **List** (one model; record type distinguishes them) | `urn:harmonic:list:{uuid}`                          |
| Watchlist **member**           | **List entry**                                       | `urn:harmonic:list_entry:{uuid}`                    |
| Watchlist **custom field**     | **List attribute** (scoped to one list)              | `urn:harmonic:list_attribute:{list_uuid}:{col}`     |
| Team **global custom field**   | **Record attribute** (follows the record everywhere) | `urn:harmonic:record_attribute:{record_type}:{col}` |
| Custom **field value**         | **Attribute value** (on the entry, or on the record) | —                                                   |
| Saved **named view**           | **Named view**                                       | `urn:harmonic:named_view:{uuid}`                    |

### Migration metadata endpoint

This endpoint is now available at `https://api.harmonic.ai/migration/manifest`. It can be used to fetch a mapping of:

- Legacy watchlists URNs to new list URNs — each entry carries a `migration_strategy` indicating whether it migrates to a v2 list (`workspace_list`, the default) or to the records endpoint for its record type (`records_endpoint`, for special lists like Team Network that have no v2 list equivalent).
- Legacy watchlist custom fields URNs to new custom attribute URNS
- Legacy global custom fields URNs to new custom record attribute URNs
- NOTE: the `workspace_migration_phase` will report the phase your account is currently in. Prior to Harmonic migrating your data, it will show `DISABLED`. After your account data is migrated, it will show `MIGRATED`. During the maintainence window, the endpoint will not be available.

**Sample request**

```
curl --location 'https://api.harmonic.ai/migration/manifest' \
--header 'apikey: APIKEY'
```

**Sample response**

```
{
    "workspace_migration_phase": "DISABLED",
    "workspace_urn": "urn:harmonic:workspace:09f2123f-f9db-5ed6-999e-821d9a56dca3",
    "list_mappings": [
        {
            "legacy_watchlist_urn": "urn:harmonic:company_watchlist:c6795d86-b4f1-4d75-aff1-5798718d286a",
            "workspace_list_urn": "urn:harmonic:list:c6795d86-b4f1-4d75-aff1-5798718d286a",
            "workspace_project_urn": "urn:harmonic:project:e861bf4f-4b49-5369-b0ea-07c69f1624cb",
            "record_type": "company",
            "migration_strategy": "workspace_list"
        },
        {
            "legacy_watchlist_urn": "urn:harmonic:people_watchlist:aaaaaaaa-0000-0000-0000-000000000007",
            "workspace_list_urn": "urn:harmonic:list:aaaaaaaa-0000-0000-0000-000000000007",
            "workspace_project_urn": null,
            "record_type": "person",
            "migration_strategy": "records_endpoint"
        }
    ],
    "custom_field_mappings": [
        {
            "legacy_custom_field_urn": "urn:harmonic:company_list_custom_field:11525",
            "legacy_type": "DATE",
            "workspace_attribute_urn": "urn:harmonic:list_attribute:7564fa22-cf44-462f-92f2-b5168569ea6a:DATE006",
            "workspace_type": "DATE",
            "has_known_mapping": true
        }
    ],
    "global_custom_field_mappings": [
        {
            "legacy_custom_field_urn": "urn:harmonic:company_list_custom_field:11493",
            "legacy_type": "CHECKBOX",
            "workspace_attribute_urn": "urn:harmonic:record_attribute:company:BOOL001",
            "workspace_type": "BOOLEAN",
            "has_known_mapping": true
        }
    ],
    "company_field_mappings": [
        {
            "legacy_field_urn": "urn:harmonic:company_field:company_accelerator_tags",
            "workspace_attribute_urn": "urn:harmonic:record_attribute:company:accelerators",
            "workspace_type": "MULTI_SELECT"
        }
    ],
    "person_field_mappings": [
        {
            "legacy_field_urn": "urn:harmonic:person_field:person_customers_connections",
            "workspace_attribute_urn": "urn:harmonic:record_attribute:person:team_network",
            "workspace_type": "USER_REFERENCE"
        }
     ],
    "company_graphql_field_mappings": [
	    {
		    "graphql_path": "companyType",
		    "workspace_attribute_urn": "urn:harmonic:record_attribute:company:type"
	    },
	    {
		    "graphql_path": "contact.primaryEmail",
		    "workspace_attribute_urn": "urn:harmonic:record_attribute:company:primary_contact_email"
	    },
	    /** Additional items omitted for brevity, full response includes the full possible catalog */
	    {
	      "graphql_path": "contact.primaryEmailPersonId",
	      "workspace_attribute_urn": null
	    }
    ],
    "person_graphql_field_mappings": [
	    {
		    "graphql_path": "contact.emails",
		    "workspace_attribute_urn": "urn:harmonic:record_attribute:person:contact_emails"
	    },
	    {
		    "graphql_path": "education.school.name",
		    "workspace_attribute_urn": "urn:harmonic:record_attribute:person:education_school_names"
	    },
	    /** Additional items omitted for brevity, full response includes the full possible catalog */
	    {
	      "graphql_path": "education.school.linkedinUrl",
	      "workspace_attribute_urn": null
	    }
    ]
}
```

#### Migrating Field resolutions

A key change between v1 Graphql APIs and the new Workspace APIs is the transition from embedded resolver fields for `Company` and `People` graph entities into record attribute urns that are supplied as parameters to your query.

The migration manifest exposes a mapping between the most commonly used paths in the graphql resolver tree and their equivalent record attribute types. However, for certain specific paths, there is no currently exposed symmetrical record attribute. In this case we recommend the following:

1. Check if that resolver path and field is actually used by the application. If it's not actually used and isn't relevant for the workflow, it's best to just drop it from the list of requested attributes.
2. If there's a required dependency on the field, see if there is a mapping between the resolver field path. If a mapping to a non-null record attribute URN exists, use this record attribute as a replacement.
3. If there's no available mapping, a workaround is to use a 2-phase approach to resolve the necessary field values. First, fetch the harmonic entities from your list entries using the workspace APIs. Then, collecting the URNs you want to fetch, use the entity Fetch APIs to fetch the company or person entity and resolver fields you need.

### Migrate with an agent

Copy everything in the block below into your coding agent.

````
# Harmonic v1 -> v2 (Workspace API) Migration Prompt

You are migrating an application from Harmonic's **v1 APIs** (REST `api.harmonic.ai/...` plus GraphQL `api.harmonic.ai/graphql`) to the **v2 GraphQL API** at `https://api.harmonic.ai/graphql/v2`. Use this document as the source of truth. For each v1 call in the codebase, find its use case below, replace it with the v2 equivalent while preserving business logic, convert page-number loops to cursor loops, and keep auth unchanged. If a use case is marked "no v2 path", leave it on v1 and add a `TODO(harmonic-migration)` note.

## Migration Logistics

Migration of the application from V1 to V2 happens within the following context/workflow:

1. **Pre-migration playground**: Harmonic has created a snapshot of your data as of the date noted in your migration notice email that is accessible from V2 APIs and isolated from your authoritative list data. Consider this data a "playground." In this stage, you can make reads and writes with the V2 APIs and it will only change this copy of data. Any changes will not be reflected or saved after this stage is over.
2. **Code change to support V2**: (Now) You will migrate the application built on top of Harmonic APIs to use the V2 API surface where applicable. You are making the change but NOT deploying it yet. You should test that the application works as expected on top of the V2 APIs.
3. **Harmonic data migration**: When your application is ready to support V2 APIs, Harmonic will trigger a 1-time data migration. This will clear any data from the first stage above and replace it with the current state of list data in your account. During this migration, there will be downtime, and your application should not make requests to Harmonic as it will fail.
4. **Deploy against V2**: Once the migration is completed, the scheduled downtime will be over. The application can be resumed and deployed working against the V2 APIs. The V1 workspace APIs will no longer work for you and will return an error.

For the application you are migrating you **must clarify with the user on how they want to handle downtime**. Determine the impact with the user on the implication of downtime from Harmonic during the data migration stage. Given the impact, create a plan for how to coordinate with the migration stages. This may involve creating a mechanism for the user to deploy the application pointing V2 APIs instead of V1. Or it could involve creating an entirely new copy of the application to deploy during stage 4. **You must confirm this choice with the user and have them direct you to update the API calls in place or create new copies and code paths and leave existing code paths alone**.

## Prime directives (read before writing any code)

These four goals rank above everything else. When a mapping below is ambiguous, resolve it in favor of these:

1. **Minimal, focused diff.** Change only what the v1-to-v2 API incompatibility forces you to change. Do not add speculative abstraction, do not write defensive parsers for shapes you can verify from the schema, and do not request fields the source never used. Every non-trivial block of new code must trace to a concrete API difference.
2. **Preserve the application's public interface.** Keep function signatures, parameters, the command/operation surface, and (where the platform allows) the **response data shape** identical. Abstract v2-native concepts (URNs, projects, records, attribute maps) *behind* the existing interface rather than surfacing them to callers. Only change the interface when the platform makes it impossible not to, and when you do, see directive 3.
3. **Preserve behavior; flag every unavoidable change.** Where behavior must change, (a) keep it as close to v1 as the platform allows, (b) emit a one-line notice at runtime through the application's normal diagnostic channel, and (c) record it in a clearly labeled "Behavior changes vs. v1" section in the migrated artifact so a reviewer can audit it. Never change behavior silently.
4. **Consult the user to clarify ambiguity.** If there are decisions to be made that impact the interface of the application, you need to make sure to run these decisions by the user and get their involvement and signoff. Avoid assuming their intent and make decisions explicit before acting on them.

**Do not guess schema.** Two authoritative sources are available to you during this migration: the **migration manifest** (legacy-to-v2 identifier and field mappings) and **GraphQL introspection** (exact type, input, field, and enum names). Consult them instead of inventing names. If a name is still unknown after consulting both, stop and ask the user rather than guessing.

---

## Discovery tools

### 1. Migration manifest (call it once, during the migration)

The manifest maps the calling account's legacy identifiers and legacy fields to their workspace equivalents. It is a **one-time discovery aid for the migration work itself**, not a runtime dependency.

**Operating rules:**

- **Call it exactly once, as part of performing the migration.** Do **not** wire a manifest fetch into the runtime path of the migrated application. Use the manifest to learn the mappings and to resolve any legacy identifiers that are **hardcoded in the source** (fixed list identifiers, fixed custom-field identifiers, hardcoded sort fields, hardcoded entity projections). For identifiers the application accepts from its callers at runtime, prefer requiring the caller to supply the v2 URN directly (a documented interface change) over shipping a live translator. Only build a runtime translator if the source clearly depends on accepting legacy identifiers at runtime, and if you do, build it against the exact schema below, not a guessed one.
- **Before calling it, stop and ask the user for a customer-scoped API key.** Do not proceed with a placeholder. The endpoint is customer-scoped and returns 403 without a customer session.
- Fetch it with the account's API key:
  ```
  GET https://api.harmonic.ai/migration/manifest
  header: apikey: <API_KEY>
  ```
  Auth is the same `apikey` header used by every other call. Use the lowercase `apikey` header consistently on every request.

**Response schema** (all fields are always present; lists may be empty):

```jsonc
{
  "workspace_migration_phase": "DISABLED",              // migration-state enum. Will be "DISABLED" before data migration and "MIGRATED" after data migration
  "workspace_urn": "urn:harmonic:workspace:<uuid>",     // null before migration

  // Legacy watchlist -> workspace list. workspace_list_urn resolves even before
  // migration (the legacy UUID is preserved as the list id).
  // workspace_project_urn is null until the list is actually migrated.
  //
  // migration_strategy tells the caller HOW to migrate the watchlist:
  //   "workspace_list"   (default) — repoint to workspace_list_urn. Everything
  //                                   that worked against the legacy watchlist
  //                                   works against the v2 list.
  //   "records_endpoint" — the watchlist has NO v2 list equivalent (special
  //                        lists like Team Network, whose members migrate to
  //                        network_connections rather than to a list). On these
  //                        entries workspace_list_urn is still emitted but does
  //                        NOT resolve to a v2 list — ignore it and read the
  //                        records endpoint for record_type instead.
  //                        workspace_project_urn is always null.
  "list_mappings": [
    {
      "legacy_watchlist_urn": "urn:harmonic:company_watchlist:<uuid>",
      "workspace_list_urn":   "urn:harmonic:list:<uuid>",
      "workspace_project_urn": "urn:harmonic:project:<id>",   // or null
      "record_type": "company",                               // "company" | "person"
      "migration_strategy": "workspace_list"                  // "workspace_list" | "records_endpoint"
    }
  ],

  // Legacy LIST custom field -> workspace list attribute.
  "custom_field_mappings": [
    {
      "legacy_custom_field_urn": "urn:harmonic:company_list_custom_field:<id>",
      "legacy_type": "TEXT",                                  // legacy custom-field type
      "workspace_attribute_urn": "urn:harmonic:list_attribute:<id>", // null if unmapped
      "workspace_type": "STRING",                             // v2 type, null if unmapped
      "has_known_mapping": true
    }
  ],

  // Legacy GLOBAL (record-level) custom field -> workspace record attribute.
  // Same entry shape as custom_field_mappings.
  "global_custom_field_mappings": [ /* same shape */ ],

  // Legacy built-in ENTITY FIELD (by field URN) -> record attribute. Static and
  // workspace-independent, so populated even before migration. Legacy fields
  // with no workspace equivalent are OMITTED entirely.
  "company_field_mappings": [
    {
      "legacy_field_urn": "urn:harmonic:company_field:company_website_url",
      "workspace_attribute_urn": "urn:harmonic:record_attribute:company:website_url",
      "workspace_type": "URL"
    }
  ],
  "person_field_mappings": [ /* same shape, person namespace */ ],

  // Legacy v1 GraphQL PROJECTION PATH -> record attribute. Exhaustive over the
  // projectable surface of the v1 Company/Person GraphQL types. Use this to
  // translate a v1 selection set into the v2 attribute URNs a caller now passes.
  // workspace_attribute_urn is null when the path was projectable in v1 but has
  // no v2 equivalent (dropped in v2).
  "company_graphql_field_mappings": [
    {
      "graphql_path": "funding.numFundingRounds",
      "workspace_attribute_urn": "urn:harmonic:record_attribute:company:funding_rounds"  // or null
    }
  ],
  "person_graphql_field_mappings": [ /* same shape, person namespace */ ]
}
```

How to use each map:

- `list_mappings`, `custom_field_mappings`, `global_custom_field_mappings`: translate hardcoded legacy list and custom-field identifiers to their workspace URNs. On a `list_mappings` entry, always check `migration_strategy` first — a `records_endpoint` entry means "read the records endpoint for `record_type` instead of repointing to `workspace_list_urn`," which does not resolve to a v2 list on those entries.
- `company_graphql_field_mappings` / `person_graphql_field_mappings`: the primary tool for **replacing entity projections** (see "Replacing entity projections"). Given a v1 GraphQL selection path, look up the v2 attribute URN to request.
- `company_field_mappings` / `person_field_mappings`: translate legacy flat field identifiers, including hardcoded **sort fields**, to attribute URNs.
- A path or field with a **null** `workspace_attribute_urn`, or absent from a map, has **no v2 attribute**. Handle it per the projection rules below; never invent a URN.

### 2. GraphQL introspection (resolve every exact type, field, and enum name)

The v2 schema is introspectable, and its types, fields, and enums carry descriptions. **Query it and rely on it** rather than hardcoding names or values. Run a standard introspection query against the live schema:

```
POST https://api.harmonic.ai/graphql/v2
header: apikey: <API_KEY>
body:   {"query": "<standard introspection query>"}
```

Use introspection as the authority for, at minimum:

- The input-object type name and field set for every mutation you call.
- Every enum you emit or interpret, and its exact member values (for example: attribute/field types, import mode, source system, import task status, select-option colors).
- The scalar URN type names used as query arguments.
- Which typed value field an attribute value carries for a given field type, and which metadata sub-fields each field type requires (read the field descriptions).

Do not fall back to guessed names or enum values. If introspection is unavailable for the key, ask the user.

---

## Setup

- All v2 calls: HTTP `POST https://api.harmonic.ai/graphql/v2`, body `{"query","variables"}`.
- **Auth unchanged**: send the API key as the lowercase `apikey` header on every request, including the manifest and introspection. Do not vary header casing per endpoint.
- Bootstrap once and cache: `query { workspace { urn companyRecordType { urn } personRecordType { urn } projects(first:50){ edges{ node{ urn name isShared } } } } }`. You need the record-type URNs for record-scoped operations and the project URNs for list creation and sharing.

## Model deltas (why this is not find-and-replace)

- **Watchlist -> List** (belongs to a Project, scoped to a RecordType: `company` / `person` / `investor`).
- **Members -> Records wrapped in ListEntries.** List reads no longer inline `companies` / `people`; page `list.entries`. Each entry has `.record` and `.attributeValueMap` (a name-to-value map merging record and list values).
- **List custom field -> ListAttribute; global field -> RecordAttribute.**
- **Cursor pagination only** (`first` / `after` plus `pageInfo{hasNextPage endCursor}`); no `page` / `size`; `first` max 100.
- **Add-by-canonical and bulk value upsert -> async imports** (`createImport` then poll `importTask`).
- Everything is a URN (`urn:harmonic:list:...`, `:list_entry:`, `:record:`, `:list_attribute:`, `:record_attribute:`, `:import_task:`, plus `urn:harmonic:company:{id}` / `:person:{id}`).

---

## Preserving output shape and entity projections (highest-risk area)

The most common regression in an API migration like this is **silent data loss**: minimal example projections get copied verbatim, dropping fields the v1 query returned. Guard against it:

1. **The GraphQL snippets in this document are minimal illustrations of an operation, not the field set to request.** For every migrated read, enumerate every field the v1 query selected and request the v2 equivalent for each. Do not shrink a projection to match an example.
2. **Reshape v2 responses back to the v1 data shape** wherever possible, so callers see the same structure. Where the shape genuinely cannot match (for example a typed value list becoming a merged attribute map), keep it as close as possible, emit a runtime notice, and document it under "Behavior changes vs. v1".
3. **Metadata reads must keep their v1 fields.** If a v1 "get one list" returned counts, timestamps, custom-field definitions, and named views, reconstruct each from its v2 source (entry `totalCount`, list attributes, named views, project sharing) rather than returning only `urn` and `name`.

### Replacing entity projections

When a v1 read projected entity fields (for example a nested `company { website { url } }` or `person { linkedinHeadline }`), resolve each projected path in this order:

1. **GraphQL field map (preferred).** Look the v1 projection path up in `company_graphql_field_mappings` / `person_graphql_field_mappings`. If it maps to a non-null attribute URN, request that attribute and read its value from the entry/record `attributeValueMap`.
2. **Flat field map.** If the path is not in the GraphQL map, try `company_field_mappings` / `person_field_mappings` by legacy field URN.
3. **Two-phase resolution (fallback).** If there is no mapping and the field is still required:
   1. Page the list or record type for entry `record.harmonicUrn` values.
   2. Extract integer ids (`urn:harmonic:company:123` yields `123`).
   3. Batch-fetch the needed fields on the **non-deprecated** entity GraphQL (for example `getCompaniesByIds` / `getPersonsByIds`) and merge the results back into the entry shape.
4. **Drop only when unused and unmapped.** Only drop a projected field after confirming it is both unused by the application and has no mapping. When you drop one, emit a runtime notice and record it under "Behavior changes vs. v1". Never drop silently.

---

## Lists (Company and People are symmetric: same v2 operations, pick the record type)

| v1 use case (REST, GraphQL) | v2 |
| --- | --- |
| Get all lists: `getCompany/PeopleWatchlistsForTeam` | `workspace { lists(first,after){ edges{ node{ urn name recordType{urn} } } pageInfo{hasNextPage endCursor} } }` (filter by record type client-side; preserve v1 fields such as owner/sharing where a v2 source exists) |
| Get a list: `get...WatchlistByIdOrUrn` | `list(urn:ListURN!){ ... }` (request the full v1 field set per the projection rules, not just `urn name totalCount`) |
| Get list entries (page/sort/search) | `list(urn:){ entries(first,after,filter,orderBy){ edges{ node{ urn record{urn name harmonicUrn} attributeValueMap } } pageInfo{hasNextPage endCursor} } }` |
| Create list: `create...Watchlist` | `createList(input:{recordTypeUrn,name}){ list{urn} }` |
| Update list: `update...Watchlist` | `updateList(input:{urn,name,...})`  |
| Delete list: `delete...Watchlist` | `deleteList(input:{urn}){ success }` |
| Add by id/urn: `add...ToWatchlistWithUrns` | `createListEntries(input:{targetListUrn,selection:{harmonicUrns:[...]}}){ createdCount skippedCount notFoundCount }` (or `recordUrns`) |
| Add by canonical (domain/linkedin/email) | `createImport` (see Imports) |
| Remove: `remove...FromWatchlistWithUrns` | `deleteListEntries(input:{targetListUrn,selection:{recordUrns:[...]}}){ deletedCount }` (or `harmonicUrns` / `entryUrns`) |
| Delete list entries (`:batchDelete`) | `deleteListEntries(...)` (same) |
| Upsert list entries (entries plus custom field values) | `createImport(mode:UPSERT)` (see Imports) |
| Upsert named view | `createNamedView` / `updateNamedView(input:{listUrn|urn,name,filter,columns,sorts})`; delete: `deleteNamedView(input:{urn})` |
| Create/Update/Delete custom field | `createListAttribute(input:{listUrn,fieldName,fieldType,fieldMetadata})` / `updateListAttribute(input:{urn,...})` / `deleteListAttribute(input:{urn})` |
| Get import details / entries / list imports | `importTask(urn:){ status ... }` / `importTask(urn:){ importEntries(status,paginationInput){...} }` / `list(urn:){ importTasks(paginationInput){...} }` |
| (People) Get all people updates in a list | per-record via `record.updateEvents` (see People updates) |

### Sorting (legacy field name -> attribute / sort-order URN)

In v1, sort parameters were plain legacy field names. In v2, `orderBy` takes a sort-order URN (`entries(orderBy:[{sortOrderUrn,descending}])`). Translate rather than pass through:

- For a hardcoded sort field, resolve it via the manifest field maps (construct the legacy field URN, look up its `workspace_attribute_urn`).
- For a sort field supplied by the caller at runtime, require the v2 attribute / sort-order URN (a documented interface change).
- This is a nuanced, breaking interface change; flag it clearly. The move from legacy field names to attribute URNs is expected and desired, reflecting the real v1-to-v2 behavior change. Do not try to fake the old plain-name interface.

### People updates (unbounded history -> time-windowed events)

The v1 people-in-watchlist read exposed an **unbounded** `updates` list. The v2 equivalent is per record: `record.updateEvents(since:Time)`, which returns an array and is time-windowed:

```graphql
list(urn:){ entries(first,after){ edges{ node{ record{
  updateEvents(since:$since){ eventType eventDate detectedAt
    metadata{ ...on PersonJobStartedMetadata{ companyName positionTitle } } } } } } } }
```

- **Set `since` explicitly.** Do not rely on the default window. Choose a deliberate window that best approximates the source behavior (for example a far-past timestamp, or a caller-supplied lookback), make the bound explicit in code, and document the exact window under "Behavior changes vs. v1". There is no truly unbounded v2 option. Confirm the argument's type and default via introspection.

---

## Global fields (record-level)

| v1 use case | v2 |
| --- | --- |
| Get global fields: `company/peopleCustomFields` | `recordType(urn:RecordTypeURN!){ attributes{ urn fieldName fieldType } }` |
| Create / Update / Delete global field | `createRecordAttribute(input:{recordTypeUrn,fieldName,fieldType,fieldMetadata})` / `updateRecordAttribute(input:{urn,...})` / `deleteRecordAttribute(input:{urn})` |
| Upsert global field values | `createImport(input:{recordTypeURN,mode:UPSERT,rows:[...]})`, or `updateRecord(s)` |
| Get global field values: `getCompany/PersonById -> customFieldValues` | `record(urn:RecordURN!,recordTypeUrn:RecordTypeURN!){ attributeValueMap }` |

> **Write scope (unchanged from v1):** custom/global field *values* can only be written on team-shared lists. Pre-existing limitation, not a regression.

## Attachments (company/person files, now in v2)

v2 attachments hang off a **Record** (`RecordURN`), so first resolve the record URN (from a list entry's `.record.urn`, or `records(urns:[...],recordTypeUrn:)`). The three-phase v1 upload collapses to one multipart `createRecordAttachment`.

| v1 use case | v2 |
| --- | --- |
| Get attachments for companies/persons | `record(urn:RecordURN!,recordTypeUrn:){ attachments(first,after){ edges{ node{ urn name extension sizeBytes uploadedAt } } pageInfo{hasNextPage endCursor} } }` (batch via `records(urns,recordTypeUrn)`; preserve v1 attachment fields where a v2 equivalent exists, drop-and-flag only if truly unavailable) |
| Initiate plus complete upload (2 v1 calls) | one multipart request: `createRecordAttachment(input:{record:RecordURN!, file:Upload!}){ attachment{urn} }` |
| Rename attachment | `updateRecordAttachment(input:{attachment:Urn!, record:RecordURN!, name:String!}){ attachment{urn name} }` |
| Delete attachment | `deleteRecordAttachment(input:{attachment:Urn!, record:RecordURN!}){ deletedUrn }` |

## Customer / users (in v2 via workspace)

| v1 use case | v2 |
| --- | --- |
| Get customer by URN | `workspace { urn name customerUrn }` |
| Get customer users | `workspace { users(first,after){ edges{ node{ urn name email role status } } pageInfo{hasNextPage endCursor} } }` |

---

## Essential patterns

**Cursor pagination** (replace every page/size loop):

```python
cursor=None
while True:
  r=gql("query($u:ListURN!,$a:String){list(urn:$u){entries(first:100,after:$a){edges{node{urn record{urn name harmonicUrn} attributeValueMap}} pageInfo{hasNextPage endCursor}}}}",{"u":urn,"a":cursor})
  c=r["list"]["entries"]; handle(n["node"] for n in c["edges"])
  if not c["pageInfo"]["hasNextPage"]: break
  cursor=c["pageInfo"]["endCursor"]
```

**Custom field plus a value on one entry:**

```graphql
createListAttribute(input:{listUrn:$l, fieldName:"Stage", fieldType:SINGLE_SELECT,
  fieldMetadata:{select:{options:[{label:"Sourced",color:0}]}}}){ listAttribute{urn} }

updateListEntry(input:{ selection:{listUrn:$l, recordUrn:$r},
  attributeValues:[{attributeUrn:$attr, stringValue:"Sourced"}] }){ listEntry{urn} }
```

An attribute value carries exactly one typed value field, chosen by the attribute's field type; some field types require `fieldMetadata` sub-fields. Use introspection to read the field-type enum, which value field pairs with each type, and which metadata sub-fields each type requires.

**Imports** (add-by-canonical and bulk value upsert; async, max 1000 rows/request):

```graphql
createImport(input:{ listURN:$l, sourceSystem:API, mode:UPSERT, rows:[
  { rowIndex:0, harmonicUrn:"urn:harmonic:company:123",
    attributeValues:[{attributeUrn:"urn:harmonic:list_attribute:...", stringValue:"Sourced"}] },
  { rowIndex:1, canonicalInput:{companyCanonicals:{websiteURL:"https://acme.com"}} }
]}){ importTask{ urn status } }
```

- Each row needs `harmonicUrn` or `canonicalInput`. Omit `listURN` and pass `recordTypeURN` for list-less global value upserts.
- Resolve the import mode, source system, and canonical sub-input field names via introspection.

**Poll the import to preserve a synchronous contract.** If the v1 call returned a final result synchronously, keep that behavior by polling `importTask(urn:$t){ status ... }` until it reaches a terminal status. Discover the status enum's members and which are terminal via introspection; poll while non-terminal. Wrapping the async import in a poll loop is the intended pattern; note the async-under-the-hood nature under "Behavior changes vs. v1" because failure and timeout handling differ from v1.

**CSV export** (REST on the v2 host; streams `text/csv`; API-key callers have no row limit):

```
POST /graphql/v2/api/export-service              {"listUrn","columns":[{"attributeUrn"}],"filter":null,"sorts":[{"sortOrderUrn","descending"}]}
POST /graphql/v2/api/export-service/view         {"viewUrn"}
POST /graphql/v2/api/export-service/record-type  {"recordTypeUrn","columns","filter","sorts"}
```

---

## Stays on existing endpoints (do not rewrite; flag if touched)

- **Not deprecated, leave unchanged:** enrichment (`/companies`, `/persons`, `enrichCompany/PersonByIdentifiers`), enrichment status, search and saved searches (`/savedSearches...`, `getSavedSearchesForTeam`, typeahead, saved-search results), entity fetch (`/companies/{id}`, `/persons/{id}`, `batchGet`, `getCompaniesByIds` / `getPersonsByIds`, employees), deal data (investors/financing), and network mapping.
- **Network mapping** (`userConnections`, `usersInNetwork`, `getPeopleInNetwork`, `getCompaniesInNetwork`) is not a first-class v2 query; keep it on the existing entity GraphQL. Partial v2 support: the `connected_by` harmonic attribute (`urn:harmonic:record_attribute:{company|person}:connected_by`) can be projected, filtered, and sorted on `record` / `list.entries` queries; resolve its URN via `workspace.{company,person}HarmonicAttributes -> recordAttributeUrn`. Other network reads stay on v1.

## Gotchas

- Imports are async; do not read entries immediately after `createImport`, poll first.
- Add-by-URN (`createListEntries`) is not add-by-canonical (`createImport`); use the right one per input type.
- Single-entity reads need scoping URNs: `record(urn,recordTypeUrn)`, `listEntry(urn,listUrn)`.
- List reads return counts only; membership comes from `entries`.
- Affinity-linked lists: verify add/remove behavior on a test list first.

---

## Migration task list

Work through these steps in order. They apply to any application regardless of language or shape.

1. **Inventory the source.** Enumerate every call the application makes to a Harmonic v1 endpoint or GraphQL operation. For each, record the use case, the exact fields it reads or writes, and how it paginates. Mark each as either on the deprecation path (has a v2 equivalent in the tables above) or not deprecated (stays as-is).
2. **Determine a migration and deployment strategy.**. Consult the user on key decisions on how to handle the downtime during Harmonic data migration and how to deploy the application against the new V2 APIs. Approach the code change in the context of this strategy.
3. **Request credentials.** Stop and ask the user for a customer-scoped API key before making any authenticated call.
4. **Fetch the migration manifest once.** Call `GET /migration/manifest` with the key and capture every mapping section. Use it only during this migration, never on the runtime path.
5. **Introspect the v2 schema.** Query the introspection endpoint and obtain the full v2 schema: all types, input objects, field sets, enum members, and scalar URN type names. Treat this as the authority for exact names and enum values.
6. **Bootstrap the workspace.** Fetch and cache the workspace record-type URNs and project URNs.
7. **Migrate each deprecated call.** For each, swap the v1 operation for its v2 equivalent, preserving the full v1 field set (using the projection-replacement order), reshaping the response to the v1 data shape, translating hardcoded identifiers and sort fields via the manifest, using introspected names and enums, converting page-number loops to cursor loops, and polling imports to a terminal status where v1 was synchronous.
8. **Leave non-deprecated calls untouched.** For any use case with no v2 path, keep it on the existing endpoint and add a `TODO(harmonic-migration)` note.
9. **Handle interface and behavior changes deliberately.** Preserve the public interface and behavior wherever possible. For each unavoidable change, keep it as close to v1 as the platform allows, emit a one-line runtime notice, and add an entry to a "Behavior changes vs. v1" section in the migrated artifact.
10. **Verify.** Confirm the behavior of the application works as intended between the V1 and V2 APIs. When making live API calls in the "playground" stage remember that the V1 APIs will operate on a separate copy of the data. Create automated tests that verify all calls work as expected and application behavior is retained. If behavior differs, evaluate if the difference is intentional or if indicates a real bug in the implementation and correct it.
11. **Deliver.** Produce the migrated artifact plus the "Behavior changes vs. v1" summary listing every interface or behavior difference and every dropped field, so a reviewer can audit the migration.
````

### Deprecated endpoints

Every endpoint and GraphQL operation below stops serving traffic on November 5th, 2026. Use these tables to audit your integration: if you call anything in the left two columns, the right column is where it goes.

- **Legacy REST** endpoints live on `https://api.harmonic.ai`.
- **Legacy GraphQL** operations run against `POST https://api.harmonic.ai/graphql`.
- **Replacements** are GraphQL operations on `POST https://api.harmonic.ai/graphql/v2` (except CSV export, which is REST on the v2 host).

**Not deprecated:** enrichment (`/companies`, `/persons`), search and saved searches (`/savedSearches…`), entity fetch (`/companies/{id}`, `/persons/{id}`, `batchGet`, employees), deal data (investors/financing), and network mapping (`userConnections`, in-network queries) are unaffected and stay where they are.

#### Company lists

| Use case                                     | Legacy REST                                                                         | Legacy GraphQL                                                               | Replaced by (v2)                                                |
| -------------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Get all company lists                        | `GET /watchlists/companies`                                                         | `getCompanyWatchlistsForTeam`                                                | `workspace.lists`                                               |
| Get a company list                           | `GET /watchlists/companies/{id_or_urn}`                                             | `getCompanyWatchlistByIdOrUrn`                                               | `list`                                                          |
| Get company list entries                     | `GET /watchlists/companies/{id_or_urn}/entries`                                     | `getCompaniesInWatchlistByIdOrUrn`                                           | `list.entries`                                                  |
| Create company list                          | `POST /watchlists/companies`                                                        | `createCompanyWatchlist`                                                     | `createList`                                                    |
| Update company list                          | `PUT /watchlists/companies/{id_or_urn}`                                             | `updateCompanyWatchlist`                                                     | `updateList`                                                    |
| Delete company list                          | `DELETE /watchlists/companies/{id_or_urn}`                                          | `deleteCompanyWatchlist`                                                     | `deleteList`                                                    |
| Add companies to list                        | `POST /watchlists/companies/{id_or_urn}:addCompanies`                               | `addCompaniesToWatchlistWithIds` / `…WithUrns` / `…WithCanonicals`           | `createListEntries` (by URN); `createImport` (by canonical)     |
| Remove companies from list                   | `POST /watchlists/companies/{id_or_urn}:removeCompanies`                            | `removeCompaniesFromWatchlistWithIds` / `…WithUrns`                          | `deleteListEntries`                                             |
| Upsert list entries (members + field values) | `POST /watchlists/companies/{id_or_urn}/entries`                                    | `upsertCompanyWatchlistEntries`, `upsertCompanyWatchlistCustomFieldValue(s)` | `createImport` (mode `UPSERT`); single entry: `updateListEntry` |
| Delete list entries                          | `POST /watchlists/companies/{id_or_urn}/entries:batchDelete`                        | `removeCompanyEntriesFromWatchlist`                                          | `deleteListEntries`                                             |
| Upsert named view                            | `POST /watchlists/companies/{id_or_urn}/named_views` (`?named_view_urn=` to update) | `upsertCompanyListNamedView`                                                 | `createNamedView` / `updateNamedView`                           |
| Delete named view                            | —                                                                                   | `removeCompanyListNamedView`                                                 | `deleteNamedView`                                               |
| Create list custom field                     | `POST /watchlists/companies/{id_or_urn}/custom_field`                               | `createCompanyWatchlistCustomField`                                          | `createListAttribute`                                           |
| Update list custom field                     | `PUT /watchlists/companies/{id_or_urn}/custom_field`                                | `updateCompanyWatchlistCustomField`                                          | `updateListAttribute`                                           |
| Delete list custom field                     | `DELETE /watchlists/companies/{id_or_urn}/custom_field`                             | `removeCompanyWatchlistCustomField`                                          | `deleteListAttribute`                                           |
| Get import details                           | `GET /watchlists/companies/imports/{id_or_urn}`                                     | `getUserCompaniesImportByIdOrUrn`                                            | `importTask`                                                    |
| Get import entries                           | `GET /watchlists/companies/imports/{id_or_urn}/entries`                             | `getUserCompaniesImportByIdOrUrn` (entries)                                  | `importTask.importEntries`                                      |
| Get list imports                             | `GET /watchlists/companies/{id_or_urn}/imports`                                     | `getUserCompaniesImportsByCompaniesListUrnOrId`                              | `list.importTasks`                                              |

#### People lists

| Use case                                     | Legacy REST                                                                      | Legacy GraphQL                                                             | Replaced by (v2)                                                |
| -------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Get all people lists                         | `GET /watchlists/people`                                                         | `getPeopleWatchlistsForTeam`                                               | `workspace.lists`                                               |
| Get a people list                            | `GET /watchlists/people/{id_or_urn}`                                             | `getPeopleWatchlistByIdOrUrn`                                              | `list`                                                          |
| Get people list entries                      | `GET /watchlists/people/{id_or_urn}/entries`                                     | `getPeopleInWatchlistByIdOrUrn`                                            | `list.entries`                                                  |
| Create people list                           | `POST /watchlists/people`                                                        | `createPeopleWatchlist`                                                    | `createList`                                                    |
| Update people list                           | `PUT /watchlists/people/{id_or_urn}`                                             | `updatePeopleWatchlist`                                                    | `updateList`                                                    |
| Delete people list                           | `DELETE /watchlists/people/{id_or_urn}`                                          | `deletePeopleWatchlist`                                                    | `deleteList`                                                    |
| Add people to list                           | `POST /watchlists/people/{id_or_urn}:addPeople`                                  | `addPeopleToWatchlistWithIds` / `…WithUrns` / `…WithCanonicals`            | `createListEntries` (by URN); `createImport` (by canonical)     |
| Remove people from list                      | `POST /watchlists/people/{id_or_urn}:removePeople`                               | `removePeopleFromWatchlistWithIds` / `…WithUrns`                           | `deleteListEntries`                                             |
| Upsert list entries (members + field values) | `POST /watchlists/people/{id_or_urn}/entries`                                    | `upsertPeopleWatchlistEntries`, `upsertPeopleWatchlistCustomFieldValue(s)` | `createImport` (mode `UPSERT`); single entry: `updateListEntry` |
| Delete list entries                          | `POST /watchlists/people/{id_or_urn}/entries:batchDelete`                        | `removePeopleEntriesFromWatchlist`                                         | `deleteListEntries`                                             |
| Upsert named view                            | `POST /watchlists/people/{id_or_urn}/named_views` (`?named_view_urn=` to update) | `upsertPeopleListNamedView`                                                | `createNamedView` / `updateNamedView`                           |
| Delete named view                            | —                                                                                | `removePeopleListNamedView`                                                | `deleteNamedView`                                               |
| Create list custom field                     | `POST /watchlists/people/{id_or_urn}/custom_field`                               | `createPeopleWatchlistCustomField`                                         | `createListAttribute`                                           |
| Update list custom field                     | `PUT /watchlists/people/{id_or_urn}/custom_field`                                | `updatePeopleWatchlistCustomField`                                         | `updateListAttribute`                                           |
| Delete list custom field                     | `DELETE /watchlists/people/{id_or_urn}/custom_field`                             | `removePeopleWatchlistCustomField`                                         | `deleteListAttribute`                                           |
| Get import details                           | `GET /watchlists/people/imports/{id_or_urn}`                                     | `getUserPeopleImportByIdOrUrn`                                             | `importTask`                                                    |
| Get import entries                           | `GET /watchlists/people/imports/{id_or_urn}/entries`                             | `getUserPeopleImportByIdOrUrn` (entries)                                   | `importTask.importEntries`                                      |
| Get list imports                             | `GET /watchlists/people/{id_or_urn}/imports`                                     | `getUserPeopleImportsByPeopleListUrnOrId`                                  | `list.importTasks`                                              |
| Get all people updates in a list             | —                                                                                | `getPeopleInWatchlistByIdOrUrn` → `updates`                                | `record.updateEvents` (via `list.entries`)                      |

#### Company attachments

| Use case                      | Legacy REST                                       | Legacy GraphQL              | Replaced by (v2)                                                                 |
| ----------------------------- | ------------------------------------------------- | --------------------------- | -------------------------------------------------------------------------------- |
| Get attachments for companies | `POST /companies/attachments`                     | —                           | `record.attachments` (batch via `records`)                                       |
| Initiate attachment upload    | `POST /companies/{id_or_urn}/attachments`         | `createAttachments`         | `createRecordAttachment` (one multipart request — no separate initiate/complete) |
| Complete attachment uploads   | `PUT /companies/{id_or_urn}/attachments`          | `completeAttachmentUploads` | `createRecordAttachment` (same — steps merged)                                   |
| Rename attachment             | `PATCH /companies/{id_or_urn}/attachments/{urn}`  | `updateAttachment`          | `updateRecordAttachment`                                                         |
| Get attachment contents       | `GET /companies/{id_or_urn}/attachments/{urn}`    | —                           | `Attachment.contentUrl` (signed download URL)                                    |
| Delete attachment             | `DELETE /companies/{id_or_urn}/attachments/{urn}` | `deleteAttachment`          | `deleteRecordAttachment`                                                         |

#### Person attachments

| Use case                    | Legacy REST                                     | Legacy GraphQL              | Replaced by (v2)                                 |
| --------------------------- | ----------------------------------------------- | --------------------------- | ------------------------------------------------ |
| Get attachments for persons | `POST /persons/attachments`                     | —                           | `record.attachments` (batch via `records`)       |
| Initiate attachment upload  | `POST /persons/{id_or_urn}/attachments`         | `createAttachments`         | `createRecordAttachment` (one multipart request) |
| Complete attachment uploads | `PUT /persons/{id_or_urn}/attachments`          | `completeAttachmentUploads` | `createRecordAttachment` (same — steps merged)   |
| Rename attachment           | `PATCH /persons/{id_or_urn}/attachments/{urn}`  | `updateAttachment`          | `updateRecordAttachment`                         |
| Get attachment contents     | `GET /persons/{id_or_urn}/attachments/{urn}`    | —                           | `Attachment.contentUrl` (signed download URL)    |
| Delete attachment           | `DELETE /persons/{id_or_urn}/attachments/{urn}` | `deleteAttachment`          | `deleteRecordAttachment`                         |

#### Company global fields

| Use case                   | Legacy REST                      | Legacy GraphQL                         | Replaced by (v2)                                            |
| -------------------------- | -------------------------------- | -------------------------------------- | ----------------------------------------------------------- |
| Get global fields          | `GET /companies/custom_fields`   | `companyCustomFields`                  | `recordType.attributes`                                     |
| Create a global field      | `POST /companies/custom_field`   | `createCompanyCustomField`             | `createRecordAttribute`                                     |
| Update a global field      | `PUT /companies/custom_field`    | `updateCompanyCustomField`             | `updateRecordAttribute`                                     |
| Delete a global field      | `DELETE /companies/custom_field` | `removeCompanyCustomField`             | `deleteRecordAttribute`                                     |
| Upsert global field values | `POST /companies/entries`        | `upsertCompanyCustomFieldValues`       | `createImport` (with `recordTypeURN`); or `updateRecord(s)` |
| Get global field values    | —                                | `getCompanyById` → `customFieldValues` | `record.attributeValueMap`                                  |

#### Person global fields

| Use case                   | Legacy REST                    | Legacy GraphQL                        | Replaced by (v2)                                            |
| -------------------------- | ------------------------------ | ------------------------------------- | ----------------------------------------------------------- |
| Get global fields          | `GET /persons/custom_fields`   | `peopleCustomFields`                  | `recordType.attributes`                                     |
| Create a global field      | `POST /persons/custom_field`   | `createPeopleCustomField`             | `createRecordAttribute`                                     |
| Update a global field      | `PUT /persons/custom_field`    | `updatePeopleCustomField`             | `updateRecordAttribute`                                     |
| Delete a global field      | `DELETE /persons/custom_field` | `removePeopleCustomField`             | `deleteRecordAttribute`                                     |
| Upsert global field values | `POST /persons/entries`        | `upsertPeopleCustomFieldValues`       | `createImport` (with `recordTypeURN`); or `updateRecord(s)` |
| Get global field values    | —                              | `getPersonById` → `customFieldValues` | `record.attributeValueMap`                                  |

#### Customer

| Use case            | Legacy REST                  | Legacy GraphQL                | Replaced by (v2)                     |
| ------------------- | ---------------------------- | ----------------------------- | ------------------------------------ |
| Get customer by URN | `GET /customers/{urn}`       | `getCustomerByUrn`            | `workspace { urn name customerUrn }` |
| Get customer users  | `GET /customers/{urn}/users` | `getAllTeamMembersByCustomer` | `workspace.users`                    |

## Company lists

Create, update, and manage company lists and their entries.

### Get all company lists

Get all company lists accessible to your account.

**GET** `https://api.harmonic.ai/watchlists/companies`

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/companies`

```json
[{
  "id": "6f7f8d5f-43dd-45b6-955f-87ec129b0006",
  "entity_urn": "urn:harmonic:company_watchlist:123",
  "name": "Example test",
  "companies_count": 2,
  "custom_fields": [
    {
      "name": "Priority",
      "type": "NUMBER"
    }
  ],
  "named_views": [
    {
      "name": "My Custom View",
      "display_type": "GRID"
    }
  ]
}]
```

**GraphQL query**

```graphql
query Query {
  getCompanyWatchlistsForTeam {
    name
    entityUrn
    id
    owner {
        ... on User {
          entityUrn
          email
          name
          customer {
            name
            identifier
          }
        }
        ... on Customer {
          name
          identifier
        }
    }
    sharedWithTeam
  }
}
```

### Get a company list

Get details about a company list including its entries, custom fields, and named views.

ID example:

```
GET https://api.harmonic.ai/watchlists/companies/780c2910-b21d-4ad2-ba04-c98ac939dbd8
```

URN example:

```
GET https://api.harmonic.ai/watchlists/companies/urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8
```

**GET** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}`

To learn more about switching to cursor pagination, read about [pagination query parameters here](/docs/api-reference/introduction#pagination).

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/companies/{id_or_urn}`

```json
{
  "id": "6f7f8d5f-43dd-45b6-955f-87ec129b0006",
  "entity_urn": "urn:harmonic:company_watchlist:123",
  "name": "Example test",
  "companies_count": 2,
  "custom_fields": [
    {
      "name": "Priority",
      "type": "NUMBER"
    }
  ],
  "named_views": [
    {
      "name": "My Custom View",
      "display_type": "GRID"
    }
  ]
}
```

**GraphQL query**

```graphql
query GetCompanyWatchlist($idOrUrn: String!) {
  getCompanyWatchlistByIdOrUrn(idOrUrn: $idOrUrn) {
    id
    entityUrn
    name
    sharedWithTeam
    createdAt
    updatedAt
    creator {
      entityUrn
    }
    owner {
      ... on User {
        entityUrn
      }
      ... on Customer {
        entityUrn
      }
    }
    companiesCount
    customFields {
      createdAt
      updatedAt
      name
      urn
      type
      metadata {
        ... on NumberListCustomFieldMetadata {
          format
        }
        ... on SelectListCustomFieldMetadata {
          options {
            color
            name
            urn
          }
        }
      }
    }
    namedViews {
      entityUrn
      name
      displayType
      groupByField {
        urn
      }
      hideEmptyColumns
      searchQuery
      visibleColumns
    }
    companyEntries(first: 10) {
      edges {
        cursor
        node {
          company {
            entityUrn
            name
          }
          customFieldValues {
            createdAt
            updatedAt
            urn
            data {
              ... on NumberListCustomFieldValue {
                number: value
              }
              ... on SingleSelectCustomFieldValue {
                singleSelect: value
              }
            }
            customField {
              urn
              name
              type
            }
          }
          entryCreatedAt
          entryUrn
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
    }
  }
}
```

**GraphQL variables**

```json
{"idOrUrn": "urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8"}
```

### Get companies list entries

Pass the id or urn of a list to get entries.

ID example:

```
GET https://api.harmonic.ai/watchlists/companies/780c2910-b21d-4ad2-ba04-c98ac939dbd8/entries
```

URN example:

```
GET https://api.harmonic.ai/watchlists/companies/urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8/entries
```

**GET** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/entries`

| Name | Type | Description |
| --- | --- | --- |
| `sort_field` | string | Examples: company_id, company_entry_created_at |
| `urns` | array[company urn] | Filter by specific company URNs. Example: { "urns": ["urn:harmonic:company:22","urn:harmonic:company:1690"] } |

##### Example request with array query parameters

Repeat the `urns` parameter once per value:

```
GET https://api.harmonic.ai/watchlists/companies/{id_or_urn}/entries?urns=urn:harmonic:company:22&urns=urn:harmonic:company:1690&sort_field=company_id
```

To learn more about switching to cursor pagination, read about [pagination query parameters here](/docs/api-reference/introduction#pagination).

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/companies/{id_or_urn}/entries`

```json
{
    "entries": [...],
    "page_info": {
      "next": "Wzc1MjAwXQ==",
      "current": null,
      "has_next": true
    },
    "total_count": 1
}
```

**GraphQL query**

```graphql
query GetWatchlistWithCompanies(
  $idOrUrn: String!
  $page: Int
  $size: Int
  $first: Int
  $after: String
  $sortField: String
  $sortDescending: Boolean
) {
  getCompanyWatchlistByIdOrUrn(idOrUrn: $idOrUrn) {
    id
    companyEntries(
      page: $page
      size: $size
      first: $first
      after: $after
      sortField: $sortField
      sortDescending: $sortDescending
    ) {
      __typename
      edges {
        cursor
        node {
          entryCreatedAt
          entryUrn
          customFieldValues {
            createdAt
            updatedAt
            urn
            data {
              ... on NumberListCustomFieldValue {
                numberValue: value
              }
              ... on SingleSelectCustomFieldValue {
                singleSelectValue: value
              }
            }
            customField {
              urn
              name
              type
            }
          }
          company {
                      companyType
          contact {
            emails
            phoneNumbers
          }
          description
          entityUrn
          foundingDate {
            date
            granularity
          }
          funding {
            fundingTotal
            numFundingRounds
            lastFundingAt
            lastFundingType
            lastFundingTotal
            investors {
              ... on Company {
                name
              }
              ... on Person {
                fullName
              }
            }
            fundingRounds {
              entityUrn
              announcementDate
              fundingRoundType
              fundingAmount
              fundingCurrency
              sourceUrl
              postMoneyValuation
              investors {
                investorName
                isLead
                entityUrn
              }
            }
          }
          websiteDomainAliases
          nameAliases
          fundingAttributeNullStatus
          id
          logoUrl
          legalName
          name
          ownershipStatus
          headcount
          stage
          highlights {
            text
            category
          }
          numNotableFollowers
          notableFollowers(first: 2) {
            followerName
            followerUrn
            firmName
            firmUrn
            followedName
            followedUrn
            followObservedAt
          }
          initializedDate
          location {
            country
            zip
            state
            city
            street
            location
            addressFormatted
          }
          employees {
            entityUrn
            fullName
            firstName
            lastName
            profilePictureUrl
            contact {
              phoneNumbers
              emails
            }
            location {
              country
              zip
              state
              city
              street
              location
              addressFormatted
            }
            education {
              endDate
              startDate
              grade
              field
              degree
              school {
                name
                websiteUrl
                linkedinUrl
                logoUrl
                entityUrn
              }
            }
            experience {
              location
              isCurrentPosition
              endDate
              startDate
              description
              title
              department
              contact {
                emails
                phoneNumbers
              }
            }
            awardsBeta
            recommendationsBeta
          }
          snapshots {
            name
          }
          socials {
             facebook {
              url
              followerCount
             }
             twitter {
              followerCount
              url
             }
             linkedin {
              followerCount
              url
             }
             instagram {
              followerCount
              url
             }
             crunchbase {
              url
              followerCount
             }
             pitchbook {
              followerCount
              url
             }
             angellist {
              followerCount
              url
             }
             indeed {
              followerCount
              url
             }
             youtube {
              followerCount
              url
             }
             monster {
              followerCount
              url
             }
             stackoverflow {
              url
              followerCount
             }
          }
          website {
            isBroken
            domain
            url
          }
          tags {
            type
            displayValue
            entityUrn
            dateAdded
          }
          userConnections {
            user {
              email
              name
            }
          }
          tractionMetrics {
            headcount {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            webTraffic {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountAdvisor {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountCustomerSuccess {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountMarketing {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountOther {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountProduct {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountSales {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountSupport {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountData {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountDesign {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountEngineering {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountFinance {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountOperations {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountLegal {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountPeople {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            facebookFollowerCount {
              ago14d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            linkedinFollowerCount {
              ago14d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            instagramFollowerCount {
              ago14d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            twitterFollowerCount {
              ago14d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
          }
          relatedCompanies {
            priorStealthAssociation {
              emergenceDate
              previouslyKnownAs
            }
          }
          }
        }
      }
      totalCount
      pageInfo {
        hasNextPage
        startCursor
        endCursor
      }
    }
  }
}
```

**GraphQL variables**

```json
{"idOrUrn": "urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8"}
```

### Create new company list

In the body, pass the name, if it's shared with team, and a list of companies.

**POST** `https://api.harmonic.ai/watchlists/companies`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Name of the list |
| `shared_with_team` | boolean | true: visible on console. false: API only. |
| `companies` | array[company urn] | The ids or urns of companies. Can be empty. |

##### Example request

```json
{
  "name": "My Companies",
  "shared_with_team": true,
  "companies": ["urn:harmonic:company:22", "urn:harmonic:company:1690"]
}
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/watchlists/companies`

```json
{
    "urn": "urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c000000000000",
}
```

**GraphQL query**

```graphql
mutation CreateWatchlist($watchlistInput: CompanyWatchlistInput!) {
  createCompanyWatchlist(watchlistInput: $watchlistInput) {
    id
    entityUrn
    name
    userWatchlistType
    sharedWithTeam
    owner {
      ... on User {
        name
        entityUrn
        __typename
      }
      ... on Customer {
        name
        identifier
        __typename
      }
      __typename
    }
    __typename
  }
}
```

**GraphQL variables**

```json
{
  "watchlistInput": {
    "name": "My Company Watchlist",
    "sharedWithTeam": false,
    "companies": ["urn:harmonic:company:1000000", "urn:harmonic:company:2000000"]
  }
}
```

### Update company list

To update name or if list is shared with team.

**PUT** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | New name for the list |
| `shared_with_team` | boolean | true: visible on console. false: API only. |

##### Example request

```json
{
  "name": "Renamed list",
  "shared_with_team": true
}
```

Supported modes: REST, GraphQL

**REST**

`PUT https://api.harmonic.ai/watchlists/companies/{id_or_urn}`

```json
{
    "urn": "urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c000000000000",
}
```

**GraphQL query**

```graphql
mutation UpdateWatchlist(
  $idOrUrn: String!
  $watchlistInput: CompanyWatchlistUpdateInput!
) {
  updateCompanyWatchlist(idOrUrn: $idOrUrn, watchlistInput: $watchlistInput) {
    id
    entityUrn
    name
    sharedWithTeam
    userWatchlistType
    __typename
  }
}
```

**GraphQL variables**

```json
{
  "idOrUrn": "971dec3d-150d-4217-902b-b000000000",
  "watchlistInput": {
    "sharedWithTeam": true
  }
}
```

### Add companies to list

Pass the id or urn of a list in the URL and a list of company ids or urns in the body.

ID example:

```
POST https://api.harmonic.ai/watchlists/companies/780c2910-b21d-4ad2-ba04-c98ac939dbd8:addCompanies
```

URN example:

```
POST https://api.harmonic.ai/watchlists/companies/urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8:addCompanies
```

**POST** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}:addCompanies`

| Name | Type | Description |
| --- | --- | --- |
| `ids` | array[company id] | Example: { "ids": [891, 123] } |
| `urns` | array[company urn] | Example: { "urns": ["urn:harmonic:company:22","urn:harmonic:company:1690"] } |

##### Example request

Provide either `ids` or `urns` (you can include both).

```json
{
  "ids": [891, 123],
  "urns": ["urn:harmonic:company:22", "urn:harmonic:company:1690"]
}
```

**GraphQL query**

```graphql
mutation AddCompaniesToWatchlistWithIds(
  $watchlist: String!
  $companies: [String]!
) {
  addCompaniesToWatchlistWithIds(id: $watchlist, companies: $companies) {
    owner {
        ... on User {
          entityUrn
          email
          name
          customer {
            name
            identifier
          }
        }
        ... on Customer {
          entityUrn
          name
          identifier
        }
    }
    id
    entityUrn
    name
    sharedWithTeam
    companyEntries {
      edges {
        node {
          entryUrn
          company {
            entityUrn
            name
            id
            logoUrl
            website {
              url
              domain
            }
            location {
              city
              country
            }
            headcount
            funding {
              fundingTotal
              lastFundingType
              lastFundingAt
            }
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
    }
  }
}
```

**GraphQL variables**

```json
{"watchlist": "780c2910-b21d-4ad2-ba04-c98ac939dbd8", "companies": ["1"]}
```

### Remove companies from list

Pass the id or urn of a list in the URL and a list of company ids or urns in the body to remove those companies from the list.

ID example:

```
POST https://api.harmonic.ai/watchlists/companies/780c2910-b21d-4ad2-ba04-c98ac939dbd8:removeCompanies
```

URN example:

```
POST https://api.harmonic.ai/watchlists/companies/urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8:removeCompanies
```

**POST** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}:removeCompanies`

| Name | Type | Description |
| --- | --- | --- |
| `ids` | array[company id] | Example: { "ids": [891, 123] } |
| `urns` | array[company urn] | Example: { "urns": ["urn:harmonic:company:22","urn:harmonic:company:1690"] } |

##### Example request

Provide either `ids` or `urns` (you can include both).

```json
{
  "ids": [891, 123],
  "urns": ["urn:harmonic:company:22", "urn:harmonic:company:1690"]
}
```

### Delete a list

Pass the id or urn of a list to delete.

ID example:

```
DELETE https://api.harmonic.ai/watchlists/companies/780c2910-b21d-4ad2-ba04-c98ac939dbd8
```

URN example:

```
DELETE https://api.harmonic.ai/watchlists/companies/urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8
```

**DELETE** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}`

### Upsert named view

Create or update a named view for a company list. Named views allow you to customize how you view your list data, including which columns are visible and display type (grid or kanban).

If you provide a named view URN as a query parameter, the existing named view will be updated. If you omit it, a new named view will be created.

Example with named view URN: `POST https://api.harmonic.ai/watchlists/companies/00000000-0000-0000-0000-000000000001/named_views?named_view_urn=urn:harmonic:company_list_named_view:1`

**POST** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/named_views`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Name of the named view |
| `display_type` | string | Options: "GRID" or "KANBAN" |
| `visible_columns` | array[string] | Array of column URNs to display |
| `hide_empty_columns` | boolean | Whether to hide columns with no data |
| `group_by_field` | string | URN of the field to group by (for kanban view) |

##### Example request

```json
{
  "name": "My Custom View",
  "display_type": "GRID",
  "visible_columns": [
    "urn:harmonic:company_field:company_description",
    "urn:harmonic:company_field:company_website_url",
    "urn:harmonic:company_field:company_team",
    "urn:harmonic:company_field:company_funding_total"
  ],
  "hide_empty_columns": false,
  "group_by_field": null
}
```

**GraphQL query**

```graphql
mutation UpsertCompanyWatchlistNamedView($watchlistUrn: CompanyWatchlistUrn!, $namedViewUrn: CompanyListNamedViewUrn, $namedViewInput: CompanyListNamedViewUpsertInput!) {
  upsertCompanyListNamedView(
    watchlistUrn: $watchlistUrn
    namedViewUrn: $namedViewUrn
    namedViewInput: $namedViewInput
  ) {
    id
    entityUrn
    name
    visibleColumns
    searchQuery
    displayType
    hideEmptyColumns
    groupByField {
      urn
      __typename
    }
    __typename
  }
}
```

**GraphQL variables**

```json
{
  "watchlistUrn": "urn:harmonic:company_watchlist:00000000-0000-0000-0000-000000000001",
  "namedViewUrn": "urn:harmonic:company_list_named_view:1",
  "namedViewInput": {
    "name": "My Custom View",
    "displayType": "GRID",
    "visibleColumns": [
      "urn:harmonic:company_field:company_name",
      "urn:harmonic:company_field:company_description"
    ],
    "hideEmptyColumns": false
  }
}
```

### Create custom field

Create a custom field for a company list.

**Note:** This API only works for Shared lists.

**POST** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Name of the custom field |
| `type` | string | One of: TEXT, NUMBER, DATE, SINGLE_SELECT, MULTI_SELECT, PERSON, WEBSITE, CHECKBOX, STATUS |
| `metadata` | object | Optional metadata for the field. Structure depends on field type. |

##### Example request

```json
{
  "name": "Deal Status",
  "type": "SINGLE_SELECT",
  "metadata": {
    "options": [
      { "name": "In Progress", "color": "#FF0000", "default": true },
      { "name": "Closed", "color": "#00FF00", "default": false }
    ]
  }
}
```

##### Metadata shape by field type

For `SINGLE_SELECT` / `MULTI_SELECT` / `STATUS`:

```
{
  "options": [
    {
      "name": "Option Name",
      "color": "#HEX_COLOR",
      "default": false
    }
  ]
}
```

For `NUMBER`:

```
{
  "format": "NUMBER" | "PERCENT" | "US_DOLLAR"
}
```

For `DATE`:

```
{
  "format": "MM_DD_YYYY" | "DD_MM_YYYY" | "YYYY_MM_DD"
}
```

For `PERSON`:

```
{
  "mode": "SINGLE" | "MULTIPLE"
}
```

**GraphQL query**

```graphql
mutation CreateCompanyWatchlistCustomField($customFieldInput: CompanyListCustomFieldCreateInput!, $urn: CompanyWatchlistUrn!) {
  createCompanyWatchlistCustomField(customFieldInput: $customFieldInput, urn: $urn) {
    createdAt
    updatedAt
    urn
    name
    type
    metadata {
      ... on SelectListCustomFieldMetadata {
        options {
          urn
          name
          color
        }
        default
      }
      ... on NumberListCustomFieldMetadata {
        numberFormat: format
      }
      ... on DateListCustomFieldMetadata {
        dateFormat: format
      }
      ... on PersonListCustomFieldMetadata {
        personMode: mode
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "customFieldInput": {
    "name": "Deal Status",
    "type": "SINGLE_SELECT",
    "selectMetadata": {
      "options": [
        {
          "name": "In Progress",
          "color": "#FF0000",
          "default": false
        }
      ]
    }
  },
  "urn": "urn:harmonic:company_watchlist:456"
}
```

### Update custom field

Update a custom field's name or metadata.

**Note:** This API only works for Shared lists.

**PUT** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `custom_field_urn` * | string | (Query Parameter) URN of the custom field to update |
| `name` | string | (Body Parameter) New name for the custom field |
| `metadata` | object | (Body Parameter) Optional metadata for the field. |

`custom_field_urn` is a query parameter; `name` and `metadata` are the request body.

##### Example request

```
PUT https://api.harmonic.ai/watchlists/companies/{id_or_urn}/custom_field?custom_field_urn=urn:harmonic:company_list_custom_field:123
```

Request body:

```json
{
  "name": "Updated Deal Status",
  "metadata": {
    "options": [
      { "name": "Updated Option", "color": "#00FF00", "default": false }
    ]
  }
}
```

##### Metadata shape by field type

For `SINGLE_SELECT` / `MULTI_SELECT` / `STATUS`:

```
{
  "options": [
    {
      "name": "Option Name",
      "color": "#HEX_COLOR",
      "default": false
    }
  ]
}
```

For `NUMBER`:

```
{
  "format": "NUMBER" | "PERCENT" | "US_DOLLAR"
}
```

For `DATE`:

```
{
  "format": "MM_DD_YYYY" | "DD_MM_YYYY" | "YYYY_MM_DD"
}
```

For `PERSON`:

```
{
  "mode": "SINGLE" | "MULTIPLE"
}
```

**GraphQL query**

```graphql
mutation UpdateCompanyWatchlistCustomField(
  $customFieldInput: CompanyListCustomFieldUpdateInput!,
  $customFieldUrn: CompanyListCustomFieldUrn!,
  $watchlistUrn: CompanyWatchlistUrn!
) {
  updateCompanyWatchlistCustomField(
    customFieldInput: $customFieldInput,
    customFieldUrn: $customFieldUrn,
    watchlistUrn: $watchlistUrn
  ) {
    createdAt
    updatedAt
    urn
    name
    type
    metadata {
      ... on SelectListCustomFieldMetadata {
        options {
          urn
          name
          color
        }
        default
      }
      ... on NumberListCustomFieldMetadata {
        numberFormat: format
      }
      ... on DateListCustomFieldMetadata {
        dateFormat: format
      }
      ... on PersonListCustomFieldMetadata {
        personMode: mode
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "customFieldInput": {
    "name": "Updated Deal Status",
    "selectMetadata": {
      "options": [
        {
          "name": "Updated Option",
          "color": "#00FF00",
          "urn": "urn:harmonic:select_list_custom_field_value_option:59345096-35a0-4af2-88bf-c627f8b240f3"
        }
      ]
    }
  },
  "customFieldUrn": "urn:harmonic:company_list_custom_field:123",
  "watchlistUrn": "urn:harmonic:company_watchlist:59345096-35a0-4af2-88bf-c627f8b240f3"
}
```

### Delete custom field

Delete a custom field from a company list.

**Note:** This API only works for Shared lists.

**DELETE** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `custom_field_urn` * | string | URN of the custom field to delete |

**GraphQL query**

```graphql
mutation RemoveCompanyWatchlistCustomField($customFieldUrn: CompanyListCustomFieldUrn!, $watchlistUrn: CompanyWatchlistUrn!) {
  removeCompanyWatchlistCustomField(customFieldUrn: $customFieldUrn, watchlistUrn: $watchlistUrn) {
    urn
  }
}
```

**GraphQL variables**

```json
{
  "customFieldUrn": "urn:harmonic:company_list_custom_field:123",
  "watchlistUrn": "urn:harmonic:company_watchlist:456"
}
```

### Upsert list entries

Create or update entries in a company list. You can add companies and set their custom field values in a single operation.

**POST** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/entries`

| Name | Type | Description |
| --- | --- | --- |
| `entries` | array[object] | Array of entries to create or update. Each entry must have either company_urn or canonical identifiers. |

##### Example request

Provide either `company_urn` or `canonical` identifiers (`website_url`, `crunchbase_url`, `pitchbook_url`, or `linkedin_url`); `values` is optional and each value's format depends on the field type (see below).

```json
{
  "entries": [
    {
      "company_urn": "urn:harmonic:company:123",
      "values": [
        {
          "custom_field_urn": "urn:harmonic:company_list_custom_field:456",
          "data": { "value": "In Progress" }
        }
      ]
    },
    {
      "canonical": { "website_url": "example.com" }
    }
  ]
}
```

##### Value formats by field type

```
TEXT: { "value": "string" }
NUMBER: { "value": number }
DATE: { "value": "YYYY-MM-DD" }
SINGLE_SELECT: { "value": "urn:harmonic:select_list_custom_field_value_option:789" }
MULTI_SELECT: { "value": ["urn:harmonic:select_list_custom_field_value_option:789"] }
PERSON: { "value": ["urn:harmonic:user:123"] } or { "value": ["max@harmonic.ai"] }
WEBSITE: { "value": "https://example.com" }
CHECKBOX: { "value": true }
STATUS: { "value": "urn:harmonic:select_list_custom_field_value_option:789" }
```

**GraphQL query**

```graphql
mutation UpsertCompanyWatchlistEntries(
  $upsertEntriesInput: [CompanyListUpsertEntriesInput!]!,
  $watchlistUrn: CompanyWatchlistUrn!
) {
  upsertCompanyWatchlistEntries(
    upsertEntriesInput: $upsertEntriesInput,
    watchlistUrn: $watchlistUrn
  ) {
    companiesFoundCount
    companiesInvalidCount
    companiesNotFoundCount
    totalCompaniesCount
    userCompaniesImportUrn
  }
}
```

**GraphQL variables**

```json
{
  "upsertEntriesInput": [
    {
      "companyUrn": "urn:harmonic:company:123",
      "customFieldValues": [
        {
          "customFieldUrn": "urn:harmonic:company_list_custom_field:456",
          "customFieldValueInput": {
            "selectData": {
              "value": "urn:harmonic:select_list_custom_field_value_option:789"
            }
          }
        }
      ]
    }
  ],
  "watchlistUrn": "urn:harmonic:company_watchlist:789"
}
```

### Get list entries

Get entries from a company list with their custom field values.

**GET** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/entries`

| Name | Type | Description |
| --- | --- | --- |
| `page` | integer | Page number (starts at 0) |
| `sort_field` | string | Field to sort entries by. Examples: company_id, company_entry_created_at |
| `size` | integer | Number of entries per page (default 50, max 1000) |

**GraphQL query**

```graphql
query GetWatchlistWithCompanies(
  $idOrUrn: String!
  $page: Int
  $size: Int
  $first: Int
  $after: String
  $sortField: String
  $sortDescending: Boolean
) {
  getCompanyWatchlistByIdOrUrn(idOrUrn: $idOrUrn) {
    id
    companyEntries(
      page: $page
      size: $size
      first: $first
      after: $after
      sortField: $sortField
      sortDescending: $sortDescending
    ) {
      __typename
      edges {
        cursor
        node {
          entryCreatedAt
          entryUrn
          customFieldValues {
            createdAt
            updatedAt
            urn
            data {
              ... on NumberListCustomFieldValue {
                numberValue: value
              }
              ... on SingleSelectCustomFieldValue {
                singleSelectValue: value
              }
            }
            customField {
              urn
              name
              type
            }
          }
          company {
                      companyType
          contact {
            emails
            phoneNumbers
          }
          description
          entityUrn
          foundingDate {
            date
            granularity
          }
          funding {
            fundingTotal
            numFundingRounds
            lastFundingAt
            lastFundingType
            lastFundingTotal
            investors {
              ... on Company {
                name
              }
              ... on Person {
                fullName
              }
            }
            fundingRounds {
              entityUrn
              announcementDate
              fundingRoundType
              fundingAmount
              fundingCurrency
              sourceUrl
              postMoneyValuation
              investors {
                investorName
                isLead
                entityUrn
              }
            }
          }
          websiteDomainAliases
          nameAliases
          fundingAttributeNullStatus
          id
          logoUrl
          legalName
          name
          ownershipStatus
          headcount
          stage
          highlights {
            text
            category
          }
          numNotableFollowers
          notableFollowers(first: 2) {
            followerName
            followerUrn
            firmName
            firmUrn
            followedName
            followedUrn
            followObservedAt
          }
          initializedDate
          location {
            country
            zip
            state
            city
            street
            location
            addressFormatted
          }
          employees {
            entityUrn
            fullName
            firstName
            lastName
            profilePictureUrl
            contact {
              phoneNumbers
              emails
            }
            location {
              country
              zip
              state
              city
              street
              location
              addressFormatted
            }
            education {
              endDate
              startDate
              grade
              field
              degree
              school {
                name
                websiteUrl
                linkedinUrl
                logoUrl
                entityUrn
              }
            }
            experience {
              location
              isCurrentPosition
              endDate
              startDate
              description
              title
              department
              contact {
                emails
                phoneNumbers
              }
            }
            awardsBeta
            recommendationsBeta
          }
          snapshots {
            name
          }
          socials {
             facebook {
              url
              followerCount
             }
             twitter {
              followerCount
              url
             }
             linkedin {
              followerCount
              url
             }
             instagram {
              followerCount
              url
             }
             crunchbase {
              url
              followerCount
             }
             pitchbook {
              followerCount
              url
             }
             angellist {
              followerCount
              url
             }
             indeed {
              followerCount
              url
             }
             youtube {
              followerCount
              url
             }
             monster {
              followerCount
              url
             }
             stackoverflow {
              url
              followerCount
             }
          }
          website {
            isBroken
            domain
            url
          }
          tags {
            type
            displayValue
            entityUrn
            dateAdded
          }
          userConnections {
            user {
              email
              name
            }
          }
          tractionMetrics {
            headcount {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            webTraffic {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountAdvisor {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountCustomerSuccess {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountMarketing {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountOther {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountProduct {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountSales {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountSupport {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountData {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountDesign {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountEngineering {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountFinance {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountOperations {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountLegal {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            headcountPeople {
              ago14d {
                value
                change
                percentChange
              }
              ago30d {
                value
              }
              ago90d {
                value
              }
              ago180d {
                value
              }
              ago365d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            facebookFollowerCount {
              ago14d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            linkedinFollowerCount {
              ago14d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            instagramFollowerCount {
              ago14d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
            twitterFollowerCount {
              ago14d {
                value
              }
              metrics {
                timestamp
                metricValue
              }
              latestMetricValue
            }
          }
          relatedCompanies {
            priorStealthAssociation {
              emergenceDate
              previouslyKnownAs
            }
          }
          }
        }
      }
      totalCount
      pageInfo {
        hasNextPage
        startCursor
        endCursor
      }
    }
  }
}
```

**GraphQL variables**

```json
{"idOrUrn": "urn:harmonic:company_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8"}
```

### Delete list entries

Remove entries from a company list. You can specify companies by URN or canonical identifiers.

**POST** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/entries:batchDelete`

| Name | Type | Description |
| --- | --- | --- |
| `entries` | array[object] | Array of entries to delete. Each entry must have either company_urn or canonical identifiers. |

##### Example request

```json
{
  "entries": [
    { "company_urn": "urn:harmonic:company:123" },
    {
      "canonical": {
        "website_url": "example.com",
        "linkedin_url": "https://linkedin.com/company/example"
      }
    }
  ]
}
```

##### Entry shape

Provide either `company_urn` or `canonical` identifiers.

```json
{
  "company_urn": "urn:harmonic:company:123",
  "canonical": {
    "website_url": "example.com",
    "linkedin_url": "https://linkedin.com/company/example"
  }
}
```

**GraphQL query**

```graphql
mutation RemoveCompanyEntriesFromWatchlist(
  $input: DeleteCompanyEntriesFromWatchlistInput!,
  $watchlistUrn: CompanyWatchlistUrn!
) {
  removeCompanyEntriesFromWatchlist(
    input: $input,
    watchlistUrn: $watchlistUrn
  ) {
    urns
  }
}
```

**GraphQL variables**

```json
{
  "input": {
    "urns": ["urn:harmonic:company:123"]
  },
  "watchlistUrn": "urn:harmonic:company_watchlist:789"
}
```

### Get import details

Get details about a specific import operation, including success/failure counts and status.

**GET** `https://api.harmonic.ai/watchlists/companies/imports/{id_or_urn}`

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/companies/imports/{id_or_urn}`

```json
{
  "entity_urn": "urn:harmonic:user_companies_import:123",
  "found_imports_count": 5,
  "failed_imports_count": 1,
  "total_imports_count": 6
}
```

**GraphQL query**

```graphql
query GetUserCompaniesImport($idOrUrn: String!) {
  getUserCompaniesImportByIdOrUrn(idOrUrn: $idOrUrn) {
    createdAt
    entityUrn
    id
    companyListId
    customerId
    customerUrn
    userId
    userUrn
    fileName
    flatfileBatchId
    foundImportsCount
    failedImportsCount
    pendingImportsCount
    totalImportsCount
  }
}
```

**GraphQL variables**

```json
{
  "idOrUrn": "urn:harmonic:user_companies_import:123"
}
```

### Get import entries

Get the entries (companies) from a specific import operation. You can filter by status (pending, success, failed) and paginate results.

**GET** `https://api.harmonic.ai/watchlists/companies/imports/{id_or_urn}/entries`

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/companies/imports/{id_or_urn}/entries`

```json
{
  "entries": [
    {
      "id": "123",
      "matched_company_urn": "urn:harmonic:company:456",
      "error_code": null
    }
  ],
  "total_count": 1
}
```

**GraphQL query**

```graphql
query GetUserCompaniesImportEntries(
  $idOrUrn: String!
  $status: String
  $page: Int!
  $size: Int!
) {
  getUserCompaniesImportByIdOrUrn(idOrUrn: $idOrUrn) {
    pendingImports(page: $page, size: $size) {
      id
      canonicals {
        websiteUrl
        linkedinUrl
        crunchbaseUrl
        pitchbookUrl
      }
      matchedCompany {
        entityUrn
        name
        website {
          url
        }
      }
      matchedCompanyUrn
      errorCode
    }
    foundImports(page: $page, size: $size) {
      id
      canonicals {
        websiteUrl
        linkedinUrl
        crunchbaseUrl
        pitchbookUrl
      }
      matchedCompany {
        entityUrn
        name
        website {
          url
        }
      }
      matchedCompanyUrn
      errorCode
    }
    failedImports(page: $page, size: $size) {
      id
      canonicals {
        websiteUrl
        linkedinUrl
        crunchbaseUrl
        pitchbookUrl
      }
      matchedCompany {
        entityUrn
        name
        website {
          url
        }
      }
      matchedCompanyUrn
      errorCode
    }
  }
}
```

**GraphQL variables**

```json
{
  "idOrUrn": "urn:harmonic:user_companies_import:123",
  "status": "SUCCESS",
  "page": 0,
  "size": 100
}
```

### Get list imports

Get all import operations for a specific company list. Results are paginated.

**GET** `https://api.harmonic.ai/watchlists/companies/{id_or_urn}/imports`

| Name | Type | Description |
| --- | --- | --- |
| `page` | integer | Page number (starts at 0) |
| `size` | integer | Number of imports per page (default 100, max 1000) |

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/companies/{id_or_urn}/imports`

```json
{
  "imports": [
    {
      "entity_urn": "urn:harmonic:user_companies_import:123",
      "found_imports_count": 5,
      "total_imports_count": 6
    }
  ],
  "total_count": 1
}
```

**GraphQL query**

```graphql
query GetUserCompaniesImports(
  $companiesListIdOrUrn: String!
  $page: Int!
  $size: Int!
) {
  getUserCompaniesImportsByCompaniesListUrnOrId(
    companiesListIdOrUrn: $companiesListIdOrUrn
    page: $page
    size: $size
  ) {
    imports {
      createdAt
      entityUrn
      id
      companyListId
      customerId
      customerUrn
      userId
      userUrn
      fileName
      flatfileBatchId
      foundImportsCount
      failedImportsCount
      pendingImportsCount
      totalImportsCount
    }
    totalCount
  }
}
```

**GraphQL variables**

```json
{
  "companiesListIdOrUrn": "urn:harmonic:company_watchlist:456",
  "page": 0,
  "size": 100
}
```

## People lists

Create, update, and manage people lists and their entries.

### Get all people lists

Get all people lists accessible to your account.

**GET** `https://api.harmonic.ai/watchlists/people`

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/people`

```json
[
{
    "name": "string",
    "owner": "urn:harmonic:user:123456",
    "shared_with_team": true,
    "entity_urn": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8",
    "people": [],
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "custom_fields": [
      {
        "name": "Priority",
        "type": "NUMBER"
      }
    ],
    "named_views": [
      {
        "name": "My Custom View",
        "display_type": "GRID"
      }
    ]
}
]
```

**GraphQL query**

```graphql
query Query {
  getPeopleWatchlistsForTeam {
    name
    entityUrn
    id
    owner {
      ... on User {
        entityUrn
        email
        name
        customer {
          name
          identifier
        }
      }
      ... on Customer {
        entityUrn
        name
        identifier
      }
    }
    sharedWithTeam
  }
}
```

### Get a people list

Pass the id or urn of a list to get data.

ID example:

```
GET https://api.harmonic.ai/watchlists/people/780c2910-b21d-4ad2-ba04-c98ac939dbd8
```

URN example:

```
GET https://api.harmonic.ai/watchlists/people/urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8
```

**GET** `https://api.harmonic.ai/watchlists/people/{id_or_urn}`

To learn more about switching to cursor pagination, read about [pagination query parameters here](/docs/api-reference/introduction#pagination).

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/people/{id_or_urn}`

```json
{
    "name": "string",
    "owner": "urn:harmonic:user:123456",
    "shared_with_team": true,
    "entity_urn": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8",
    "people": [],
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "custom_fields": [
      {
        "name": "Priority",
        "type": "NUMBER"
      }
    ],
    "named_views": [
      {
        "name": "My Custom View",
        "display_type": "GRID"
      }
    ]
}
```

**GraphQL query**

```graphql
query GetPeopleInWatchlistByIdOrUrn($idOrUrn: String!) {
  getPeopleInWatchlistByIdOrUrn(idOrUrn: $idOrUrn) {
    edges {
      node {
        ... on Person {
                    fullName
          firstName
          lastName
          profilePictureUrl
          linkedinHeadline
          contact {
            emails
            phoneNumbers
          }
          location {
            addressFormatted
            location
            street
            city
            state
            zip
            country
          }
          education {
            school {
              name
              websiteUrl
              linkedinUrl
              logoUrl
              entityUrn
            }
            degree
            field
            grade
            startDate
            endDate
          }
          experience {
            location
            isCurrentPosition
            endDate
            startDate
            description
            title
            department
            contact {
              emails
              phoneNumbers
            }
            company {
              name
              funding {
                fundingTotal
              }
              foundingDate {
                date
              }
              socials {
                linkedin {
                  url
                }
              }
            }
          }
          numNotableFollowers
          notableFollowers(first: 2) {
            followerName
            followerUrn
            firmName
            firmUrn
            followedName
            followedUrn
            followObservedAt
          }
          awardsBeta
          recommendationsBeta
          currentCompanyUrns
          entityUrn
          socials {
             facebook {
              url
              followerCount
             }
             twitter {
              followerCount
              url
             }
             linkedin {
              followerCount
              url
             }
             instagram {
              followerCount
              url
             }
             crunchbase {
              url
              followerCount
             }
             pitchbook {
              followerCount
              url
             }
             angellist {
              followerCount
              url
             }
             indeed {
              followerCount
              url
             }
             youtube {
              followerCount
              url
             }
             monster {
              followerCount
              url
             }
             stackoverflow {
              url
              followerCount
             }
          }
          recentJobUpdateStatus {
            date
            helperText
            type
          }
          linkedinProfileVisibilityType
          lastRefreshedAt
          lastCheckedAt
          languages {
            name
          }
        }
      }
    }
    totalCount
  }
}
```

**GraphQL variables**

```json
{"idOrUrn": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8"}
```

### Get people list entries

Pass the id or urn of a list to get entries.

ID example:

```
GET https://api.harmonic.ai/watchlists/people/780c2910-b21d-4ad2-ba04-c98ac939dbd8/entries
```

URN example:

```
GET https://api.harmonic.ai/watchlists/people/urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8/entries
```

**GET** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/entries`

| Name | Type | Description |
| --- | --- | --- |
| `sort_field` | string | Examples: person_id, person_entry_created_at |
| `sort_descending` | boolean | Sort direction |

To learn more about switching to cursor pagination, read about [pagination query parameters here](/docs/api-reference/introduction#pagination).

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/people/{id_or_urn}/entries`

```json
{
    "entries": [...],
    "page_info": {
      "next": "Wzc1MjAwXQ==",
      "current": null,
      "has_next": true
    },
    "total_count": 1
}
```

**GraphQL query**

```graphql
query GetWatchlistWithPeople(
  $idOrUrn: String!
  $page: Int
  $size: Int
  $first: Int
  $after: String
  $sortField: String
  $sortDescending: Boolean
) {
  getPeopleWatchlistByIdOrUrn(idOrUrn: $idOrUrn) {
    id
    personEntries(
      page: $page
      size: $size
      first: $first
      after: $after
      sortField: $sortField
      sortDescending: $sortDescending
    ) {
      __typename
      edges {
        cursor
        node {
         entryCreatedAt
         entryUrn
         customFieldValues {
           createdAt
           updatedAt
           urn
           data {
             ... on NumberListCustomFieldValue {
               value
             }
             ... on SingleSelectCustomFieldValue {
               value
             }
           }
           customField {
             urn
             name
             type
           }
         }
         company {
                   fullName
          firstName
          lastName
          profilePictureUrl
          linkedinHeadline
          contact {
            emails
            phoneNumbers
          }
          location {
            addressFormatted
            location
            street
            city
            state
            zip
            country
          }
          education {
            school {
              name
              websiteUrl
              linkedinUrl
              logoUrl
              entityUrn
            }
            degree
            field
            grade
            startDate
            endDate
          }
          experience {
            location
            isCurrentPosition
            endDate
            startDate
            description
            title
            department
            contact {
              emails
              phoneNumbers
            }
            company {
              name
              funding {
                fundingTotal
              }
              foundingDate {
                date
              }
              socials {
                linkedin {
                  url
                }
              }
            }
          }
          numNotableFollowers
          notableFollowers(first: 2) {
            followerName
            followerUrn
            firmName
            firmUrn
            followedName
            followedUrn
            followObservedAt
          }
          awardsBeta
          recommendationsBeta
          currentCompanyUrns
          entityUrn
          socials {
             facebook {
              url
              followerCount
             }
             twitter {
              followerCount
              url
             }
             linkedin {
              followerCount
              url
             }
             instagram {
              followerCount
              url
             }
             crunchbase {
              url
              followerCount
             }
             pitchbook {
              followerCount
              url
             }
             angellist {
              followerCount
              url
             }
             indeed {
              followerCount
              url
             }
             youtube {
              followerCount
              url
             }
             monster {
              followerCount
              url
             }
             stackoverflow {
              url
              followerCount
             }
          }
          recentJobUpdateStatus {
            date
            helperText
            type
          }
          linkedinProfileVisibilityType
          lastRefreshedAt
          lastCheckedAt
          languages {
            name
          }
          }
        }
      }
      totalCount
      pageInfo {
        hasNextPage
        startCursor
        endCursor
      }
    }
  }
}
```

**GraphQL variables**

```json
{"idOrUrn": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8"}
```

### Create new people list

In the body, pass the name, if it's shared with team, and a list of people.

**POST** `https://api.harmonic.ai/watchlists/people`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Example: { "name": "My Watchlist" } |
| `shared_with_team` | boolean | **true**: your team will be able to see this list on console. **false**: list only accessible via API. Example: { "shared_with_team": true } |
| `people` | array[person urn] | The ids or urns of people you want. Can be empty. Example 1: { "people": ["urn:harmonic:person:22","urn:harmonic:person:1690"] }; Example 2: { "people": ["22","1690"] }; Example 3: { "people": [] } |

##### Example request

```json
{
  "name": "My Watchlist",
  "shared_with_team": true,
  "people": ["urn:harmonic:person:22", "urn:harmonic:person:1690"]
}
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/watchlists/people`

```json
{
    "urn": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c000000000000",
}
```

**GraphQL query**

```graphql
mutation CreatePeopleWatchlist($watchlistInput: PeopleWatchlistInput!) {
  createPeopleWatchlist(watchlistInput: $watchlistInput) {
    id
    entityUrn
    name
    sharedWithTeam
    userWatchlistType
    owner {
      ... on User {
        name
        entityUrn
        __typename
      }
      ... on Customer {
        name
        identifier
        __typename
      }
      __typename
    }
  }
}
```

**GraphQL variables**

```json
{
  "watchlistInput": {
    "name": "My People Watchlist",
    "sharedWithTeam": true
  }
}
```

### Update people list

To update name or if list is shared with team.

**PUT** `https://api.harmonic.ai/watchlists/people/{id_or_urn}`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | New name for the list |
| `shared_with_team` | boolean | true: visible on console. false: API only. |

##### Example request

```json
{
  "name": "Renamed list",
  "shared_with_team": true
}
```

**REST**

`PUT https://api.harmonic.ai/watchlists/people/{id_or_urn}`

```json
{
    "urn": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c000000000000",
}
```

### Add people to list

Pass the id or urn of a people list in the URL and a list of person ids or urns in the body to add those people to the list.

ID example:

```
POST https://api.harmonic.ai/watchlists/people/780c2910-b21d-4ad2-ba04-c98ac939dbd8:addPeople
```

URN example:

```
POST https://api.harmonic.ai/watchlists/people/urn:harmonic:person_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8:addPeople
```

**POST** `https://api.harmonic.ai/watchlists/people/{id_or_urn}:addPeople`

| Name | Type | Description |
| --- | --- | --- |
| `ids` | array[person id] | Example: { "ids": [891, 123], "urns": [] } |
| `urns` | array[person urn] | Example: { "ids": [], "urns": ["urn:harmonic:person:22","urn:harmonic:person:1690"] } |

##### Example request

Provide either `ids` or `urns` (you can include both).

```json
{
  "ids": [891, 123],
  "urns": ["urn:harmonic:person:22", "urn:harmonic:person:1690"]
}
```

**GraphQL query**

```graphql
mutation AddPeopleToWatchlistWithIds(
  $watchlist: String!
  $people: [String]!
) {
  addPeopleToWatchlistWithIds(id: $watchlist, people: $people) {
    owner {
        ... on User {
          entityUrn
          email
          name
          customer {
            name
            identifier
          }
        }
        ... on Customer {
          entityUrn
          name
          identifier
        }
    }
    id
    entityUrn
    name
    sharedWithTeam
    personEntries {
      edges {
        node {
          entryUrn
          person {
            entityUrn
            fullName
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount
    }
  }
}
```

**GraphQL variables**

```json
{"watchlist": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8", "people": [123456]}
```

### Remove people from list

Pass the id or urn of a list in the URL and a list of people ids or urns in the body to remove those people from the list.

ID example:

```
POST https://api.harmonic.ai/watchlists/people/780c2910-b21d-4ad2-ba04-c98ac939dbd8:removePeople
```

URN example:

```
POST https://api.harmonic.ai/watchlists/people/urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8:removePeople
```

**POST** `https://api.harmonic.ai/watchlists/people/{id_or_urn}:removePeople`

| Name | Type | Description |
| --- | --- | --- |
| `ids` | array[person id] | Example: { "ids": [891, 123], "urns": [] } |
| `urns` | array[person urn] | Example: { "ids": [], "urns": ["urn:harmonic:person:22","urn:harmonic:person:1690"] } |

##### Example request

Provide either `ids` or `urns` (you can include both).

```json
{
  "ids": [891, 123],
  "urns": ["urn:harmonic:person:22", "urn:harmonic:person:1690"]
}
```

**GraphQL query**

```graphql
mutation RemovePeopleFromWatchlistWithIds(
  $watchlist: String!
  $people: [String]!
) {
  removePeopleFromWatchlistWithIds(id: $watchlist, people: $people) {
    owner {
      ... on User {
        entityUrn
        email
      }
      ... on Customer {
        entityUrn
        identifier
      }
    }
    owner {
      ... on User {
        entityUrn
        email
      }
      ... on Customer {
        entityUrn
        identifier
      }
    }
    id
    entityUrn
    name
    sharedWithTeam
  }
}
```

**GraphQL variables**

```json
{"watchlist": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8", "people": [123456]}
```

### Delete a list

Pass the id or urn of a list to delete.

ID example:

```
DELETE https://api.harmonic.ai/watchlists/people/780c2910-b21d-4ad2-ba04-c98ac939dbd8
```

URN example:

```
DELETE https://api.harmonic.ai/watchlists/people/urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8
```

**DELETE** `https://api.harmonic.ai/watchlists/people/{id_or_urn}`

### Upsert named view

Create or update a named view for a people list. Named views allow you to customize how you view your list data, including which columns are visible and display type (grid or kanban).

If you provide a named view URN as a query parameter, the existing named view will be updated. If you omit it, a new named view will be created.

Example with named view URN: `POST https://api.harmonic.ai/watchlists/people/00000000-0000-0000-0000-000000000001/named_views?named_view_urn=urn:harmonic:person_list_named_view:1`

**POST** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/named_views`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Name of the named view |
| `display_type` | string | Display type of the view. Options: "GRID" or "KANBAN" |
| `visible_columns` | array[string] | Array of column URNs to display, you can find a full list of available columns and their URNs [here](https://support.harmonic.ai/en/articles/10657032-company-and-people-lists-api-data-fields). Example: { "visible_columns": ["urn:harmonic:person_field:person_name", "urn:harmonic:person_field:person_lists"] } |
| `hide_empty_columns` | boolean | Whether to hide columns with no data |
| `group_by_field` | string | URN of the field to group by (for kanban view) |

##### Example request

```json
{
  "name": "My Custom View",
  "display_type": "GRID",
  "visible_columns": [
    "urn:harmonic:person_field:person_name",
    "urn:harmonic:person_field:person_lists"
  ],
  "hide_empty_columns": false,
  "group_by_field": null
}
```

### Get all people updates in a list

This query fetches an array of recent updates for individuals within a specified list, using either an ID or URN for identification. Updates are sorted in descending order, with the most recent at the top. The collected updates cover a 7-day window and consist of changes to a person's profile, such as LinkedIn headline changes or job transitions.

**GET** `GraphQL only`

Supported modes: REST, GraphQL

```json
This is supported in the GraphQL API only.
```

**GraphQL query**

```graphql
query GetPeopleInWatchlistByIdOrUrn($idOrUrn: String!) {
  getPeopleInWatchlistByIdOrUrn(idOrUrn: $idOrUrn) {
    edges {
      node {
        ... on Person {
          id
          entityUrn
          updates {
            eventType
            date
            helperText
          }
        }
      }
    }
    totalCount
  }
}
```

**GraphQL variables**

```json
{"idOrUrn": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8"}
```

### Create custom field

Create a new custom field for a people watchlist.

**Note:** This API only works for Shared lists.

**POST** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Name of the custom field |
| `type` | string | Type of the custom field. One of: TEXT, NUMBER, DATE, SINGLE_SELECT, MULTI_SELECT, PERSON, WEBSITE, CHECKBOX, STATUS |
| `metadata` | object | Optional metadata for the field. Structure depends on field type. |

##### Example request

```json
{
  "name": "Deal Status",
  "type": "SINGLE_SELECT",
  "metadata": {
    "options": [
      { "name": "In Progress", "color": "#FF0000", "default": true },
      { "name": "Closed", "color": "#00FF00", "default": false }
    ]
  }
}
```

##### Metadata shape by field type

For `SINGLE_SELECT` / `MULTI_SELECT` / `STATUS`:

```
{
  "options": [
    {
      "name": "Option Name",
      "color": "#HEX_COLOR",
      "default": false
    }
  ]
}
```

For `NUMBER`:

```
{
  "format": "NUMBER" | "PERCENT" | "US_DOLLAR"
}
```

For `DATE`:

```
{
  "format": "MM_DD_YYYY" | "DD_MM_YYYY" | "YYYY_MM_DD"
}
```

For `PERSON`:

```
{
  "mode": "SINGLE" | "MULTIPLE"
}
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/watchlists/people/{id_or_urn}/custom_field`

```json
{
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z",
  "urn": "urn:harmonic:person_list_custom_field:123",
  "list_urn": "urn:harmonic:people_watchlist:456",
  "name": "Priority",
  "type": "SINGLE_SELECT",
  "metadata": {
    "options": [
      { "name": "High", "color": "#FF0000" },
      { "name": "Medium", "color": "#FFA500" },
      { "name": "Low", "color": "#00FF00" }
    ]
  }
}
```

**GraphQL query**

```graphql
mutation CreatePeopleListCustomField($urn: PeopleWatchlistUrn!, $customFieldInput: PeopleListCustomFieldCreateInput!) {
  createPeopleWatchlistCustomField(urn: $urn, customFieldInput: $customFieldInput) {
    urn
    name
    type
    metadata {
      __typename
    }
    createdAt
    updatedAt
  }
}
```

**GraphQL variables**

```json
{
  "urn": "urn:harmonic:people_watchlist:d935db75-d12d-44bd-b0c8-37585e1b523f",
  "customFieldInput": {
    "name": "Priority test",
    "type": "SINGLE_SELECT",
    "selectMetadata": {
      "options": [
        { "name": "High", "color": "#FF0000" },
        { "name": "Medium", "color": "#FFA500" },
        { "name": "Low", "color": "#00FF00" }
      ]
    }
  }
}
```

### Update custom field

Update a custom field's name or metadata.

**Note:** This API only works for Shared lists.

**PUT** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `custom_field_urn` * | string | (Query Parameter) URN of the custom field to update (format: urn:harmonic:person_list_custom_field:<id>) |
| `name` | string | (Body Parameter) New name for the custom field |
| `metadata` | object | (Body Parameter) Optional metadata for the field. Structure depends on field type. |

`custom_field_urn` is a query parameter; `name` and `metadata` are the request body.

##### Example request

```
PUT https://api.harmonic.ai/watchlists/people/{id_or_urn}/custom_field?custom_field_urn=urn:harmonic:person_list_custom_field:123
```

Request body:

```json
{
  "name": "Updated Deal Status",
  "metadata": {
    "options": [
      { "name": "Updated Option", "color": "#00FF00", "default": false }
    ]
  }
}
```

##### Metadata shape by field type

For `SINGLE_SELECT` / `MULTI_SELECT` / `STATUS`:

```
{
  "options": [
    {
      "name": "Option Name",
      "color": "#HEX_COLOR",
      "default": false
    }
  ]
}
```

For `NUMBER`:

```
{
  "format": "NUMBER" | "PERCENT" | "US_DOLLAR"
}
```

For `DATE`:

```
{
  "format": "MM_DD_YYYY" | "DD_MM_YYYY" | "YYYY_MM_DD"
}
```

For `PERSON`:

```
{
  "mode": "SINGLE" | "MULTIPLE"
}
```

Supported modes: REST, GraphQL

**REST**

`PUT https://api.harmonic.ai/watchlists/people/{id_or_urn}/custom_field`

```json
{
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-01-15T13:00:00Z",
  "urn": "urn:harmonic:person_list_custom_field:123",
  "list_urn": "urn:harmonic:people_watchlist:456",
  "name": "High Priority",
  "type": "SINGLE_SELECT",
  "metadata": {
    "options": [
      { "name": "Critical", "color": "#FF0000" },
      { "name": "Important", "color": "#FFA500" },
      { "name": "Normal", "color": "#00FF00" }
    ]
  }
}
```

**GraphQL query**

```graphql
mutation UpdatePeopleListCustomField($urn: PeopleWatchlistUrn!, $customFieldUrn: PeopleListCustomFieldUrn!, $customFieldInput: PeopleListCustomFieldUpdateInput!) {
  updatePeopleWatchlistCustomField(watchlistUrn: $urn, customFieldUrn: $customFieldUrn, customFieldInput: $customFieldInput) {
    urn
    name
    type
    metadata {
      __typename
    }
    updatedAt
  }
}
```

**GraphQL variables**

```json
{
  "urn": "urn:harmonic:people_watchlist:123",
  "customFieldUrn": "urn:harmonic:person_list_custom_field:456",
  "customFieldInput": {
    "name": "High Priority",
    "selectMetadata": {
      "options": [
        { "name": "Critical", "color": "#FF0000" },
        { "name": "Important", "color": "#FFA500" },
        { "name": "Normal", "color": "#00FF00" }
      ]
    }
  }
}
```

### Delete custom field

Delete a custom field from a people list. The custom field URN must be provided as a query parameter.

**Note:** This API only works for Shared lists.

**DELETE** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `custom_field_urn` * | string | URN of the custom field to delete (format: urn:harmonic:person_list_custom_field:<id>) |

Supported modes: REST, GraphQL

**REST**

`DELETE https://api.harmonic.ai/watchlists/people/{id_or_urn}/custom_field`

```json
{
  "urn": "urn:harmonic:person_list_custom_field:123"
}
```

**GraphQL query**

```graphql
mutation DeletePeopleListCustomField($watchlistUrn: PeopleWatchlistUrn!, $customFieldUrn: PeopleListCustomFieldUrn!) {
  removePeopleWatchlistCustomField(
    watchlistUrn: $watchlistUrn
    customFieldUrn: $customFieldUrn
  ) {
    urn
  }
}
```

**GraphQL variables**

```json
{
  "watchlistUrn": "urn:harmonic:people_watchlist:watchlist_ID",
  "customFieldUrn": "urn:harmonic:person_list_custom_field:custom_field_ID"
}
```

### Upsert list entries

Create or update entries in a people list. You can add people and set their custom field values in a single operation.

**POST** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/entries`

| Name | Type | Description |
| --- | --- | --- |
| `entries` | array[object] | Array of entries to create or update. Each entry must have either person_urn or canonical identifiers (linkedin_url or email). |

If you provide a canonical identifier, at least one of `linkedin_url` or `email` must be provided. Harmonic will attempt to match this to a person in our database. We recommend providing a `linkedin_url` when possible for the best results.

##### Example request

Provide either `person_urn` or `canonical` identifiers (`linkedin_url` or `email`); `values` is optional and each value's format depends on the field type (see below).

```json
{
  "entries": [
    {
      "person_urn": "urn:harmonic:person:123",
      "values": [
        {
          "custom_field_urn": "urn:harmonic:person_list_custom_field:456",
          "data": { "value": "In Progress" }
        }
      ]
    },
    {
      "canonical": { "linkedin_url": "https://linkedin.com/in/example" }
    }
  ]
}
```

##### Value formats by field type

```
TEXT: { "value": "string" }
NUMBER: { "value": number }
DATE: { "value": "YYYY-MM-DD" }
SINGLE_SELECT: { "value": "urn:harmonic:select_list_custom_field_value_option:789" }
MULTI_SELECT: { "value": ["urn:harmonic:select_list_custom_field_value_option:789"] }
PERSON: { "value": ["urn:harmonic:user:123"] } or { "value": ["max@harmonic.ai"] }
WEBSITE: { "value": "https://example.com" }
CHECKBOX: { "value": true }
STATUS: { "value": "urn:harmonic:select_list_custom_field_value_option:789" }
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/watchlists/people/{id_or_urn}/entries`

```json
{
  "people_found_count": 1,
  "total_people_count": 1
}
```

**GraphQL query**

```graphql
mutation UpsertPeopleWatchlistEntries(
  $upsertEntriesInput: [PeopleListUpsertEntriesInput!]!,
  $watchlistUrn: PeopleWatchlistUrn!
) {
  upsertPeopleWatchlistEntries(
    upsertEntriesInput: $upsertEntriesInput,
    watchlistUrn: $watchlistUrn
  ) {
    peopleFoundCount
    peopleInvalidCount
    peopleNotFoundCount
    totalPeopleCount
    userPeopleImportUrn
  }
}
```

**GraphQL variables**

```json
{
  "upsertEntriesInput": [
    {
      "personUrn": "urn:harmonic:person:123",
      "canonicals": {
        "linkedinUrl": "https://linkedin.com/in/example",
        "email": "person@example.com"
      },
      "customFieldValues": [
        {
          "customFieldUrn": "urn:harmonic:person_list_custom_field:456",
          "customFieldValueInput": {
            "selectData": {
              "value": "urn:harmonic:select_list_custom_field_value_option:789"
            }
          }
        }
      ]
    }
  ],
  "watchlistUrn": "urn:harmonic:people_watchlist:789"
}
```

### Get list entries

Get entries from a people list with their custom field values.

**GET** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/entries`

| Name | Type | Description |
| --- | --- | --- |
| `page` | integer | Page number (starts at 0) |
| `sort_field` | string | Field to sort entries by. Examples: person_id, person_entry_created_at |
| `size` | integer | Number of entries per page (default 50, max 1000) |
| `cursor` | string | Cursor for pagination |

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/watchlists/people/{id_or_urn}/entries`

```json
{
  "entries": [
    {
      "person_urn": "urn:harmonic:person:123",
      "entry_urn": "urn:harmonic:people_watchlist_entry:789"
    }
  ],
  "total_count": 1
}
```

**GraphQL query**

```graphql
query GetWatchlistWithPeople(
  $idOrUrn: String!
  $page: Int
  $size: Int
  $first: Int
  $after: String
  $sortField: String
  $sortDescending: Boolean
) {
  getPeopleWatchlistByIdOrUrn(idOrUrn: $idOrUrn) {
    id
    personEntries(
      page: $page
      size: $size
      first: $first
      after: $after
      sortField: $sortField
      sortDescending: $sortDescending
    ) {
      __typename
      edges {
        cursor
        node {
         entryCreatedAt
         entryUrn
         customFieldValues {
           createdAt
           updatedAt
           urn
           data {
             ... on NumberListCustomFieldValue {
               value
             }
             ... on SingleSelectCustomFieldValue {
               value
             }
           }
           customField {
             urn
             name
             type
           }
         }
         company {
                   fullName
          firstName
          lastName
          profilePictureUrl
          linkedinHeadline
          contact {
            emails
            phoneNumbers
          }
          location {
            addressFormatted
            location
            street
            city
            state
            zip
            country
          }
          education {
            school {
              name
              websiteUrl
              linkedinUrl
              logoUrl
              entityUrn
            }
            degree
            field
            grade
            startDate
            endDate
          }
          experience {
            location
            isCurrentPosition
            endDate
            startDate
            description
            title
            department
            contact {
              emails
              phoneNumbers
            }
            company {
              name
              funding {
                fundingTotal
              }
              foundingDate {
                date
              }
              socials {
                linkedin {
                  url
                }
              }
            }
          }
          numNotableFollowers
          notableFollowers(first: 2) {
            followerName
            followerUrn
            firmName
            firmUrn
            followedName
            followedUrn
            followObservedAt
          }
          awardsBeta
          recommendationsBeta
          currentCompanyUrns
          entityUrn
          socials {
             facebook {
              url
              followerCount
             }
             twitter {
              followerCount
              url
             }
             linkedin {
              followerCount
              url
             }
             instagram {
              followerCount
              url
             }
             crunchbase {
              url
              followerCount
             }
             pitchbook {
              followerCount
              url
             }
             angellist {
              followerCount
              url
             }
             indeed {
              followerCount
              url
             }
             youtube {
              followerCount
              url
             }
             monster {
              followerCount
              url
             }
             stackoverflow {
              url
              followerCount
             }
          }
          recentJobUpdateStatus {
            date
            helperText
            type
          }
          linkedinProfileVisibilityType
          lastRefreshedAt
          lastCheckedAt
          languages {
            name
          }
          }
        }
      }
      totalCount
      pageInfo {
        hasNextPage
        startCursor
        endCursor
      }
    }
  }
}
```

**GraphQL variables**

```json
{"idOrUrn": "urn:harmonic:people_watchlist:780c2910-b21d-4ad2-ba04-c98ac939dbd8"}
```

### Delete list entries

Remove entries from a people list. You can specify people by URN or canonical identifiers.

**POST** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/entries:batchDelete`

| Name | Type | Description |
| --- | --- | --- |
| `entries` | array[object] | Array of entries to delete. Each entry must have either person_urn or canonical identifiers. |

##### Example request

Provide either `person_urn` or `canonical` identifiers for each entry.

```json
{
  "entries": [
    { "person_urn": "urn:harmonic:person:123" },
    {
      "canonical": {
        "linkedin_url": "https://linkedin.com/in/example",
        "email": "max@example.com"
      }
    }
  ]
}
```

**REST**

`POST https://api.harmonic.ai/watchlists/people/{id_or_urn}/entries:batchDelete`

```json
{
  "urns": [
    "urn:harmonic:person:123",
    "urn:harmonic:person:456"
  ]
}
```

### Get import details

Get details about a specific import operation, including success/failure counts and status.

**GET** `https://api.harmonic.ai/watchlists/people/imports/{id_or_urn}`

**REST**

`GET https://api.harmonic.ai/watchlists/people/imports/{id_or_urn}`

```json
{
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z",
  "user_people_import_urn": "urn:harmonic:user_people_import:123",
  "people_list_urn": "urn:harmonic:people_watchlist:456",
  "file_name": "import.csv",
  "flatfile_batch_id": "batch_123",
  "user_urn": "urn:harmonic:user:789",
  "user_urn": "urn:harmonic:user:1",
  "user_id": "1",
  "customer_urn": "urn:harmonic:customer:1",
  "customer_id": "1",
  "entity_urn": "urn:harmonic:user_people_import:123",
  "id": "123",
  "failed_people_count": 0,
  "pending_people_count": 0,
  "success_people_count": 1
}
```

### Get import entries

Get the entries (people) from a specific import operation. Results include matched people and any validation errors.

**GET** `https://api.harmonic.ai/watchlists/people/imports/{id_or_urn}/entries`

**REST**

`GET https://api.harmonic.ai/watchlists/people/imports/{id_or_urn}/entries`

```json
{
  "imported_people": [
    {
      "matched_person_urn": "urn:harmonic:person:123",
      "canonicals": {
        "linkedin_url": "https://linkedin.com/in/example",
      },
      "user_people_import_urn": "urn:harmonic:user_people_import:456",
      "custom_field_values": [
        {
          "custom_field_urn": "urn:harmonic:person_list_custom_field:789",
          "data": {
            "value": "In Progress"
          }
        }
      ],
      "invalid_canonicals": false,
      "created_at": "2024-01-15T12:00:00Z",
      "updated_at": "2024-01-15T12:00:00Z",
      "user_imported_person_urn": "urn:harmonic:user_imported_person:012"
    }
  ]
}
```

### Get list imports

Get all import operations for a specific people list. Results are paginated.

**GET** `https://api.harmonic.ai/watchlists/people/{id_or_urn}/imports`

| Name | Type | Description |
| --- | --- | --- |
| `page` | integer | Page number (starts at 0) |
| `size` | integer | Number of imports per page (default 50) |

**REST**

`GET https://api.harmonic.ai/watchlists/people/{id_or_urn}/imports`

```json
{
  "user_people_imports": [
    {
      "created_at": "2024-01-15T12:00:00Z",
      "updated_at": "2024-01-15T12:00:00Z",
      "user_people_import_urn": "urn:harmonic:user_people_import:123",
      "people_list_urn": "urn:harmonic:people_watchlist:456",
      "file_name": "import.csv",
      "flatfile_batch_id": "batch_123",
      "user_urn": "urn:harmonic:user:789"
    }
  ],
  "total_count": 1
}
```

## Company attachments

Upload, rename, download, and delete attachments on companies.

### Get attachments for companies

Get all attachments for a list of companies.

**POST** `https://api.harmonic.ai/companies/attachments`

| Name | Type | Description |
| --- | --- | --- |
| `entity_urns` | array[string] | List of company urns to get attachments for. |

##### Example request

```json
{
  "entity_urns": ["urn:harmonic:company:123", "urn:harmonic:company:456"]
}
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/companies/attachments`

```json
[
  {
    "entity_urn": "urn:harmonic:company:123",
    "attachments": [
      {
        "attachment_urn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
        "name": "file.pdf",
        "extension": "pdf",
        "size": 123456,
        "upload_uri": "invalid",
        "link": "https://api.harmonic.ai/companies/123/attachments/016342c0-708e-463d-81ab-231369032b84",
        "created_at": "2025-06-15T12:00:00Z",
        "updated_at": "2025-06-15T12:00:00Z"
        "uploaded_at": "2025-06-15T12:00:00Z",
        "uploaded_by": "urn:harmonic:customer:123",
      }
    ]
  }
]
```

**GraphQL query**

```graphql
query GetCompanyAttachments($id: Int!) {
  getCompanyById(id: $id) {
    attachments {
      attachmentUrn
      name
      extension
      size
      uploadUri
      link
      createdAt
      updatedAt
      uploadedAt
      uploadedBy {
        ...on User {
         name
         email
         entityUrn
        }
        ...on Customer {
          name
          entityUrn
        }
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "id": 123
}
```

### Initiate company attachment upload

Initiate a new attachments upload for a company.

Uploads have 3 steps:

1. Initiate the upload with this endpoint
2. Upload the files to the `upload_uri` returned in the response
3. Complete the upload with the **Complete Company Attachment Upload** endpoint

All 3 steps must be completed for each file being uploaded to create a new attachment.

**POST** `https://api.harmonic.ai/companies/{id_or_urn}/attachments`

| Name | Type | Description |
| --- | --- | --- |
| `attachments` | array[object] | Array of attachments to create. Each must have name, extension (pdf, png, jpg, jpeg, ppt, pptx, doc, docx, csv, xls, xlsx), and size in bytes (max 500MB). |

##### Example request

```json
[
  {
    "name": "file.pdf",
    "extension": "pdf",
    "size": 123456
  }
]
```

**Restrictions on inputs:**

1. The `name` field must be 200 characters or less. It does not need to be unique.
2. The `extension` field must be one of the following values: `pdf`, `png`, `jpg`, `jpeg`, `ppt`, `pptx`, `doc`, `docx`, `csv`, `xls`, `xlsx`
3. The `size` field must be less than 500 MB

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/companies/{id_or_urn}/attachments`

```json
{
  "attachments": [
    {
      "attachment_urn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
      "name": "file.pdf",
      "extension": "pdf",
      "size": 123456,
      "upload_uri": "https://storage.harmonic.ai/upload/016342c0-708e-463d-81ab-231369032b84",
      "created_at": "2025-06-15T12:00:00Z",
      "updated_at": "2025-06-15T12:00:00Z",
      "uploaded_by": "urn:harmonic:customer:123"
    }
  ]
}
```

**GraphQL query**

```graphql
mutation CreateAttachments($input: [AttachmentMetadataCreateInput!]!, $entityUrn: String!) {
  createAttachments(input: $input, entityUrn: $entityUrn) {
    attachmentUrn
    name
    extension
    size
    uploadUri
    link
    createdAt
    updatedAt
    uploadedAt
    uploadedBy {
      ...on User {
        name
        email
        entityUrn
      }
      ...on Customer {
        name
        entityUrn
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "input": [
    {
      "name": "file.pdf",
      "extension": "pdf",
      "size": 123456
    }
  ],
  "entityUrn": "urn:harmonic:company:123"
}
```

### Complete company attachment uploads

Complete the uploads of a set of company attachments.

This endpoint must be called to complete the upload process. When this API is called, an `uploaded_at` date is added and persisted with the attachment metadata.

**PUT** `https://api.harmonic.ai/companies/{id_or_urn}/attachments`

| Name | Type | Description |
| --- | --- | --- |
| `attachment_urns` * | array[string] | Array of attachment URNs to complete upload for. |

##### Example request

```json
{
  "attachment_urns": [
    "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84"
  ]
}
```

Supported modes: REST, GraphQL

**REST**

`PUT https://api.harmonic.ai/companies/{id_or_urn}/attachments`

```json
{
  "attachments": [
    {
      "attachment_urn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
      "name": "file.pdf",
      "extension": "pdf",
      "size": 123456,
      "upload_uri": "invalid",
      "link": "https://api.harmonic.ai/companies/123/attachments/016342c0-708e-463d-81ab-231369032b84",
      "created_at": "2025-06-15T12:00:00Z",
      "updated_at": "2025-06-15T12:00:00Z",
      "uploaded_at": "2025-06-15T12:00:00Z",
      "uploaded_by": "urn:harmonic:customer:123"
    }
  ]
}
```

**GraphQL query**

```graphql
mutation CompleteAttachmentUploads($attachmentUrns: [String!]!, $entityUrn: String!) {
  completeAttachmentUploads(attachmentUrns: $attachmentUrns, entityUrn: $entityUrn) {
    attachmentUrn
    name
    extension
    size
    uploadUri
    link
    createdAt
    updatedAt
    uploadedAt
    uploadedBy {
      ...on User {
        name
        email
        entityUrn
      }
      ...on Customer {
        name
        entityUrn
      }
    }
  }
}
```

### Rename company attachment

Rename a company attachment.

**PATCH** `https://api.harmonic.ai/companies/{id_or_urn}/attachments/{urn}`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | The new name for the attachment. |

##### Example request

```json
{
  "name": "new-name.pdf"
}
```

Supported modes: REST, GraphQL

**REST**

`PATCH https://api.harmonic.ai/companies/{id_or_urn}/attachments/{urn}`

```json
{
    "attachment_urn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
    "name": "file.pdf",
    "extension": "pdf",
    "size": 123456,
    "upload_uri": "invalid",
    "link": "https://api.harmonic.ai/companies/123/attachments/016342c0-708e-463d-81ab-231369032b84",
    "created_at": "2025-06-15T12:00:00Z",
    "updated_at": "2025-06-15T12:00:00Z"
    "uploaded_at": "2025-06-15T12:00:00Z",
    "uploaded_by": "urn:harmonic:customer:123",
}
```

**GraphQL query**

```graphql
mutation RenameAttachment($attachmentUrn: String!, $input: AttachmentMetadataUpdateInput!, $entityUrn: String!) {
  updateAttachment(attachmentUrn: $attachmentUrn, input: $input, entityUrn: $entityUrn) {
    attachmentUrn
    name
    extension
    size
    uploadUri
    link
    createdAt
    updatedAt
    uploadedAt
    uploadedBy {
      ...on User {
        name
        email
        entityUrn
      }
      ...on Customer {
        name
        entityUrn
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "attachmentUrn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
  "input": {
    "name": "new-name.pdf"
  },
  "entityUrn": "urn:harmonic:company:123"
}
```

### Get company attachment contents

Get the contents of a company attachment.

This request will return a secure URL from where the original file contents can be downloaded. Getting access to the contents requires a two step process:

1. Make a `GET` request to this endpoint, and parse the response to get the secure `url`
2. Issue a `GET` request to the secure `url` returned in the response

The secure `url` may only be used to fetch contents once, and will be available only for 1 minute after being issued. As a result, the `url` should not be shared or persisted. This API will generate a new secure `url` on each request.

**GET** `https://api.harmonic.ai/companies/{id_or_urn}/attachments/{urn}`

**REST**

`GET https://api.harmonic.ai/companies/{id_or_urn}/attachments/{urn}`

```json
{
  "url": "https://storage.harmonic.ai/attachments/016342c0-708e-463d-81ab-231369032b84"
}
```

### Delete company attachment

Deletes a company attachment.

**DELETE** `https://api.harmonic.ai/companies/{id_or_urn}/attachments/{urn}`

Supported modes: REST, GraphQL

**REST**

`DELETE https://api.harmonic.ai/companies/{id_or_urn}/attachments/{urn}`

```json
true
```

**GraphQL query**

```graphql
mutation DeleteAttachment($attachmentUrn: String!, $entityUrn: String!) {
  deleteAttachment(attachmentUrn: $attachmentUrn, entityUrn: $entityUrn)
}
```

**GraphQL variables**

```json
{
  "attachmentUrn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
  "entityUrn": "urn:harmonic:company:123"
}
```

## Person attachments

Upload, rename, download, and delete attachments on people.

### Get attachments for persons

Get all attachments for a list of persons.

**POST** `https://api.harmonic.ai/persons/attachments`

| Name | Type | Description |
| --- | --- | --- |
| `entity_urns` | array[string] | List of person urns to get attachments for. |

##### Example request

```json
{
  "entity_urns": ["urn:harmonic:person:123", "urn:harmonic:person:456"]
}
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/persons/attachments`

```json
[
  {
    "entity_urn": "urn:harmonic:person:123",
    "attachments": [
      {
        "attachment_urn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
        "name": "file.pdf",
        "extension": "pdf",
        "size": 123456,
        "upload_uri": "invalid",
        "link": "https://api.harmonic.ai/persons/123/attachments/016342c0-708e-463d-81ab-231369032b84",
        "created_at": "2025-06-15T12:00:00Z",
        "updated_at": "2025-06-15T12:00:00Z"
        "uploaded_at": "2025-06-15T12:00:00Z",
        "uploaded_by": "urn:harmonic:customer:123",
      }
    ]
  }
]
```

**GraphQL query**

```graphql
query GetPersonAttachments($id: Int!) {
  getPersonById(id: $id) {
    attachments {
      attachmentUrn
      name
      extension
      size
      uploadUri
      link
      createdAt
      updatedAt
      uploadedAt
      uploadedBy {
        ...on User {
         name
         email
         entityUrn
        }
        ...on Customer {
          name
          entityUrn
        }
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "id": 123
}
```

### Create person attachments

Create new attachments for a person in batch.

Uploads have 3 steps:

1. Initiate the upload with this endpoint
2. Upload the files to the `upload_uri` returned in the response
3. Complete the upload with the **Complete Person Attachment Upload** endpoint

All 3 steps must be completed for each file being uploaded to create a new attachment.

**POST** `https://api.harmonic.ai/persons/{id_or_urn}/attachments`

| Name | Type | Description |
| --- | --- | --- |
| `attachments` | array[object] | Array of attachments to create. Each must have name, extension (pdf, png, jpg, jpeg, ppt, pptx, doc, docx, csv, xls, xlsx), and size in bytes (max 500MB). |

##### Example request

```json
[
  {
    "name": "file.pdf",
    "extension": "pdf",
    "size": 123456
  }
]
```

**Restrictions on inputs:**

1. The `name` field must be 200 characters or less. It does not need to be unique.
2. The `extension` field must be one of the following values: `pdf`, `png`, `jpg`, `jpeg`, `ppt`, `pptx`, `doc`, `docx`, `csv`, `xls`, `xlsx`
3. The `size` field must be less than 500 MB

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/persons/{id_or_urn}/attachments`

```json
{
  "attachments": [
    {
      "attachment_urn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
      "name": "file.pdf",
      "extension": "pdf",
      "size": 123456,
      "upload_uri": "https://storage.harmonic.ai/upload/016342c0-708e-463d-81ab-231369032b84",
      "created_at": "2025-06-15T12:00:00Z",
      "updated_at": "2025-06-15T12:00:00Z",
      "uploaded_by": "urn:harmonic:customer:123"
    }
  ]
}
```

**GraphQL query**

```graphql
mutation CreateAttachments($input: [AttachmentMetadataCreateInput!]!, $entityUrn: String!) {
  createAttachments(input: $input, entityUrn: $entityUrn) {
    attachmentUrn
    name
    extension
    size
    uploadUri
    link
    createdAt
    updatedAt
    uploadedAt
    uploadedBy {
      ...on User {
        name
        email
        entityUrn
      }
      ...on Customer {
        name
        entityUrn
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "input": [
    {
      "name": "file.pdf",
      "extension": "pdf",
      "size": 123456
    }
  ],
  "entityUrn": "urn:harmonic:person:123"
}
```

### Complete person attachment uploads

Complete the uploads of a set of person attachments.

This endpoint must be called to complete the upload process. When this API is called, an `uploaded_at` date is added and persisted with the attachment metadata.

**PUT** `https://api.harmonic.ai/persons/{id_or_urn}/attachments`

| Name | Type | Description |
| --- | --- | --- |
| `attachment_urns` * | array[string] | Array of attachment URNs to complete upload for. |

##### Example request

```json
{
  "attachment_urns": [
    "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84"
  ]
}
```

Supported modes: REST, GraphQL

**REST**

`PUT https://api.harmonic.ai/persons/{id_or_urn}/attachments`

```json
{
  "attachments": [
    {
      "attachment_urn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
      "name": "file.pdf",
      "extension": "pdf",
      "size": 123456,
      "upload_uri": "invalid",
      "link": "https://api.harmonic.ai/persons/123/attachments/016342c0-708e-463d-81ab-231369032b84",
      "created_at": "2025-06-15T12:00:00Z",
      "updated_at": "2025-06-15T12:00:00Z",
      "uploaded_at": "2025-06-15T12:00:00Z",
      "uploaded_by": "urn:harmonic:customer:123"
    }
  ]
}
```

**GraphQL query**

```graphql
mutation CompleteAttachmentUploads($attachmentUrns: [String!]!, $entityUrn: String!) {
  completeAttachmentUploads(attachmentUrns: $attachmentUrns, entityUrn: $entityUrn) {
    attachmentUrn
    name
    extension
    size
    uploadUri
    link
    createdAt
    updatedAt
    uploadedAt
    uploadedBy {
      ...on User {
        name
        email
        entityUrn
      }
      ...on Customer {
        name
        entityUrn
      }
    }
  }
}
```

### Rename person attachment

Rename a person attachment.

**PATCH** `https://api.harmonic.ai/persons/{id_or_urn}/attachments/{urn}`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | The new name for the attachment. |

##### Example request

```json
{
  "name": "new-name.pdf"
}
```

Supported modes: REST, GraphQL

**REST**

`PATCH https://api.harmonic.ai/persons/{id_or_urn}/attachments/{urn}`

```json
{
  "attachment_urn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
  "name": "file.pdf",
  "extension": "pdf",
  "size": 123456,
  "upload_uri": "invalid",
  "link": "https://api.harmonic.ai/persons/123/attachments/016342c0-708e-463d-81ab-231369032b84",
  "created_at": "2025-06-15T12:00:00Z",
  "updated_at": "2025-06-15T12:00:00Z"
  "uploaded_at": "2025-06-15T12:00:00Z",
  "uploaded_by": "urn:harmonic:customer:123",
}
```

**GraphQL query**

```graphql
mutation RenameAttachment($attachmentUrn: String!, $input: AttachmentMetadataUpdateInput!, $entityUrn: String!) {
  updateAttachment(attachmentUrn: $attachmentUrn, input: $input, entityUrn: $entityUrn) {
    attachmentUrn
    name
    extension
    size
    uploadUri
    link
    createdAt
    updatedAt
    uploadedAt
    uploadedBy {
      ...on User {
        name
        email
        entityUrn
      }
      ...on Customer {
        name
        entityUrn
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "attachmentUrn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
  "input": {
    "name": "new-name.pdf"
  },
  "entityUrn": "urn:harmonic:person:123"
}
```

### Get person attachment contents

Get the contents of a person attachment.

This request will return a secure URL from where the original file contents can be downloaded. Getting access to the contents requires a two step process:

1. Make a `GET` request to this endpoint, and parse the response to get the secure `url`
2. Issue a `GET` request to the secure `url` returned in the response

The secure `url` may only be used to fetch contents once, and will be available only for 1 minute after being issued. As a result, the `url` should not be shared or persisted. This API will generate a new secure `url` on each request.

**GET** `https://api.harmonic.ai/persons/{id_or_urn}/attachments/{urn}`

**REST**

`GET https://api.harmonic.ai/persons/{id_or_urn}/attachments/{urn}`

```json
{
  "url": "https://storage.harmonic.ai/attachments/016342c0-708e-463d-81ab-231369032b84"
}
```

### Delete person attachment

Deletes a person attachment.

**DELETE** `https://api.harmonic.ai/persons/{id_or_urn}/attachments/{urn}`

Supported modes: REST, GraphQL

**REST**

`DELETE https://api.harmonic.ai/persons/{id_or_urn}/attachments/{urn}`

```json
true
```

**GraphQL query**

```graphql
mutation DeleteAttachment($attachmentUrn: String!, $entityUrn: String!) {
  deleteAttachment(attachmentUrn: $attachmentUrn, entityUrn: $entityUrn)
}
```

**GraphQL variables**

```json
{
  "attachmentUrn": "urn:harmonic:user_uploaded_content:016342c0-708e-463d-81ab-231369032b84",
  "entityUrn": "urn:harmonic:person:123"
}
```

## Company global fields

Manage custom fields and values across all companies.

### Get global fields

Get all global custom fields defined for companies. Returns an array of custom fields.

**GET** `https://api.harmonic.ai/companies/custom_fields`

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/companies/custom_fields`

```json
[
  {
    "urn": "urn:harmonic:company_list_custom_field:123",
    "name": "Contract Value",
    "type": "NUMBER"
  },
  {
    "urn": "urn:harmonic:company_list_custom_field:124",
    "name": "Sales Stage",
    "type": "SINGLE_SELECT"
  },
  {
    "urn": "urn:harmonic:company_list_custom_field:125",
    "name": "Primary Contact",
    "type": "PERSON"
  }
]
```

**GraphQL query**

```graphql
query CompanyGlobalFields {
  companyCustomFields {
    urn
    name
    type
  }
}
```

### Create a global field

Create a new global custom field for companies.

**POST** `https://api.harmonic.ai/companies/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Name of the custom field |
| `type` | string | Type of the custom field. One of: TEXT, NUMBER, DATE, SINGLE_SELECT, MULTI_SELECT, PERSON, WEBSITE, CHECKBOX, STATUS |
| `metadata` | object | Optional metadata for the field. Structure depends on field type. |

##### Example request

```json
{
  "name": "Account owner",
  "type": "PERSON",
  "metadata": {
    "mode": "SINGLE"
  }
}
```

##### Metadata shape by field type

For `SINGLE_SELECT` / `MULTI_SELECT` / `STATUS`:

```
{
  "options": [
    {
      "name": "Option Name",
      "color": "#HEX_COLOR",
      "default": false
    }
  ]
}
```

For `NUMBER`:

```
{
  "format": "NUMBER" | "PERCENT" | "US_DOLLAR"
}
```

For `DATE`:

```
{
  "format": "MM_DD_YYYY" | "DD_MM_YYYY" | "YYYY_MM_DD"
}
```

For `PERSON`:

```
{
  "mode": "SINGLE" | "MULTIPLE"
}
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/companies/custom_field`

```json
{
  "urn": "urn:harmonic:company_list_custom_field:126",
  "name": "Deal Size",
  "type": "NUMBER",
  "metadata": {
    "format": "US_DOLLAR"
  }
}
```

**GraphQL query**

```graphql
mutation CreateCompanyCustomField($customFieldInput: CompanyListCustomFieldCreateInput!) {
  createCompanyCustomField(customFieldInput: $customFieldInput) {
    urn
    name
    type
    metadata
  }
}
```

**GraphQL variables**

```json
{
  "customFieldInput": {
    "name": "Custom field",
    "type": "TEXT"
  }
}
```

### Update a global field

Update an existing global custom field for companies.

**PUT** `https://api.harmonic.ai/companies/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `custom_field_urn` * | string | (Query Parameter) URN of the custom field to update (format: urn:harmonic:company_list_custom_field:<id>) |
| `name` | string | (Body Parameter) New name for the custom field |
| `metadata` | object | (Body Parameter) Optional metadata for the field. Structure depends on field type. |

`custom_field_urn` is passed as a query parameter; `name` and `metadata` go in the request body.

##### Example request

```json
{
  "name": "Updated account owner"
}
```

##### Metadata shape by field type

For `SINGLE_SELECT` / `MULTI_SELECT` / `STATUS`:

```
{
  "options": [
    {
      "name": "Option Name",
      "color": "#HEX_COLOR",
      "default": false
    }
  ]
}
```

For `NUMBER`:

```
{
  "format": "NUMBER" | "PERCENT" | "US_DOLLAR"
}
```

For `DATE`:

```
{
  "format": "MM_DD_YYYY" | "DD_MM_YYYY" | "YYYY_MM_DD"
}
```

For `PERSON`:

```
{
  "mode": "SINGLE" | "MULTIPLE"
}
```

Supported modes: REST, GraphQL

**REST**

`PUT https://api.harmonic.ai/companies/custom_field`

```json
{
  "urn": "urn:harmonic:company_list_custom_field:126",
  "name": "Updated Deal Size",
  "type": "NUMBER",
  "metadata": {
    "format": "US_DOLLAR"
  }
}
```

**GraphQL query**

```graphql
mutation UpdateCompanyCustomField($customFieldUrn: CompanyListCustomFieldUrn!, $customFieldInput: CompanyListCustomFieldUpdateInput!) {
  updateCompanyCustomField(customFieldUrn: $customFieldUrn, customFieldInput: $customFieldInput) {
    urn
    name
    type
    metadata
  }
}
```

**GraphQL variables**

```json
{
  "customFieldUrn": "urn:harmonic:company_list_custom_field:126",
  "customFieldInput": {
    "name": "Updated Custom field"
  }
}
```

### Delete a global field

Delete a global custom field. This will remove the field and all associated values.

**DELETE** `https://api.harmonic.ai/companies/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `custom_field_urn` * | string | The URN of the custom field to delete. Format: urn:harmonic:company_list_custom_field:<id> |

Supported modes: REST, GraphQL

**REST**

`DELETE https://api.harmonic.ai/companies/custom_field`

```json
{
  "success": true
}
```

**GraphQL query**

```graphql
mutation RemoveCompanyCustomField($customFieldUrn: String!) {
  removeCompanyCustomField(customFieldUrn: $customFieldUrn)
}
```

**GraphQL variables**

```json
{
  "customFieldUrn": "urn:harmonic:company_list_custom_field:126"
}
```

### Upsert global field values

Set or update custom field values for one or more companies.

**POST** `https://api.harmonic.ai/companies/entries`

| Name | Type | Description |
| --- | --- | --- |
| `entries` | array[object] | Array of companies to create or update global field values for. Each company must have either company_urn or canonical identifiers. |

**Value formats by field type:**

- **TEXT:** `{ "value": "string" }`
- **NUMBER:** `{ "value": 123.45 }`
- **DATE:** `{ "value": "2024-12-15" }` (YYYY-MM-DD format)
- **SINGLE_SELECT:** `{ "value": "urn:harmonic:select_list_custom_field_value_option:789" }`
- **MULTI_SELECT:** `{ "value": ["urn:harmonic:select_list_custom_field_value_option:789", ...] }`
- **PERSON:** `{ "value": ["urn:harmonic:user:123"] }` or `{ "value": ["max@harmonic.ai"] }`
- **WEBSITE:** `{ "value": "https://example.com" }`
- **CHECKBOX:** `{ "value": true }`
- **STATUS:** `{ "value": "urn:harmonic:select_list_custom_field_value_option:789" }`

##### Example request

Provide either `company_urn` or `canonical` identifiers; `values` is optional and each value's format depends on the field type (see above):

```json
{
  "company_urn": "urn:harmonic:company:123",
  "canonical": {
    "website_url": "example.com",
    "crunchbase_url": "https://www.crunchbase.com/organization/example",
    "pitchbook_url": "https://pitchbook.com/profile/example",
    "linkedin_url": "https://linkedin.com/company/example"
  },
  "values": [
    {
      "custom_field_urn": "urn:harmonic:company_list_custom_field:456",
      "data": {
        "value": "In Progress"
      }
    }
  ]
}
```

**GraphQL query**

```graphql
mutation UpsertCompanyCustomFieldValues($customFieldUrn: CompanyListCustomFieldUrn!, $companyUrns: [CompanyUrn!]!, $customFieldValueInput: CompanyListCustomFieldValueUpsertInput!) {
  upsertCompanyCustomFieldValues(customFieldUrn: $customFieldUrn, companyUrns: $companyUrns, customFieldValueInput: $customFieldValueInput) {
    entityUrn
  }
}
```

**GraphQL variables**

```json
{
  "customFieldUrn": "urn:harmonic:company_list_custom_field:456",
  "companyUrns": ["urn:harmonic:company:123"],
  "customFieldValueInput": {
    "selectData": {
      "value": "urn:harmonic:select_list_custom_field_value_option:789"
    }
  }
}
```

### Get global field values

Get custom field values for a company.

**GET** `GraphQL only`

Supported modes: REST, GraphQL

```json
This is supported in the GraphQL API only.
```

**GraphQL query**

```graphql
query GetCompanyById($getCompanyByIdId: Int!) {
  getCompanyById(id: $getCompanyByIdId) {
    customFieldValues {
      urn
      data {
        ... on TextCustomFieldValue {
          value
        }
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "getCompanyByIdId": 1
}
```

## Person global fields

Manage custom fields and values across all people.

### Get global fields

Get all global custom fields defined for people.

**GET** `https://api.harmonic.ai/persons/custom_fields`

Supported modes: REST, GraphQL

**REST**

`GET https://api.harmonic.ai/persons/custom_fields`

```json
[
  {
    "urn": "urn:harmonic:person_list_custom_field:456",
    "name": "Interview Status",
    "type": "STATUS"
  },
  {
    "urn": "urn:harmonic:person_list_custom_field:457",
    "name": "Skills",
    "type": "MULTI_SELECT"
  },
  {
    "urn": "urn:harmonic:person_list_custom_field:458",
    "name": "Last Contact Date",
    "type": "DATE"
  }
]
```

**GraphQL query**

```graphql
query PeopleGlobalFields {
  peopleCustomFields {
    urn
    name
    type
  }
}
```

### Create a global field

Create a new global custom field for people.

**POST** `https://api.harmonic.ai/persons/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `name` | string | Name of the custom field |
| `type` | string | Type of the custom field. One of: TEXT, NUMBER, DATE, SINGLE_SELECT, MULTI_SELECT, PERSON, WEBSITE, CHECKBOX, STATUS |
| `metadata` | object | Optional metadata for the field. Structure depends on field type. |

##### Example request

```json
{
  "name": "Referral source",
  "type": "SINGLE_SELECT",
  "metadata": {
    "options": [
      { "name": "Inbound", "color": "#4F46E5", "default": true },
      { "name": "Outbound", "color": "#059669", "default": false }
    ]
  }
}
```

##### Metadata shape by field type

For `SINGLE_SELECT` / `MULTI_SELECT` / `STATUS`:

```
{
  "options": [
    {
      "name": "Option Name",
      "color": "#HEX_COLOR",
      "default": false
    }
  ]
}
```

For `NUMBER`:

```
{
  "format": "NUMBER" | "PERCENT" | "US_DOLLAR"
}
```

For `DATE`:

```
{
  "format": "MM_DD_YYYY" | "DD_MM_YYYY" | "YYYY_MM_DD"
}
```

For `PERSON`:

```
{
  "mode": "SINGLE" | "MULTIPLE"
}
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/persons/custom_field`

```json
{
  "urn": "urn:harmonic:person_list_custom_field:459",
  "name": "Referral Source",
  "type": "TEXT"
}
```

**GraphQL query**

```graphql
mutation CreatePeopleCustomField($customFieldInput: PeopleListCustomFieldCreateInput!) {
  createPeopleCustomField(customFieldInput: $customFieldInput) {
    name
    type
  }
}
```

**GraphQL variables**

```json
{
  "customFieldInput": {
    "name": "Referral Source",
    "type": "TEXT"
  }
}
```

### Update a global field

Update an existing global custom field for people.

**PUT** `https://api.harmonic.ai/persons/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `custom_field_urn` * | string | (Query Parameter) URN of the custom field to update (format: urn:harmonic:person_list_custom_field:<id>) |
| `name` | string | (Body Parameter) New name for the custom field |
| `metadata` | object | (Body Parameter) Optional metadata for the field. Structure depends on field type. |

`custom_field_urn` is passed as a query parameter; `name` and `metadata` go in the request body.

##### Example request

```json
{
  "name": "Updated referral source"
}
```

##### Metadata shape by field type

For `SINGLE_SELECT` / `MULTI_SELECT` / `STATUS`:

```
{
  "options": [
    {
      "name": "Option Name",
      "color": "#HEX_COLOR",
      "default": false
    }
  ]
}
```

For `NUMBER`:

```
{
  "format": "NUMBER" | "PERCENT" | "US_DOLLAR"
}
```

For `DATE`:

```
{
  "format": "MM_DD_YYYY" | "DD_MM_YYYY" | "YYYY_MM_DD"
}
```

For `PERSON`:

```
{
  "mode": "SINGLE" | "MULTIPLE"
}
```

Supported modes: REST, GraphQL

**REST**

`PUT https://api.harmonic.ai/persons/custom_field`

```json
{
  "urn": "urn:harmonic:person_list_custom_field:459",
  "name": "Updated Referral Source",
  "type": "TEXT"
}
```

**GraphQL query**

```graphql
mutation UpdatePeopleCustomField($customFieldUrn: PeopleListCustomFieldUrn!, $customFieldInput: PeopleListCustomFieldUpdateInput!) {
  updatePeopleCustomField(customFieldUrn: $customFieldUrn, customFieldInput: $customFieldInput) {
    name
    type
  }
}
```

**GraphQL variables**

```json
{
  "customFieldUrn": "urn:harmonic:person_list_custom_field:459",
  "customFieldInput": {
    "name": "Updated Referral Source"
  }
}
```

### Delete a global field

Delete a global custom field. This will remove the field and all associated values.

**DELETE** `https://api.harmonic.ai/persons/custom_field`

| Name | Type | Description |
| --- | --- | --- |
| `custom_field_urn` * | string | The URN of the custom field to delete. Format: urn:harmonic:person_list_custom_field:<id> |

Supported modes: REST, GraphQL

**REST**

`DELETE https://api.harmonic.ai/persons/custom_field`

```json
{
  "success": true
}
```

**GraphQL query**

```graphql
mutation RemovePeopleCustomField($customFieldUrn: PeopleListCustomFieldUrn!) {
  removePeopleCustomField(customFieldUrn: $customFieldUrn) {
    urn
  }
}
```

**GraphQL variables**

```json
{
  "customFieldUrn": "urn:harmonic:person_list_custom_field:459"
}
```

### Upsert global field values

Set or update custom field values for one or more people.

**POST** `https://api.harmonic.ai/persons/entries`

| Name | Type | Description |
| --- | --- | --- |
| `entries` | array[object] | Array of people to create or update global field values for. Each person must have either person_urn or canonical identifiers (linkedin_url or email). |

If you provide a canonical identifier, at least one of linkedin_url or email must be provided. Harmonic will attempt to match this to a person in our database. We recommend providing a linkedin_url when possible for the best results.

**Value formats by field type:**

- **TEXT:** `{ "value": "string" }`
- **NUMBER:** `{ "value": 123.45 }`
- **DATE:** `{ "value": "2024-12-15" }` (YYYY-MM-DD format)
- **SINGLE_SELECT:** `{ "value": "urn:harmonic:select_list_custom_field_value_option:789" }`
- **MULTI_SELECT:** `{ "value": ["urn:harmonic:select_list_custom_field_value_option:789", ...] }`
- **PERSON:** `{ "value": ["urn:harmonic:user:123"] }` or `{ "value": ["max@harmonic.ai"] }`
- **WEBSITE:** `{ "value": "https://example.com" }`
- **CHECKBOX:** `{ "value": true }`
- **STATUS:** `{ "value": "urn:harmonic:select_list_custom_field_value_option:789" }`

##### Example request

Provide either `person_urn` or `canonical` identifiers; `values` is optional and each value's format depends on the field type (see above):

```json
{
  "person_urn": "urn:harmonic:person:123",
  "canonical": {
    "linkedin_url": "https://linkedin.com/in/example",
    "email": "max@example.com"
  },
  "values": [
    {
      "custom_field_urn": "urn:harmonic:person_list_custom_field:456",
      "data": {
        "value": "In Progress"
      }
    }
  ]
}
```

Supported modes: REST, GraphQL

**REST**

`POST https://api.harmonic.ai/persons/entries`

```json
{
  "people_found_count": 1,
  "people_invalid_count": 0,
  "people_not_found_count": 0,
  "total_people_count": 1,
  "user_people_import_urn": "urn:harmonic:user_people_import:123"
}
```

**GraphQL query**

```graphql
mutation UpsertPeopleCustomFieldValues($customFieldUrn: PeopleListCustomFieldUrn!, $personUrns: [PersonUrn!]!, $customFieldValueInput: PeopleListCustomFieldValueUpsertInput!) {
  upsertPeopleCustomFieldValues(customFieldUrn: $customFieldUrn, personUrns: $personUrns, customFieldValueInput: $customFieldValueInput) {
    customFieldValues {
      name
      type
    }
  }
}
```

**GraphQL variables**

```json
{
  "customFieldUrn": "urn:harmonic:person_list_custom_field:456",
  "personUrns": ["urn:harmonic:person:123"],
  "customFieldValueInput": {
    "selectData": {
      "value": "urn:harmonic:select_list_custom_field_value_option:789"
    }
  }
}
```

### Get global field values

Get custom field values for a person.

**GET** `GraphQL only`

Supported modes: REST, GraphQL

```json
This is supported in the GraphQL API only.
```

**GraphQL query**

```graphql
query GetPersonById($getPersonByIdId: Int!) {
  getPersonById(id: $getPersonByIdId) {
    customFieldValues {
      urn
      data {
        ... on TextCustomFieldValue {
          value
        }
      }
    }
  }
}
```

**GraphQL variables**

```json
{
  "getPersonByIdId": 1
}
```

## Customer

Get customer details and team users.

### Get customer by URN

Retrieve detailed information about a customer by providing their URN.

**GET** `https://api.harmonic.ai/customers/{urn}`

**GraphQL query**

```graphql
query GetCustomer($urn: String!) {
  getCustomerByUrn(urn: $urn) {
    entityUrn
    name
    __typename
  }
}
```

**GraphQL variables**

```json
{ "urn": "urn:harmonic:customer:123456" }
```

### Get customer users

Retrieve a list of all users associated with a specific customer by providing the customer URN.

**GET** `https://api.harmonic.ai/customers/{urn}/users`

**GraphQL query**

```graphql
query GetAllTeamMembersByCustomer($urn: String!) {
  getAllTeamMembersByCustomer(urn: $urn) {
    role
    status
    user {
      email
      entityUrn
      name
      __typename
    }
    __typename
  }
}
```

**GraphQL variables**

```json
{ "urn": "urn:harmonic:customer:123456" }
```
