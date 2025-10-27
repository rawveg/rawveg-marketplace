# Hashnode-Api - Api

**Pages:** 2

---

## Hashnode Public API Docs

**URL:** https://apidocs.hashnode.com

**Contents:**
- Hashnode Public API Docs
- Welcome
- GQL Playground
- Caching
- Rate Limits
- Authentication
- Status and Error Codes
- Pagination
- 1. Cursor-Based Pagination
  - Example Query in GraphQL

This document describes the Hashnode Public API. The Hashnode Public API is a GraphQL API that allows you to interact with Hashnode.

Make sure to join our Discord server to be in the loop about any updates.

If you're seeing Errors with a 502 status code, it's highly likely that you are using api.hashnode.com. This was our legacy API and is now officially discontinued. Please use these docs and the migration guide to transition to our new GQL API.

All Hashnode Public API queries are made through a single GraphQL endpoint, which only accepts POST requests.

https://gql.hashnode.com

You can visit the same URL to check out Hashnode API Playground.

You can query user details, publication information, posts within publications, drafts, and more. Please explore the playground to view all available fields.

Additionally, mutations are at your disposal for actions such as publishing posts, subscribing to newsletters, and following users. The complete list of these available mutations can be found within the playground.

If you're not familiar with GraphQL, be sure to check out this beginner-friendly guide on freeCodeCamp

Almost all responses of queries are cached on the Edge. Cached data will automatically be purged if you mutate the data. For example, if you request a post of your blog:

The playground shows you if a response is cached or not. You can see it in the bottom right corner (MISS or HIT).

🚧 Important: You need to request the field id of each field. It is best practice to always request the id. If you don't do that it is possible that you get stale data.

We have a very generous rate limit in place which are as follows:

Almost all queries can be accessed without any authentication mechanism. Some sensitive fields need authentication. All mutations need an authentication header.

You can include an Authorization header in your request to access restricted fields. The value of the Authorization header needs to be your Personal Access Token (PAT).

You can test it in the GQL playground and click on the Headers tab to add the header.

To generate the token, go to https://hashnode.com/settings/developer and click on "Generate New Token".

Once the token is generated, simply pass it as Authorization header.

An example of a restricted query could be getting drafts inside any blog, it can only be queried by their respective owners.

Similarly, anyone can request user details but certain fields like unsubscribeCode and email require an authorization header to be present.

Please ensure that you pass the token when requesting restricted fields; otherwise, the API will throw an error.

GraphQL APIs use HTTP status codes to indicate the success or failure of a request. A 200 OK status code means the request was successful. In addition to HTTP status codes, GraphQL APIs also return error objects in response to specific errors.

These error objects have a code and message property. The code is a string that identifies the type of error. For example, you'll receive something like this if you try to request restricted fields without passing the authorization header.

Some of the error codes are:

You can check out this article to understand error codes in detail.

You must check for the presence of error objects along with error codes and messages to handle GraphQL errors in a structured way.

When handling extensive lists of items in an API, such as many blog posts, it's practical to fetch them in smaller sets rather than all at once. This process is known as pagination. For instance, if your blog has 500 posts, retrieving them all simultaneously can be inefficient. A better approach is to initially fetch a subset, like 10 posts, and then continue loading more in small groups.

Hashnode offers two distinct pagination methods, each suited for different scenarios:

Only one type of pagination is available for a query. You can distinguish the types of the type of response connection that is available. For cursor-based pagination the type PageInfo is available. For offset-based pagination the type OffsetPageInfo is available.

Cursor-based pagination is ideal for an infinite scrolling mechanism, where there is no fixed concept of pages. It uses a field named endCursor to keep track of the last item fetched. This cursor is then used to request subsequent items.

In this approach, the first API request does not include a cursor, and the API responds with the first set of results along with a new cursor. This new cursor is then utilized to fetch the next set of results.

In this example, edges contains a list of nodes (the data), and the pageInfo object provides pagination details. Use pageInfo.hasNextPage to check for more data and pageInfo.endCursor for subsequent requests.

For more information, visit Relay Pagination Specification.

Offset-based pagination is more traditional, involving distinct pages. It is suitable when you want to display data on specific pages or embed page information in URLs.

In this method, pageInfo includes information about the availability of next and previous pages, allowing for easy navigation between different sets of data.

Breaking changes, while rare, can occur. Our aim is to minimize them. Stay updated by joining our Discord server.

When a breaking change is imminent, rest assured, we'll notify you beforehand. Affected fields, queries, or mutations will be deprecated in advance, ensuring you're well-prepared for the upcoming change.

Thank you for your understanding and collaboration.

After the deprecation phase, our old legacy GraphQL API is now shutdown. To ensure that your apps are still working, follow this migration guide from the old API to the new API (gql.hashnode.com).

Replace the old API endpoint https://api.hashnode.com with the new GraphQL endpoint https://gql.hashnode.com.

If you were using authentication for the old API, ensure that your authentication mechanism remains valid for the new API. Check the documentation for how Authentication works in our GraphQL API.

Review your existing GraphQL queries and mutations. Some types and fields may have changed. Refer to the documentation for Examples and below to review the latest schema, query and mutation definitions.

If your application relies on pagination, ensure that you are using the updated pagination methods provided by the new API. We offer two kinds of pagination: Cursor-Based Pagination and Offset-Based Pagination. Review the pagination guide in the docs on how these two are working.

The new API might have different error responses or codes. Update your error handling mechanisms to accommodate any changes in error formats. You can check out this article to understand error codes in detail.

If you want to access a count of some entity we provide them via the field totalDocuments on the connection of the attribute.

Let's see an example:

The result looks like that:

The field totalDocuments shows you how many series are in the publication with the host engineering.hashnode.com. The totalDocuments field doesn't refer to how many items you request with first. This is independent of each other.

We don't expose this field for all connections, but for most of them.

Let’s look at some examples which might help you get started:

The queries support pagination, and let you fetch a full list of the posts to recreate your blog home page.

As long as you have your publication hostname and article slug, you can fetch it like the above.

Returns a CheckCustomDomainAvailabilityResult!

Returns a CheckSubdomainAvailabilityResult!

Returns a DocumentationProject

Returns a draft by ID. Draft is a post that is not published yet.

Returns a paginated list of posts based on the provided filter. Used in Hashnode home feed.

Returns a FeedPostConnection!

Returns the current authenticated user. Only available to the authenticated user.

Returns post by ID. Can be used to render post page on blog.

Returns the publication with the given ID or host. User can pass anyone of them.

Returns a Publication

Get a scheduled post by ID.

Returns a ScheduledPost

Returns a paginated list of posts based on search query for a particular publication id.

Returns a SearchPostConnection!

Returns tag details by its slug.

Returns users who have most actively participated in discussions by commenting in the last 7 days.

Returns a CommenterUserConnection!

Returns the user with the username.

Mutation to accept an invite to a documentation project

Returns an AcceptInviteToDocumentationProjectPayload!

Accepts an invitation to join a publication. The user is added as a member of the publication.

Returns an AcceptInviteToPublicationPayload!

Accepts a role based invite and adds the user as a member of the publication. The user is assigned the role specified in the invite.

Returns an AcceptRoleBasedInvitePayload!

Adds a comment to a post.

Returns an AddCommentPayload!

Returns an AddContentBlockPayload!

Returns an AddCustomMdxComponentPayload!

Returns an AddDocumentationProjectCustomDomainPayload!

Adds a post to a series.

Returns an AddPostToSeriesPayload!

Adds a reply to a comment.

Returns an AddReplyPayload!

Returns a CancelScheduledDraftPayload!

Changes the role of a user in a publication.

Returns a ChangePublicationMemberRolePayload!

Changes the privacy state of a user in a publication. PRIVATE members are not visible on the members page while PUBLIC members are visible.

Returns a ChangePublicationMemberVisibilityPayload!

Returns a CreateDocumentationApiReferencePayload!

Returns a CreateDocumentationGuidePayload!

Returns a CreateDocumentationLinkPayload!

Returns a CreateDocumentationPageDraftPayload!

Returns a CreateDocumentationProjectPayload!

Returns a CreateDocumentationSectionPayload!

Creates a new draft for a post.

Returns a CreateDraftPayload!

Returns a CreateRedirectionRulePayload!

Creates a role based invite for a publication and returns a link to invite users to a publication.

Returns a CreateRoleBasedInviteForPublicationPayload!

Creates a new series.

Returns a CreateSeriesPayload!

Returns a CreateWebhookPayload!

Returns a DeleteContentBlockPayload!

Returns a DeleteCustomMdxComponentPayload!

Deletes a role based invite.

Returns a DeleteRoleBasedInvitePayload!

Returns a DeleteWebhookPayload!

Mutation to disable AI search for a documentation project

Returns a DisableDocumentationProjectAISearchPayload!

Returns a DisableDocumentationProjectHeadlessCmsPayload!

Mutation to enable AI search for a documentation project

Returns an EnableDocumentationProjectAISearchPayload!

Returns an EnableDocumentationProjectHeadlessCmsPayload!

Returns a FollowTagsPayload!

Will generate a authorization JWT to preview a docs project. A token is required to generate the JWT.

Returns a GenerateDocumentationProjectPreviewAuthorizationTokenPayload!

Will generate a token that can be exchanged as a JWT to preview a docs project. Only the owner or editors of the project can generate the token.

Returns a GenerateDocumentationProjectPreviewTokenPayload!

Mutation to invite an user to a documentation project

Returns an InviteDocumentationProjectAdminPayload!

Invites users to a publication. Either by username or email.

Returns an InviteUsersToPublicationPayload!

Returns a LikeCommentPayload!

Returns a LikePostPayload!

Returns a LikeReplyPayload!

Returns a MapDocumentationProjectCustomDomainWwwRedirectPayload!

Returns a MoveDocumentationSidebarItemPayload!

Returns a PublishDocumentationApiReferencePayload!

Publishes the default version of the guide.

Returns a PublishDocumentationGuidePayload!

Returns a PublishDocumentationPageDraftPayload!

Publishes an existing draft as a post.

Returns a PublishDraftPayload!

Returns a PublishPostPayload!

Returns a RecommendPublicationsPayload!

Resends an invitation to a user to join a publication. The user must have been previously invited. Sends an email to the user.

Returns a ReinviteUserToPublicationPayload!

Removes a comment from a post.

Returns a RemoveCommentPayload!

Returns a RemoveDocumentationGuidePayload!

Mutation to remove a documentation project. This will free the custom domain and subdomain and removes all guides and pages.

Returns a RemoveDocumentationProjectPayload!

Mutation to remove a prompt from the AI search

Returns a RemoveDocumentationProjectAIPromptPayload!

Returns a RemoveDocumentationProjectCustomDomainPayload!

Mutation to remove a Member from a Documentation Project

Returns a RemoveDocumentationProjectMemberPayload!

Returns a RemoveDocumentationSidebarItemPayload!

Returns a RemovePostPayload!

Removes a user from a teams publication.

Returns a RemovePublicationMemberPayload!

Returns a RemoveRecommendationPayload!

Returns a RemoveRedirectionRulePayload!

Removes a reply from a comment.

Returns a RemoveReplyPayload!

Returns a RemoveSeriesPayload!

Returns a RenameDocumentationGuideItemPayload!

Returns a RenameDocumentationSidebarItemPayload!

Returns a RescheduleDraftPayload!

Returns a ResendWebhookRequestPayload!

Restores a deleted post.

Returns a RestorePostPayload!

Returns a RetryDocumentationProjectCustomDomainVerificationPayload!

Mutation to revoke documentation project invite

Returns a RevokeInviteToDocumentationProjectPayload!

Revokes a user invitation that was sent to join a publication.

Returns a RevokeUserInviteToPublicationPayload!

Returns a SaveDocumentationPageDraftContentPayload!

Returns a ScheduleDraftPayload!

Returns a SetDocumentationSidebarItemVisibilityPayload!

Returns a SubscribeToNewsletterPayload!

Mutation to sync documentation API reference definition

Returns a SyncDocumentationProjectApiDefinitionPayload!

Toggle allowContributorEdits flag to allow or restrict external contributors to further edit published articles.

Returns a ToggleAllowContributorEditsPayload!

Update the follow state for the user that is provided via id or username. If the authenticated user does not follow the user, the mutation will follow the user. If the authenticated user already follows the user, the mutation will un-follow the user. Only available to the authenticated user.

Returns a ToggleFollowUserPayload!

Toggle GPT bot crawling feature.

Returns a ToggleGPTBotCrawlingPayload!

Toggles role based invite links' active status. Users can join the publication by the invite link only if it is active.

Returns a ToggleRoleBasedInviteLinksPayload!

Toggle text selection sharer feature.

Returns a ToggleTextSelectionSharerPayload!

Returns a TriggerWebhookTestPayload!

Returns an UnfollowTagsPayload!

Returns an UnsubscribeFromNewsletterPayload!

Updates a comment on a post.

Returns an UpdateCommentPayload!

Returns an UpdateContentBlockPayload!

Returns an UpdateCustomMdxComponentPayload!

Returns an UpdateDocumentationAppearancePayload!

Returns an UpdateDocumentationGeneralSettingsPayload!

Returns an UpdateDocumentationGuidePayload!

Returns an UpdateDocumentationIntegrationsPayload!

Returns an UpdateDocumentationLinkPayload!

Returns an UpdateDocumentationPageSettingsPayload!

Mutation to update the AI search prompts

Returns an UpdateDocumentationProjectAIPromptPayload!

Returns an UpdateDocumentationProjectSubdomainPayload!

Mutation to update a section in a guide

Returns an UpdateDocumentationSectionPayload!

Returns an UpdatePostPayload!

Returns an UpdateRedirectionRulePayload!

Returns an UpdateReplyPayload!

Updates a role based invite for a publication.

Returns an UpdateRoleBasedInvitePayload!

Returns an UpdateSeriesPayload!

Returns an UpdateWebhookPayload!

Returns a VerifyDocumentationProjectCustomDomainPayload!

The start date of the views. The time range will include this date (using >=).

Defaults to the unix epoch start (1970-01-01).

The end date of the views. The time range will include this date (using <=).

Defaults to the current date.

The input for accepting an invitation to join a documentation project.

Response to accepting an invitation to join a documentation project.

Response to accepting an invitation to join a publication.

Input to accept a role based invite.

Input to toggle role based invite links.

Contains the flag indicating if the audio blog feature is enabled or not. User can enable or disable the audio blog feature from the publication settings. Shows audio player on blogs if enabled.

The voice type for the audio blog.

Used when Audioblog feature is enabled. Contains URLs to the audioblog of the post.

The status of the backup i.e., success or failure.

A badge that the user has earned.

Contains information about banner image options of the post. Like URL of the banner image, attribution, etc.

Contains basic information about the beta feature. A beta feature is a feature that is not yet released to all users.

The Boolean scalar type represents true or false.

Input to change the role of a user in a publication.

Response to changing the role of a user in a publication.

Input to change the privacy state of a user in a publication.

Response to changing the privacy state of a user in a publication.

Contains the flag indicating if the collaboration feature is enabled or not.

Contains basic information about the comment. A comment is a response to a post.

The number of replies to return. Max is 50.

Returns the elements in the list that come after the specified cursor.

Connection to get list of replies to a comment. Returns a list of edges which contains the posts in publication and cursor to the last item of the previous page.

An edge that contains a node of type reply and cursor to the node.

Connection to get list of top commenters. Contains a list of edges containing nodes. Each node is a user who commented recently. Page info contains information about pagination like hasNextPage and endCursor.

Connection to get list of items. Returns a list of edges which contains the items and cursor to the last item of the previous page. This is a common interface for all connections.

UserPublicationsConnection

CommenterUserConnection

PostCommenterConnection

PostCommentConnection

PublicationPostConnection

CommentReplyConnection

WebhookMessageConnection

ProjectViewsConnection

ProjectVisitorsConnection

Two letter ISO 3166-1 alpha-2 country code.

Contains information about cover image options of the post. Like URL of the cover image, attribution, etc.

The slug of the version the new link should be created in.

Defaults to the default version slug.

The slug of the version the new page should be created in.

Defaults to the default version slug.

The input for creating a documentation preview page

The slug of the version the new section should be created in.

Defaults to the default version slug.

Publish the draft on behalf of another user who is a member of the publication.

Only applicable for team publications.

A tag id that is referencing an existing tag.

Either this or name and slug should be provided. If both are provided, the id will be used.

A slug of a new tag to create.

Either this and name or id should be provided. If both are provided, the id will be used.

A name of a new tag to create.

Either this and slug or id should be provided. If both are provided, the id will be used.

Input to create a role based invite for a publication.

Response to creating a role based invite for a publication.

Contains the publication's dark mode preferences.

A date-time string at UTC, such as 2007-12-03T10:15:30Z, compliant with the date-time format outlined in section 5.6 of the RFC 3339 profile of the ISO 8601 standard for representation of dates and times using the Gregorian calendar.

Input to delete a role based invite.

Response to deleting a role based invite.

The input for disabling AI search for a documentation project

The response to disabling AI search for a documentation project

Contains basic information about the docs custom page. Docs custom pages are pages that can be written in mdx and can be added to docs. It can be used for changelog or other such requirements.

GroupedByDocsGuideViews

GroupedByDocsPageViews

GroupedByDocsTimeViews

GroupedByDocsPathViews

GroupedByDocsOperatingSystemViews

GroupedByDocsDeviceTypeViews

GroupedByDocsBrowserViews

GroupedByDocsCountryViews

GroupedByDocsReferrerHostViews

UngroupedDocsVisitors

GroupedByDocsGuideVisitors

GroupedByDocsTimeVisitors

GroupedByDocsPathVisitors

GroupedByDocsOperatingSystemVisitors

GroupedByDocsDeviceTypeVisitors

GroupedByDocsBrowserVisitors

GroupedByDocsCountryVisitors

GroupedByDocsReferrerHostVisitors

GroupedByDocsPageVisitors

A guide can be locked if the subscription doesn't cover to having this guide.

A locked guide is readonly. It can only be removed or edited after subscribing.

A guide can be locked if the subscription doesn't cover to having this guide.

A locked guide is readonly. It can only be removed or edited after subscribing.

URL of the published guide.

Example: https://example.com/my-guide-slug

Only published page of any version of this guide. The path may include the version slug.

Takes redirects into account and may return the page that the requested page redirects to.

If the path is only a version slug, it will redirect to the first page of that version.

DocumentationApiReference

Visibility options for documentation guides.

A column for the navigation. Used in the footer

DocumentationNavbarItemLink

DocumentationNavbarItemGuide

DocumentationNavbarItemPage

A navigation item pointing to a guide.

A navigation item pointing to an external URL.

A navigation item pointing to an custom page

URL of the published page.

Returns null if the page is not published.

The number of members to return on a single page.

The page number that should be returned.

Filters to be applied to the member list.

The slug of the docs custom page to retrieve.

The number of custom pages to return in a single page.

The page number that should be returned.

The number of pending invites to return on a single page.

The page number that should be returned.

The number of view nodes to be returned per page.

A cursor to the last item of the previous page.

The number of view nodes to be returned per page.

A cursor to the last item of the previous page.

Contains the documentation project's beta features.

Contains the pending invite information.

The filter for the documentation member connection.

Contains the header and footer navigation for the documentation project.

A connection for the user search result.

A connection for the user search result.

DocumentationSidebarItemPage

URL of the published page.

Returns null if the page is not published.

Contains the publication's domain information.

The subdomain of the publication on hashnode.dev.

It will redirect to you custom domain if it is present and ready.

Contains the publication's domain status.

Contains basic information about the draft. A draft is a post that is not published yet.

Returns the user details of the co-authors of the post.

Only available for team publications.

Whether or not the draft has been submitted for review.

Only applicable to drafts in team publications.

Contains information about the banner image of the draft.

Contains basic information about a Tag within a Draft. A tag in a draft is a tag that is not published yet.

Connection to get list of drafts. Returns a list of edges which contains the draft and cursor to the last item of the previous page.

Contains information about the cover image of the draft.

An edge that contains a node of type draft and cursor to the node.

An edge that contains a node and cursor to the node. This is a common interface for all edges.

RecommendedPublicationEdge

PublicationVisitorsEdge

The input for the email import acknowledgement mutation.

Contains information about the email import.

The status of the email import.

User's email notification preferences.

The input for enabling AI search for a documentation project

The response to enabling AI search for a documentation project

Invitations that failed to be sent to the user

Common fields that describe a feature.

TextSelectionSharerFeature

GPTBotCrawlingFeature

TableOfContentsFeature

Connection for posts within a feed. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Contains information about type of feed to be returned.

Returns only posts of the users you follow or publications you have subscribed to.

Note: You have to be authenticated to use this feed type.

Returns only posts based on users following and interactions.

Personalised feed is curated per requesting user basis.

The Float scalar type represents signed double-precision fractional values as specified by IEEE 754.

The input for the exchange of token to a JWT to preview token for a documentation project.

The payload for the exchange of token to a JWT to preview token for a documentation project.

The input for the generation of a exchangeable preview token for a documentation project.

The payload for the generation of a exchangeable preview token for a documentation project.

Contains the flag indicating if the GitHub sync feature is enabled or not.

Views implementation that will be returned if grouping by browser.

Visitors implementation that will be returned if grouping by browser.

Views implementation that will be returned if grouping by country.

Visitors implementation that will be returned if grouping by country.

Views implementation that will be returned if grouping by device type.

Visitors implementation that will be returned if grouping by device type.

Views implementation that will be returned if grouping by browser.

Visitors implementation that will be returned if grouping by browser.

Views implementation that will be returned if grouping by country.

Visitors implementation that will be returned if grouping by country.

Views implementation that will be returned if grouping by device type.

Visitors implementation that will be returned if grouping by device type.

Grouped views by documentation guide or API reference guide.

Grouped visitors by documentation guide or API reference guide.

Views implementation that will be returned if grouping by operating system.

Visitors implementation that will be returned if grouping by operating system.

Visitors implementation that will be returned if grouping by docs page.

Views implementation that will be returned if grouping by path.

Visitors implementation that will be returned if grouping by path.

Views implementation that will be returned if grouping by REFERRER_HOST dimension.

Visitors implementation that will be returned if grouping by REFERRER_HOST dimension.

Visitors implementation that will be returned if a grouping by time is provided.

Views implementation that will be returned if grouping by operating system.

Visitors implementation that will be returned if grouping by operating system.

Views implementation that will be returned if grouping by page.

Visitors implementation that will be returned if grouping by page.

Views implementation that will be returned if grouping by path.

Visitors implementation that will be returned if grouping by path.

Views implementation that will be returned if grouping by post.

Visitors implementation that will be returned if grouping by post.

Views implementation that will be returned if grouping by REFERRER_HOST dimension.

Visitors implementation that will be returned if grouping by REFERRER_HOST dimension.

Visitors implementation that will be returned if a grouping by time is provided.

The ID scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as "4") or integer (such as 4) input value will be accepted as an ID.

DocumentationSidebarItemPage

DocumentationSidebarItemPage

A guide can be locked if the subscription doesn't cover to having this guide.

A locked guide is readonly. It can only be removed or edited after subscribing.

DocumentationApiReference

Indicates if this is the default version.

There is always exactly one default version at a given time.

Contains basic information about the tag. A tag is a label that categorizes posts with similar topics.

Basic information about a user on Hashnode.

The maximum number of publications to return in a batch.

The cursor to start the query from.

The sort direction for the publication.

Filter to apply to the publications.

The number of posts to return on a single page.

The page number that should be returned.

The sort direction for the posts.

The filters to be applied to the post list.

The number of users to return on a single page.

The page number that should be returned.

The number of users to return on a single page.

The page number that should be returned.

The number of tags to return on a single page.

The page number that should be returned.

The Int scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

Input to invite users to a publication.

Response to inviting users to a publication.

Contains information about meta tags. Used for SEO purpose.

Basic information about the authenticated user. User must be authenticated to use this type.

The maximum number of publications to return in a batch.

The cursor to start the query from.

The sort direction for the publication.

Filter to apply to the publications.

The number of posts to return on a single page.

The page number that should be returned.

The sort direction for the posts based on the publish dates.

The filters to be applied to the post list.

The number of posts to return on a single page.

The page number that should be returned.

The number of posts to return on a single page.

The page number that should be returned.

The number of posts to return.

A cursor to the last item in the previous page.

The number of tags to return on a single page.

The page number that should be returned.

Contains the flag indicating if the newsletter feature is enabled or not. User can enable or disable the newsletter feature from the publication settings. Shows a newsletter prompt on blog if enabled.

Node is a common interface for all types example User, Post, Comment, etc.

DocumentationProjectCustomComponent

DocumentationProjectContentBlock

DocumentationProjectInvite

DocumentationProjectMemberV2

DocumentationNavbarItemLink

DocumentationNavbarItemGuide

DocumentationNavbarItemPage

DocumentationNavbarColumn

GroupedByTimeVisitors

GroupedByPostVisitors

GroupedByPageVisitors

GroupedByPathVisitors

GroupedByOperatingSystemVisitors

GroupedByDeviceTypeVisitors

GroupedByBrowserVisitors

GroupedByCountryVisitors

GroupedByReferrerHostVisitors

GroupedByOperatingSystemViews

GroupedByDeviceTypeViews

GroupedByBrowserViews

GroupedByCountryViews

GroupedByReferrerHostViews

GroupedByDocsGuideViews

GroupedByDocsPageViews

GroupedByDocsTimeViews

GroupedByDocsPathViews

GroupedByDocsOperatingSystemViews

GroupedByDocsDeviceTypeViews

GroupedByDocsBrowserViews

GroupedByDocsCountryViews

UngroupedDocsVisitors

GroupedByDocsGuideVisitors

GroupedByDocsTimeVisitors

GroupedByDocsReferrerHostViews

GroupedByDocsPathVisitors

GroupedByDocsOperatingSystemVisitors

GroupedByDocsDeviceTypeVisitors

GroupedByDocsBrowserVisitors

GroupedByDocsCountryVisitors

GroupedByDocsReferrerHostVisitors

GroupedByDocsPageVisitors

A field whose value conforms with the standard mongodb object Id as described here: https://docs.mongodb.com/manual/reference/method/ObjectId/#ObjectId. Example: 5e5677d71bdc2ae76344968c

Contains information to help in pagination for page based pagination.

Information to help in open graph related meta tags.

A Connection for page based pagination to get a list of items. Returns a list of nodes which contains the items. This is a common interface for all page connections.

PublicationUserRecommendingPublicationConnection

PublicationMemberConnection

PublicationPostPageConnection

DocumentationProjectMemberConnection

DocumentationProjectSearchUserConnection

DocumentationProjectPendingInviteConnection

DocsCustomPageConnection

PendingInviteConnection

RoleBasedInviteConnection

An edge that contains a node and is used in page based pagination. This is a common interface for all edges in page based pagination.

DocumentationProjectSearchUserEdge

Contains information to help in pagination.

Contains the preferences publication's autogenerated pages. Used to enable or disable pages like badge, newsletter and members.

Contains the pending invite information.

Contains basic information about the tag returned by popularTags query.

Contains a tag and a cursor for pagination.

Contains basic information about the post. A post is a published article on Hashnode.

The previous slugs of the post. Only present if the slug has been changed.

This could be used to create redirects for all posts from all previous slugs to the current slug.

The latest slug is always the first element in the array.

The number of users to be returned per page.

A cursor to the last item of the previous page.

The sorting option for commenters. Used to sort commenters by popularity or recency.

The number of comments to be returned per page.

A cursor to the last item of the previous page.

The sorting option for comments. Used to sort comments by top or recent.

Flag to indicate if the post is bookmarked by the requesting user.

Returns false if the user is not authenticated.

The number of users to be returned per page.

A cursor to the last item of the previous page.

Whether or not the authenticated user is following this post.

Returns null if the user is not authenticated.

The author type of a post from a user's perspective

FEATURED_DAILY_DOT_DEV

Contains information about the banner image of the post.

Connection for comments. Contains a list of edges containing nodes. Each node holds a comment. Page info contains information about pagination like hasNextPage and endCursor. Total documents contains the total number of comments.

A comment on the post. Contains information about the content of the comment, user who commented, etc.

Sorting options for comments. Used to sort comments by top or recent.

Connection for commenters (users). Contains a list of edges containing nodes. Each node holds commenter. Page info contains information about pagination like hasNextPage and endCursor. Total documents contains the total number of commenters.

A commenter on the post. Contains information about the user who commented.

Sorting options for commenters. Used to sort commenters by popularity or recency.

Contains information about the cover image of the post.

Contains a post and a cursor for pagination.

Connection for users who liked the post. Contains a list of edges containing nodes. Each node is a user who liked the post. Page info contains information about pagination like hasNextPage and endCursor. Total documents contains the total number of users who liked the post.

A user who liked the post. Contains information about the user and number of reactions added by the user.

Contains Post preferences. Used to determine if the post is pinned to blog, comments are disabled, or cover image is sticked to bottom.

Contains the publication's preferences for layout, theme and other personalisations.

Filter for project views.

Individual filters are combined with an AND condition whereas multiple values for the same filter are combined with an OR condition.

Example: documentationGuideIds: ["1", "2"], operatingSystems: ["Mac OS"] will return views for posts with ID 1 or 2 AND operating system Mac OS.

Filter by one or multiple documentation guide IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple api reference guide IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple page IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple paths.

If multiple paths are provided, the filter will be applied as an OR condition.

Filter by one or multiple operating systems.

If multiple operating systems are provided, the filter will be applied as an OR condition.

Filter by one or multiple device types.

If multiple device types are provided, the filter will be applied as an OR condition.

Filter by one or multiple browsers.

If multiple browsers are provided, the filter will be applied as an OR condition.

Filter by one or multiple countries.

If multiple countries are provided, the filter will be applied as an OR condition.

Filter by one or multiple referrer hosts.

If multiple referrer hosts are provided, the filter will be applied as an OR condition.

Group by one analytics dimensions.

Can not be used together with granularity.

Group by time. Without this, all views over time will be aggregated.

Can not be used together with dimension.

The timezone that is used for grouping the views by time. E.g. if you group by day, the timezone will be used to determine the start of the day as indicated by to and from.

It has no effect outside of time grouping.

Filter for project visitors.

Individual filters are combined with an AND condition whereas multiple values for the same filter are combined with an OR condition.

Example: documentationGuideIds: ["1", "2"], operatingSystems: ["Mac OS"] will return visitors for posts with ID 1 or 2 AND operating system Mac OS.

Filter by one or multiple documentation guide IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple api reference guide IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple page IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple paths.

If multiple paths are provided, the filter will be applied as an OR condition.

Filter by one or multiple operating systems.

If multiple operating systems are provided, the filter will be applied as an OR condition.

Filter by one or multiple device types.

If multiple device types are provided, the filter will be applied as an OR condition.

Filter by one or multiple browsers.

If multiple browsers are provided, the filter will be applied as an OR condition.

Filter by one or multiple countries.

If multiple countries are provided, the filter will be applied as an OR condition.

Filter by one or multiple referrer hosts.

If multiple referrer hosts are provided, the filter will be applied as an OR condition.

Group by one analytics dimensions.

Can not be used together with granularity.

Group by time. Without this, all views over time will be aggregated.

Can not be used together with dimension.

The timezone that is used for grouping the views by time. E.g. if you group by day, the timezone will be used to determine the start of the day as indicated by to and from.

It has no effect outside of time grouping.

Contains basic information about the publication. A publication is a blog that can be created for a user or a team.

The number of series to return.

A cursor to the last item in the previous page.

The number of posts to return.

A cursor to the last item in the previous page.

The filters to be applied to the post list.

The number of posts to return on a single page.

The page number that should be returned.

The filters to be applied to the post list.

Returns a post by a previous slug. It does not resolve a post by its current slug.

If a slug has been changed, we'll create a redirect from the old slug to the new one. With redirectedPost you can resolve a post by the old slug.

This can be used to redirect a user to the new post slug (via redirectedPost.slug).

The number of drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the draft list.

The number of drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the draft list.

The number of scheduled drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the draft list.

The number of scheduled drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the scheduled draft list.

The slug of the static page to retrieve.

The number of static pages to return.

A cursor to the last item in the previous page.

The number of submitted drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the draft list.

The number of members to return on a single page.

The page number that should be returned.

Filters to be applied to the member list.

The number of members to return on a single page.

The page number that should be returned.

Connection to get list of drafts in publications. Returns a list of edges which contains the drafts in publication and cursor to the last item of the previous page.

Contains the publication's beta features.

Contains the publication's integrations. Used to connect the publication with third party services like Google Analytics, Facebook Pixel, etc.

Contains the publication invite information.

The number of pending invites to return on a single page.

The page number that should be returned.

The number of role based invites to return on a single page.

The page number that should be returned.

Contains publication's layout choices.

Contains the publication's social media links.

Contains the publication member information.

The filter for the publication member connection.

Publication member privacy state on members page

Contains the publication's navbar items.

The type of the navbar item, can be series, link or page.

Connection for posts within a publication. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Connection to get list of posts in publications. Returns a list of edges which contains the posts in publication and cursor to the last item of the previous page.

Filtering by tag slugs and tag IDs will return posts that match either of the filters.

It is an "OR" filter and not an "AND" filter.

Filtering by tag slugs and tag IDs will return posts that match either of the filters.

It is an "OR" filter and not an "AND" filter.

Filtering by tag slugs and tag IDs will return posts that match either of the filters.

It is an "OR" filter and not an "AND" filter.

Filtering by tag slugs and tag IDs will return posts that match either of the filters.

It is an "OR" filter and not an "AND" filter.

ConnectionFilter to get list of drafts in publications. The filters are combined with an "AND" operation.

Contains the publication's Sponsorship information. User can sponsor their favorite publications and pay them directly using Stripe.

Contains information about the post to be published.

Publish the post on behalf of another user who is a member of the publication.

Only applicable for team publications.

A tag id that is referencing an existing tag.

Either this or name and slug should be provided. If both are provided, the id will be used.

A slug of a new tag to create.

Either this and name or id should be provided. If both are provided, the id will be used.

A name of a new tag to create.

Either this and slug or id should be provided. If both are provided, the id will be used.

Contains the flag indicating if the read time feature is enabled or not. User can enable or disable the read time feature from the publication settings. Shows read time on blogs if enabled.

Contains a publication and a cursor for pagination.

Input to reinvite a user to a publication.

Response to reinviting a user to a publication.

The input for removing a prompt from the AI search

Response to removing a prompt from the AI search

The input for removing a documentation project.

The input for the removal of a member from a documentation

The payload for removing a documentation project.

Input to remove a user from a publication.

Response to removing a user from a publication.

Contains basic information about the reply. A reply is a response to a comment.

Input to revoke a user invitation to join a documentation project.

Response to revoking an invitation to join a documentation project.

Input to revoke a user invitation to a publication.

Response to revoking a user invitation to a publication.

Contains the role based invite information.

Information to help in seo related meta tags.

Contains basic information about the scheduled post. A scheduled post is a post that is scheduled to be published in the future.

Enum of all the scopes that can be used with the @requireAuth directive.

import_subscribers_to_publication

acknowledge_email_import

recommend_publications

reject_draft_submission

write_ai_search_prompt

Connection for posts within a publication search. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Contains basic information about the series. A series is a collection of posts that are related to each other.

The number of posts to return.

The cursor after which the posts are to be returned.

Connection for Series. Contains a list of edges containing nodes. Each node is a Series. Page info contains information about pagination like hasNextPage and endCursor.

Contains a Series and a cursor for pagination.

Connection for posts within a series. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Available social media links.

SortOrder is a common enum for all types that can be sorted.

Contains basic information about the static page. Static pages are pages that are written in markdown and can be added to blog.

Connection to get list of static pages. Returns a list of edges which contains the static page and cursor to the last item of the previous page.

An edge that contains a node of type static page and cursor to the node.

The String scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.

Contains the publication's Stripe configuration.

The input for syncing API reference definitions

The response to syncing documentation project API Reference definition

The number of posts in particular tag to return per page.

The cursor after which the posts are to be returned.

The cursor before which the posts are to be returned.

Contains a tag and a cursor for pagination.

The field by which to sort the tag feed.

Contains the flag indicating if the text selection sharer feature is enabled or not. User can enable or disable the text selection sharer feature from the publication settings. Shows a widget if a text on a blog post is selected. Allows for easy sharing or copying of the selected text.

Narrow the time range to a specific period.

Can't be used with relative.

Narrow the time range to a specific period.

Can't be used with absolute.

A field whose value exists in the standard IANA Time Zone Database: https://www.iana.org/time-zones

Payload for the toggleFollowingUser mutation.

Response to toggling role based invite links.

Views implementation that will be returned if no grouping is applied.

Visitors implementation that will be returned if no grouping is applied.

Views implementation that will be returned if no grouping is applied.

Visitors implementation that will be returned if no grouping is applied.

The input for updating the AI search prompts

Response to updating the AI search prompts

Input to update a role based invite.

Response to updating a role based invite for a publication.

Basic information about a user on Hashnode.

The maximum number of publications to return in a batch.

The cursor to start the query from.

The sort direction for the publication.

Filter to apply to the publications.

The number of posts to return on a single page.

The page number that should be returned.

The sort direction for the posts based on the publish dates.

The filters to be applied to the post list.

The number of posts to return on a single page.

The page number that should be returned.

The number of posts to return on a single page.

The page number that should be returned.

The number of tags to return on a single page.

The page number that should be returned.

Connection for users to another user. Contains a list of nodes. Each node is a user. Page info contains information about pagination like hasNextPage and endCursor.

Drafts that belong to a user.

A generic type which holds a draft during pagination.

Contains a node of type user and cursor for pagination.

Connection for posts written by a single user. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Filter for the posts of a user.

Only include posts that reference the provided tag IDs.

Filtering by tags and tagSlugs will filter posts that match either of those two filters.

Only include posts that reference the provided tag slugs.

Filtering by tags and tagSlugs will filter posts that match either of those two filters.

Contains a post and the author status.

Filter for the posts of a user.

Sorting for the posts of a user.

The invited role of the user in the publication.

The role of the user in the publication.

Connection to get list of publications. Returns a list of edges which contains the publications and cursor to the last item of the previous page.

Filter to apply to the publications.

An edge that contains a node of type publication and cursor to the node.

Sorting for the publications of a user.

Role of the user within Hashnode

Contains the flag indicating if the Versioning feature is enabled or not.

Contains the flag indicating if the view count feature is enabled or not. User can enable or disable the view count feature from the publication settings. Shows total views on blogs if enabled.

GroupedByOperatingSystemViews

GroupedByDeviceTypeViews

GroupedByBrowserViews

GroupedByCountryViews

GroupedByReferrerHostViews

GroupedByTimeVisitors

GroupedByPostVisitors

GroupedByPageVisitors

GroupedByPathVisitors

GroupedByOperatingSystemVisitors

GroupedByDeviceTypeVisitors

GroupedByBrowserVisitors

GroupedByCountryVisitors

GroupedByReferrerHostVisitors

The number of items to be returned per page.

A cursor to the last item of the previous page.

STATIC_PAGE_PUBLISHED

**Examples:**

Example 1 (graphql):
```graphql
query Publication($first: Int!, $host: String) {
    publication(host: $host) {
        drafts(first: $first) {
            edges {
                node {
                    title
                }
            }
        }
    }
}
```

Example 2 (json):
```json
{
    "errors": [
        {
            "message": "You must be authenticated.",
            "locations": [
                {
                    "line": 2,
                    "column": 3
                }
            ],
            "path": ["me"],
            "extensions": {
                "code": "UNAUTHENTICATED"
            }
        }
    ],
    "data": null
}
```

Example 3 (graphql):
```graphql
query Publication {
    publication(host: "blog.developerdao.com") {
        isTeam
        title
        posts(
            first: 10
            after: "NjQxZTc4NGY0M2NiMzc2YjAyNzNkMzU4XzIwMjMtMDMtMjVUMDQ6Mjc6NTkuNjQxWg=="
        ) {
            edges {
                node {
                    title
                    brief
                    url
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
}
```

Example 4 (gql):
```gql
query Followers {
    user(username: "SandroVolpicella") {
        id
        followers(pageSize: 10, page: 1) {
            pageInfo {
                hasNextPage
                hasPreviousPage
                previousPage
                nextPage
            }
        }
    }
}
```

---

## Hashnode Public API Docs

**URL:** https://apidocs.hashnode.com/

**Contents:**
- Hashnode Public API Docs
- Welcome
- GQL Playground
- Caching
- Rate Limits
- Authentication
- Status and Error Codes
- Pagination
- 1. Cursor-Based Pagination
  - Example Query in GraphQL

This document describes the Hashnode Public API. The Hashnode Public API is a GraphQL API that allows you to interact with Hashnode.

Make sure to join our Discord server to be in the loop about any updates.

If you're seeing Errors with a 502 status code, it's highly likely that you are using api.hashnode.com. This was our legacy API and is now officially discontinued. Please use these docs and the migration guide to transition to our new GQL API.

All Hashnode Public API queries are made through a single GraphQL endpoint, which only accepts POST requests.

https://gql.hashnode.com

You can visit the same URL to check out Hashnode API Playground.

You can query user details, publication information, posts within publications, drafts, and more. Please explore the playground to view all available fields.

Additionally, mutations are at your disposal for actions such as publishing posts, subscribing to newsletters, and following users. The complete list of these available mutations can be found within the playground.

If you're not familiar with GraphQL, be sure to check out this beginner-friendly guide on freeCodeCamp

Almost all responses of queries are cached on the Edge. Cached data will automatically be purged if you mutate the data. For example, if you request a post of your blog:

The playground shows you if a response is cached or not. You can see it in the bottom right corner (MISS or HIT).

🚧 Important: You need to request the field id of each field. It is best practice to always request the id. If you don't do that it is possible that you get stale data.

We have a very generous rate limit in place which are as follows:

Almost all queries can be accessed without any authentication mechanism. Some sensitive fields need authentication. All mutations need an authentication header.

You can include an Authorization header in your request to access restricted fields. The value of the Authorization header needs to be your Personal Access Token (PAT).

You can test it in the GQL playground and click on the Headers tab to add the header.

To generate the token, go to https://hashnode.com/settings/developer and click on "Generate New Token".

Once the token is generated, simply pass it as Authorization header.

An example of a restricted query could be getting drafts inside any blog, it can only be queried by their respective owners.

Similarly, anyone can request user details but certain fields like unsubscribeCode and email require an authorization header to be present.

Please ensure that you pass the token when requesting restricted fields; otherwise, the API will throw an error.

GraphQL APIs use HTTP status codes to indicate the success or failure of a request. A 200 OK status code means the request was successful. In addition to HTTP status codes, GraphQL APIs also return error objects in response to specific errors.

These error objects have a code and message property. The code is a string that identifies the type of error. For example, you'll receive something like this if you try to request restricted fields without passing the authorization header.

Some of the error codes are:

You can check out this article to understand error codes in detail.

You must check for the presence of error objects along with error codes and messages to handle GraphQL errors in a structured way.

When handling extensive lists of items in an API, such as many blog posts, it's practical to fetch them in smaller sets rather than all at once. This process is known as pagination. For instance, if your blog has 500 posts, retrieving them all simultaneously can be inefficient. A better approach is to initially fetch a subset, like 10 posts, and then continue loading more in small groups.

Hashnode offers two distinct pagination methods, each suited for different scenarios:

Only one type of pagination is available for a query. You can distinguish the types of the type of response connection that is available. For cursor-based pagination the type PageInfo is available. For offset-based pagination the type OffsetPageInfo is available.

Cursor-based pagination is ideal for an infinite scrolling mechanism, where there is no fixed concept of pages. It uses a field named endCursor to keep track of the last item fetched. This cursor is then used to request subsequent items.

In this approach, the first API request does not include a cursor, and the API responds with the first set of results along with a new cursor. This new cursor is then utilized to fetch the next set of results.

In this example, edges contains a list of nodes (the data), and the pageInfo object provides pagination details. Use pageInfo.hasNextPage to check for more data and pageInfo.endCursor for subsequent requests.

For more information, visit Relay Pagination Specification.

Offset-based pagination is more traditional, involving distinct pages. It is suitable when you want to display data on specific pages or embed page information in URLs.

In this method, pageInfo includes information about the availability of next and previous pages, allowing for easy navigation between different sets of data.

Breaking changes, while rare, can occur. Our aim is to minimize them. Stay updated by joining our Discord server.

When a breaking change is imminent, rest assured, we'll notify you beforehand. Affected fields, queries, or mutations will be deprecated in advance, ensuring you're well-prepared for the upcoming change.

Thank you for your understanding and collaboration.

After the deprecation phase, our old legacy GraphQL API is now shutdown. To ensure that your apps are still working, follow this migration guide from the old API to the new API (gql.hashnode.com).

Replace the old API endpoint https://api.hashnode.com with the new GraphQL endpoint https://gql.hashnode.com.

If you were using authentication for the old API, ensure that your authentication mechanism remains valid for the new API. Check the documentation for how Authentication works in our GraphQL API.

Review your existing GraphQL queries and mutations. Some types and fields may have changed. Refer to the documentation for Examples and below to review the latest schema, query and mutation definitions.

If your application relies on pagination, ensure that you are using the updated pagination methods provided by the new API. We offer two kinds of pagination: Cursor-Based Pagination and Offset-Based Pagination. Review the pagination guide in the docs on how these two are working.

The new API might have different error responses or codes. Update your error handling mechanisms to accommodate any changes in error formats. You can check out this article to understand error codes in detail.

If you want to access a count of some entity we provide them via the field totalDocuments on the connection of the attribute.

Let's see an example:

The result looks like that:

The field totalDocuments shows you how many series are in the publication with the host engineering.hashnode.com. The totalDocuments field doesn't refer to how many items you request with first. This is independent of each other.

We don't expose this field for all connections, but for most of them.

Let’s look at some examples which might help you get started:

The queries support pagination, and let you fetch a full list of the posts to recreate your blog home page.

As long as you have your publication hostname and article slug, you can fetch it like the above.

Returns a CheckCustomDomainAvailabilityResult!

Returns a CheckSubdomainAvailabilityResult!

Returns a DocumentationProject

Returns a draft by ID. Draft is a post that is not published yet.

Returns a paginated list of posts based on the provided filter. Used in Hashnode home feed.

Returns a FeedPostConnection!

Returns the current authenticated user. Only available to the authenticated user.

Returns post by ID. Can be used to render post page on blog.

Returns the publication with the given ID or host. User can pass anyone of them.

Returns a Publication

Get a scheduled post by ID.

Returns a ScheduledPost

Returns a paginated list of posts based on search query for a particular publication id.

Returns a SearchPostConnection!

Returns tag details by its slug.

Returns users who have most actively participated in discussions by commenting in the last 7 days.

Returns a CommenterUserConnection!

Returns the user with the username.

Mutation to accept an invite to a documentation project

Returns an AcceptInviteToDocumentationProjectPayload!

Accepts an invitation to join a publication. The user is added as a member of the publication.

Returns an AcceptInviteToPublicationPayload!

Accepts a role based invite and adds the user as a member of the publication. The user is assigned the role specified in the invite.

Returns an AcceptRoleBasedInvitePayload!

Adds a comment to a post.

Returns an AddCommentPayload!

Returns an AddContentBlockPayload!

Returns an AddCustomMdxComponentPayload!

Returns an AddDocumentationProjectCustomDomainPayload!

Adds a post to a series.

Returns an AddPostToSeriesPayload!

Adds a reply to a comment.

Returns an AddReplyPayload!

Returns a CancelScheduledDraftPayload!

Changes the role of a user in a publication.

Returns a ChangePublicationMemberRolePayload!

Changes the privacy state of a user in a publication. PRIVATE members are not visible on the members page while PUBLIC members are visible.

Returns a ChangePublicationMemberVisibilityPayload!

Returns a CreateDocumentationApiReferencePayload!

Returns a CreateDocumentationGuidePayload!

Returns a CreateDocumentationLinkPayload!

Returns a CreateDocumentationPageDraftPayload!

Returns a CreateDocumentationProjectPayload!

Returns a CreateDocumentationSectionPayload!

Creates a new draft for a post.

Returns a CreateDraftPayload!

Returns a CreateRedirectionRulePayload!

Creates a role based invite for a publication and returns a link to invite users to a publication.

Returns a CreateRoleBasedInviteForPublicationPayload!

Creates a new series.

Returns a CreateSeriesPayload!

Returns a CreateWebhookPayload!

Returns a DeleteContentBlockPayload!

Returns a DeleteCustomMdxComponentPayload!

Deletes a role based invite.

Returns a DeleteRoleBasedInvitePayload!

Returns a DeleteWebhookPayload!

Mutation to disable AI search for a documentation project

Returns a DisableDocumentationProjectAISearchPayload!

Returns a DisableDocumentationProjectHeadlessCmsPayload!

Mutation to enable AI search for a documentation project

Returns an EnableDocumentationProjectAISearchPayload!

Returns an EnableDocumentationProjectHeadlessCmsPayload!

Returns a FollowTagsPayload!

Will generate a authorization JWT to preview a docs project. A token is required to generate the JWT.

Returns a GenerateDocumentationProjectPreviewAuthorizationTokenPayload!

Will generate a token that can be exchanged as a JWT to preview a docs project. Only the owner or editors of the project can generate the token.

Returns a GenerateDocumentationProjectPreviewTokenPayload!

Mutation to invite an user to a documentation project

Returns an InviteDocumentationProjectAdminPayload!

Invites users to a publication. Either by username or email.

Returns an InviteUsersToPublicationPayload!

Returns a LikeCommentPayload!

Returns a LikePostPayload!

Returns a LikeReplyPayload!

Returns a MapDocumentationProjectCustomDomainWwwRedirectPayload!

Returns a MoveDocumentationSidebarItemPayload!

Returns a PublishDocumentationApiReferencePayload!

Publishes the default version of the guide.

Returns a PublishDocumentationGuidePayload!

Returns a PublishDocumentationPageDraftPayload!

Publishes an existing draft as a post.

Returns a PublishDraftPayload!

Returns a PublishPostPayload!

Returns a RecommendPublicationsPayload!

Resends an invitation to a user to join a publication. The user must have been previously invited. Sends an email to the user.

Returns a ReinviteUserToPublicationPayload!

Removes a comment from a post.

Returns a RemoveCommentPayload!

Returns a RemoveDocumentationGuidePayload!

Mutation to remove a documentation project. This will free the custom domain and subdomain and removes all guides and pages.

Returns a RemoveDocumentationProjectPayload!

Mutation to remove a prompt from the AI search

Returns a RemoveDocumentationProjectAIPromptPayload!

Returns a RemoveDocumentationProjectCustomDomainPayload!

Mutation to remove a Member from a Documentation Project

Returns a RemoveDocumentationProjectMemberPayload!

Returns a RemoveDocumentationSidebarItemPayload!

Returns a RemovePostPayload!

Removes a user from a teams publication.

Returns a RemovePublicationMemberPayload!

Returns a RemoveRecommendationPayload!

Returns a RemoveRedirectionRulePayload!

Removes a reply from a comment.

Returns a RemoveReplyPayload!

Returns a RemoveSeriesPayload!

Returns a RenameDocumentationGuideItemPayload!

Returns a RenameDocumentationSidebarItemPayload!

Returns a RescheduleDraftPayload!

Returns a ResendWebhookRequestPayload!

Restores a deleted post.

Returns a RestorePostPayload!

Returns a RetryDocumentationProjectCustomDomainVerificationPayload!

Mutation to revoke documentation project invite

Returns a RevokeInviteToDocumentationProjectPayload!

Revokes a user invitation that was sent to join a publication.

Returns a RevokeUserInviteToPublicationPayload!

Returns a SaveDocumentationPageDraftContentPayload!

Returns a ScheduleDraftPayload!

Returns a SetDocumentationSidebarItemVisibilityPayload!

Returns a SubscribeToNewsletterPayload!

Mutation to sync documentation API reference definition

Returns a SyncDocumentationProjectApiDefinitionPayload!

Toggle allowContributorEdits flag to allow or restrict external contributors to further edit published articles.

Returns a ToggleAllowContributorEditsPayload!

Update the follow state for the user that is provided via id or username. If the authenticated user does not follow the user, the mutation will follow the user. If the authenticated user already follows the user, the mutation will un-follow the user. Only available to the authenticated user.

Returns a ToggleFollowUserPayload!

Toggle GPT bot crawling feature.

Returns a ToggleGPTBotCrawlingPayload!

Toggles role based invite links' active status. Users can join the publication by the invite link only if it is active.

Returns a ToggleRoleBasedInviteLinksPayload!

Toggle text selection sharer feature.

Returns a ToggleTextSelectionSharerPayload!

Returns a TriggerWebhookTestPayload!

Returns an UnfollowTagsPayload!

Returns an UnsubscribeFromNewsletterPayload!

Updates a comment on a post.

Returns an UpdateCommentPayload!

Returns an UpdateContentBlockPayload!

Returns an UpdateCustomMdxComponentPayload!

Returns an UpdateDocumentationAppearancePayload!

Returns an UpdateDocumentationGeneralSettingsPayload!

Returns an UpdateDocumentationGuidePayload!

Returns an UpdateDocumentationIntegrationsPayload!

Returns an UpdateDocumentationLinkPayload!

Returns an UpdateDocumentationPageSettingsPayload!

Mutation to update the AI search prompts

Returns an UpdateDocumentationProjectAIPromptPayload!

Returns an UpdateDocumentationProjectSubdomainPayload!

Mutation to update a section in a guide

Returns an UpdateDocumentationSectionPayload!

Returns an UpdatePostPayload!

Returns an UpdateRedirectionRulePayload!

Returns an UpdateReplyPayload!

Updates a role based invite for a publication.

Returns an UpdateRoleBasedInvitePayload!

Returns an UpdateSeriesPayload!

Returns an UpdateWebhookPayload!

Returns a VerifyDocumentationProjectCustomDomainPayload!

The start date of the views. The time range will include this date (using >=).

Defaults to the unix epoch start (1970-01-01).

The end date of the views. The time range will include this date (using <=).

Defaults to the current date.

The input for accepting an invitation to join a documentation project.

Response to accepting an invitation to join a documentation project.

Response to accepting an invitation to join a publication.

Input to accept a role based invite.

Input to toggle role based invite links.

Contains the flag indicating if the audio blog feature is enabled or not. User can enable or disable the audio blog feature from the publication settings. Shows audio player on blogs if enabled.

The voice type for the audio blog.

Used when Audioblog feature is enabled. Contains URLs to the audioblog of the post.

The status of the backup i.e., success or failure.

A badge that the user has earned.

Contains information about banner image options of the post. Like URL of the banner image, attribution, etc.

Contains basic information about the beta feature. A beta feature is a feature that is not yet released to all users.

The Boolean scalar type represents true or false.

Input to change the role of a user in a publication.

Response to changing the role of a user in a publication.

Input to change the privacy state of a user in a publication.

Response to changing the privacy state of a user in a publication.

Contains the flag indicating if the collaboration feature is enabled or not.

Contains basic information about the comment. A comment is a response to a post.

The number of replies to return. Max is 50.

Returns the elements in the list that come after the specified cursor.

Connection to get list of replies to a comment. Returns a list of edges which contains the posts in publication and cursor to the last item of the previous page.

An edge that contains a node of type reply and cursor to the node.

Connection to get list of top commenters. Contains a list of edges containing nodes. Each node is a user who commented recently. Page info contains information about pagination like hasNextPage and endCursor.

Connection to get list of items. Returns a list of edges which contains the items and cursor to the last item of the previous page. This is a common interface for all connections.

UserPublicationsConnection

CommenterUserConnection

PostCommenterConnection

PostCommentConnection

PublicationPostConnection

CommentReplyConnection

WebhookMessageConnection

ProjectViewsConnection

ProjectVisitorsConnection

Two letter ISO 3166-1 alpha-2 country code.

Contains information about cover image options of the post. Like URL of the cover image, attribution, etc.

The slug of the version the new link should be created in.

Defaults to the default version slug.

The slug of the version the new page should be created in.

Defaults to the default version slug.

The input for creating a documentation preview page

The slug of the version the new section should be created in.

Defaults to the default version slug.

Publish the draft on behalf of another user who is a member of the publication.

Only applicable for team publications.

A tag id that is referencing an existing tag.

Either this or name and slug should be provided. If both are provided, the id will be used.

A slug of a new tag to create.

Either this and name or id should be provided. If both are provided, the id will be used.

A name of a new tag to create.

Either this and slug or id should be provided. If both are provided, the id will be used.

Input to create a role based invite for a publication.

Response to creating a role based invite for a publication.

Contains the publication's dark mode preferences.

A date-time string at UTC, such as 2007-12-03T10:15:30Z, compliant with the date-time format outlined in section 5.6 of the RFC 3339 profile of the ISO 8601 standard for representation of dates and times using the Gregorian calendar.

Input to delete a role based invite.

Response to deleting a role based invite.

The input for disabling AI search for a documentation project

The response to disabling AI search for a documentation project

Contains basic information about the docs custom page. Docs custom pages are pages that can be written in mdx and can be added to docs. It can be used for changelog or other such requirements.

GroupedByDocsGuideViews

GroupedByDocsPageViews

GroupedByDocsTimeViews

GroupedByDocsPathViews

GroupedByDocsOperatingSystemViews

GroupedByDocsDeviceTypeViews

GroupedByDocsBrowserViews

GroupedByDocsCountryViews

GroupedByDocsReferrerHostViews

UngroupedDocsVisitors

GroupedByDocsGuideVisitors

GroupedByDocsTimeVisitors

GroupedByDocsPathVisitors

GroupedByDocsOperatingSystemVisitors

GroupedByDocsDeviceTypeVisitors

GroupedByDocsBrowserVisitors

GroupedByDocsCountryVisitors

GroupedByDocsReferrerHostVisitors

GroupedByDocsPageVisitors

A guide can be locked if the subscription doesn't cover to having this guide.

A locked guide is readonly. It can only be removed or edited after subscribing.

A guide can be locked if the subscription doesn't cover to having this guide.

A locked guide is readonly. It can only be removed or edited after subscribing.

URL of the published guide.

Example: https://example.com/my-guide-slug

Only published page of any version of this guide. The path may include the version slug.

Takes redirects into account and may return the page that the requested page redirects to.

If the path is only a version slug, it will redirect to the first page of that version.

DocumentationApiReference

Visibility options for documentation guides.

A column for the navigation. Used in the footer

DocumentationNavbarItemLink

DocumentationNavbarItemGuide

DocumentationNavbarItemPage

A navigation item pointing to a guide.

A navigation item pointing to an external URL.

A navigation item pointing to an custom page

URL of the published page.

Returns null if the page is not published.

The number of members to return on a single page.

The page number that should be returned.

Filters to be applied to the member list.

The slug of the docs custom page to retrieve.

The number of custom pages to return in a single page.

The page number that should be returned.

The number of pending invites to return on a single page.

The page number that should be returned.

The number of view nodes to be returned per page.

A cursor to the last item of the previous page.

The number of view nodes to be returned per page.

A cursor to the last item of the previous page.

Contains the documentation project's beta features.

Contains the pending invite information.

The filter for the documentation member connection.

Contains the header and footer navigation for the documentation project.

A connection for the user search result.

A connection for the user search result.

DocumentationSidebarItemPage

URL of the published page.

Returns null if the page is not published.

Contains the publication's domain information.

The subdomain of the publication on hashnode.dev.

It will redirect to you custom domain if it is present and ready.

Contains the publication's domain status.

Contains basic information about the draft. A draft is a post that is not published yet.

Returns the user details of the co-authors of the post.

Only available for team publications.

Whether or not the draft has been submitted for review.

Only applicable to drafts in team publications.

Contains information about the banner image of the draft.

Contains basic information about a Tag within a Draft. A tag in a draft is a tag that is not published yet.

Connection to get list of drafts. Returns a list of edges which contains the draft and cursor to the last item of the previous page.

Contains information about the cover image of the draft.

An edge that contains a node of type draft and cursor to the node.

An edge that contains a node and cursor to the node. This is a common interface for all edges.

RecommendedPublicationEdge

PublicationVisitorsEdge

The input for the email import acknowledgement mutation.

Contains information about the email import.

The status of the email import.

User's email notification preferences.

The input for enabling AI search for a documentation project

The response to enabling AI search for a documentation project

Invitations that failed to be sent to the user

Common fields that describe a feature.

TextSelectionSharerFeature

GPTBotCrawlingFeature

TableOfContentsFeature

Connection for posts within a feed. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Contains information about type of feed to be returned.

Returns only posts of the users you follow or publications you have subscribed to.

Note: You have to be authenticated to use this feed type.

Returns only posts based on users following and interactions.

Personalised feed is curated per requesting user basis.

The Float scalar type represents signed double-precision fractional values as specified by IEEE 754.

The input for the exchange of token to a JWT to preview token for a documentation project.

The payload for the exchange of token to a JWT to preview token for a documentation project.

The input for the generation of a exchangeable preview token for a documentation project.

The payload for the generation of a exchangeable preview token for a documentation project.

Contains the flag indicating if the GitHub sync feature is enabled or not.

Views implementation that will be returned if grouping by browser.

Visitors implementation that will be returned if grouping by browser.

Views implementation that will be returned if grouping by country.

Visitors implementation that will be returned if grouping by country.

Views implementation that will be returned if grouping by device type.

Visitors implementation that will be returned if grouping by device type.

Views implementation that will be returned if grouping by browser.

Visitors implementation that will be returned if grouping by browser.

Views implementation that will be returned if grouping by country.

Visitors implementation that will be returned if grouping by country.

Views implementation that will be returned if grouping by device type.

Visitors implementation that will be returned if grouping by device type.

Grouped views by documentation guide or API reference guide.

Grouped visitors by documentation guide or API reference guide.

Views implementation that will be returned if grouping by operating system.

Visitors implementation that will be returned if grouping by operating system.

Visitors implementation that will be returned if grouping by docs page.

Views implementation that will be returned if grouping by path.

Visitors implementation that will be returned if grouping by path.

Views implementation that will be returned if grouping by REFERRER_HOST dimension.

Visitors implementation that will be returned if grouping by REFERRER_HOST dimension.

Visitors implementation that will be returned if a grouping by time is provided.

Views implementation that will be returned if grouping by operating system.

Visitors implementation that will be returned if grouping by operating system.

Views implementation that will be returned if grouping by page.

Visitors implementation that will be returned if grouping by page.

Views implementation that will be returned if grouping by path.

Visitors implementation that will be returned if grouping by path.

Views implementation that will be returned if grouping by post.

Visitors implementation that will be returned if grouping by post.

Views implementation that will be returned if grouping by REFERRER_HOST dimension.

Visitors implementation that will be returned if grouping by REFERRER_HOST dimension.

Visitors implementation that will be returned if a grouping by time is provided.

The ID scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as "4") or integer (such as 4) input value will be accepted as an ID.

DocumentationSidebarItemPage

DocumentationSidebarItemPage

A guide can be locked if the subscription doesn't cover to having this guide.

A locked guide is readonly. It can only be removed or edited after subscribing.

DocumentationApiReference

Indicates if this is the default version.

There is always exactly one default version at a given time.

Contains basic information about the tag. A tag is a label that categorizes posts with similar topics.

Basic information about a user on Hashnode.

The maximum number of publications to return in a batch.

The cursor to start the query from.

The sort direction for the publication.

Filter to apply to the publications.

The number of posts to return on a single page.

The page number that should be returned.

The sort direction for the posts.

The filters to be applied to the post list.

The number of users to return on a single page.

The page number that should be returned.

The number of users to return on a single page.

The page number that should be returned.

The number of tags to return on a single page.

The page number that should be returned.

The Int scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.

Input to invite users to a publication.

Response to inviting users to a publication.

Contains information about meta tags. Used for SEO purpose.

Basic information about the authenticated user. User must be authenticated to use this type.

The maximum number of publications to return in a batch.

The cursor to start the query from.

The sort direction for the publication.

Filter to apply to the publications.

The number of posts to return on a single page.

The page number that should be returned.

The sort direction for the posts based on the publish dates.

The filters to be applied to the post list.

The number of posts to return on a single page.

The page number that should be returned.

The number of posts to return on a single page.

The page number that should be returned.

The number of posts to return.

A cursor to the last item in the previous page.

The number of tags to return on a single page.

The page number that should be returned.

Contains the flag indicating if the newsletter feature is enabled or not. User can enable or disable the newsletter feature from the publication settings. Shows a newsletter prompt on blog if enabled.

Node is a common interface for all types example User, Post, Comment, etc.

DocumentationProjectCustomComponent

DocumentationProjectContentBlock

DocumentationProjectInvite

DocumentationProjectMemberV2

DocumentationNavbarItemLink

DocumentationNavbarItemGuide

DocumentationNavbarItemPage

DocumentationNavbarColumn

GroupedByTimeVisitors

GroupedByPostVisitors

GroupedByPageVisitors

GroupedByPathVisitors

GroupedByOperatingSystemVisitors

GroupedByDeviceTypeVisitors

GroupedByBrowserVisitors

GroupedByCountryVisitors

GroupedByReferrerHostVisitors

GroupedByOperatingSystemViews

GroupedByDeviceTypeViews

GroupedByBrowserViews

GroupedByCountryViews

GroupedByReferrerHostViews

GroupedByDocsGuideViews

GroupedByDocsPageViews

GroupedByDocsTimeViews

GroupedByDocsPathViews

GroupedByDocsOperatingSystemViews

GroupedByDocsDeviceTypeViews

GroupedByDocsBrowserViews

GroupedByDocsCountryViews

UngroupedDocsVisitors

GroupedByDocsGuideVisitors

GroupedByDocsTimeVisitors

GroupedByDocsReferrerHostViews

GroupedByDocsPathVisitors

GroupedByDocsOperatingSystemVisitors

GroupedByDocsDeviceTypeVisitors

GroupedByDocsBrowserVisitors

GroupedByDocsCountryVisitors

GroupedByDocsReferrerHostVisitors

GroupedByDocsPageVisitors

A field whose value conforms with the standard mongodb object Id as described here: https://docs.mongodb.com/manual/reference/method/ObjectId/#ObjectId. Example: 5e5677d71bdc2ae76344968c

Contains information to help in pagination for page based pagination.

Information to help in open graph related meta tags.

A Connection for page based pagination to get a list of items. Returns a list of nodes which contains the items. This is a common interface for all page connections.

PublicationUserRecommendingPublicationConnection

PublicationMemberConnection

PublicationPostPageConnection

DocumentationProjectMemberConnection

DocumentationProjectSearchUserConnection

DocumentationProjectPendingInviteConnection

DocsCustomPageConnection

PendingInviteConnection

RoleBasedInviteConnection

An edge that contains a node and is used in page based pagination. This is a common interface for all edges in page based pagination.

DocumentationProjectSearchUserEdge

Contains information to help in pagination.

Contains the preferences publication's autogenerated pages. Used to enable or disable pages like badge, newsletter and members.

Contains the pending invite information.

Contains basic information about the tag returned by popularTags query.

Contains a tag and a cursor for pagination.

Contains basic information about the post. A post is a published article on Hashnode.

The previous slugs of the post. Only present if the slug has been changed.

This could be used to create redirects for all posts from all previous slugs to the current slug.

The latest slug is always the first element in the array.

The number of users to be returned per page.

A cursor to the last item of the previous page.

The sorting option for commenters. Used to sort commenters by popularity or recency.

The number of comments to be returned per page.

A cursor to the last item of the previous page.

The sorting option for comments. Used to sort comments by top or recent.

Flag to indicate if the post is bookmarked by the requesting user.

Returns false if the user is not authenticated.

The number of users to be returned per page.

A cursor to the last item of the previous page.

Whether or not the authenticated user is following this post.

Returns null if the user is not authenticated.

The author type of a post from a user's perspective

FEATURED_DAILY_DOT_DEV

Contains information about the banner image of the post.

Connection for comments. Contains a list of edges containing nodes. Each node holds a comment. Page info contains information about pagination like hasNextPage and endCursor. Total documents contains the total number of comments.

A comment on the post. Contains information about the content of the comment, user who commented, etc.

Sorting options for comments. Used to sort comments by top or recent.

Connection for commenters (users). Contains a list of edges containing nodes. Each node holds commenter. Page info contains information about pagination like hasNextPage and endCursor. Total documents contains the total number of commenters.

A commenter on the post. Contains information about the user who commented.

Sorting options for commenters. Used to sort commenters by popularity or recency.

Contains information about the cover image of the post.

Contains a post and a cursor for pagination.

Connection for users who liked the post. Contains a list of edges containing nodes. Each node is a user who liked the post. Page info contains information about pagination like hasNextPage and endCursor. Total documents contains the total number of users who liked the post.

A user who liked the post. Contains information about the user and number of reactions added by the user.

Contains Post preferences. Used to determine if the post is pinned to blog, comments are disabled, or cover image is sticked to bottom.

Contains the publication's preferences for layout, theme and other personalisations.

Filter for project views.

Individual filters are combined with an AND condition whereas multiple values for the same filter are combined with an OR condition.

Example: documentationGuideIds: ["1", "2"], operatingSystems: ["Mac OS"] will return views for posts with ID 1 or 2 AND operating system Mac OS.

Filter by one or multiple documentation guide IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple api reference guide IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple page IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple paths.

If multiple paths are provided, the filter will be applied as an OR condition.

Filter by one or multiple operating systems.

If multiple operating systems are provided, the filter will be applied as an OR condition.

Filter by one or multiple device types.

If multiple device types are provided, the filter will be applied as an OR condition.

Filter by one or multiple browsers.

If multiple browsers are provided, the filter will be applied as an OR condition.

Filter by one or multiple countries.

If multiple countries are provided, the filter will be applied as an OR condition.

Filter by one or multiple referrer hosts.

If multiple referrer hosts are provided, the filter will be applied as an OR condition.

Group by one analytics dimensions.

Can not be used together with granularity.

Group by time. Without this, all views over time will be aggregated.

Can not be used together with dimension.

The timezone that is used for grouping the views by time. E.g. if you group by day, the timezone will be used to determine the start of the day as indicated by to and from.

It has no effect outside of time grouping.

Filter for project visitors.

Individual filters are combined with an AND condition whereas multiple values for the same filter are combined with an OR condition.

Example: documentationGuideIds: ["1", "2"], operatingSystems: ["Mac OS"] will return visitors for posts with ID 1 or 2 AND operating system Mac OS.

Filter by one or multiple documentation guide IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple api reference guide IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple page IDs.

If multiple IDs are provided, the filter will be applied as an OR condition.

Filter by one or multiple paths.

If multiple paths are provided, the filter will be applied as an OR condition.

Filter by one or multiple operating systems.

If multiple operating systems are provided, the filter will be applied as an OR condition.

Filter by one or multiple device types.

If multiple device types are provided, the filter will be applied as an OR condition.

Filter by one or multiple browsers.

If multiple browsers are provided, the filter will be applied as an OR condition.

Filter by one or multiple countries.

If multiple countries are provided, the filter will be applied as an OR condition.

Filter by one or multiple referrer hosts.

If multiple referrer hosts are provided, the filter will be applied as an OR condition.

Group by one analytics dimensions.

Can not be used together with granularity.

Group by time. Without this, all views over time will be aggregated.

Can not be used together with dimension.

The timezone that is used for grouping the views by time. E.g. if you group by day, the timezone will be used to determine the start of the day as indicated by to and from.

It has no effect outside of time grouping.

Contains basic information about the publication. A publication is a blog that can be created for a user or a team.

The number of series to return.

A cursor to the last item in the previous page.

The number of posts to return.

A cursor to the last item in the previous page.

The filters to be applied to the post list.

The number of posts to return on a single page.

The page number that should be returned.

The filters to be applied to the post list.

Returns a post by a previous slug. It does not resolve a post by its current slug.

If a slug has been changed, we'll create a redirect from the old slug to the new one. With redirectedPost you can resolve a post by the old slug.

This can be used to redirect a user to the new post slug (via redirectedPost.slug).

The number of drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the draft list.

The number of drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the draft list.

The number of scheduled drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the draft list.

The number of scheduled drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the scheduled draft list.

The slug of the static page to retrieve.

The number of static pages to return.

A cursor to the last item in the previous page.

The number of submitted drafts to return.

A cursor to the last item in the previous page.

The filters to be applied to the draft list.

The number of members to return on a single page.

The page number that should be returned.

Filters to be applied to the member list.

The number of members to return on a single page.

The page number that should be returned.

Connection to get list of drafts in publications. Returns a list of edges which contains the drafts in publication and cursor to the last item of the previous page.

Contains the publication's beta features.

Contains the publication's integrations. Used to connect the publication with third party services like Google Analytics, Facebook Pixel, etc.

Contains the publication invite information.

The number of pending invites to return on a single page.

The page number that should be returned.

The number of role based invites to return on a single page.

The page number that should be returned.

Contains publication's layout choices.

Contains the publication's social media links.

Contains the publication member information.

The filter for the publication member connection.

Publication member privacy state on members page

Contains the publication's navbar items.

The type of the navbar item, can be series, link or page.

Connection for posts within a publication. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Connection to get list of posts in publications. Returns a list of edges which contains the posts in publication and cursor to the last item of the previous page.

Filtering by tag slugs and tag IDs will return posts that match either of the filters.

It is an "OR" filter and not an "AND" filter.

Filtering by tag slugs and tag IDs will return posts that match either of the filters.

It is an "OR" filter and not an "AND" filter.

Filtering by tag slugs and tag IDs will return posts that match either of the filters.

It is an "OR" filter and not an "AND" filter.

Filtering by tag slugs and tag IDs will return posts that match either of the filters.

It is an "OR" filter and not an "AND" filter.

ConnectionFilter to get list of drafts in publications. The filters are combined with an "AND" operation.

Contains the publication's Sponsorship information. User can sponsor their favorite publications and pay them directly using Stripe.

Contains information about the post to be published.

Publish the post on behalf of another user who is a member of the publication.

Only applicable for team publications.

A tag id that is referencing an existing tag.

Either this or name and slug should be provided. If both are provided, the id will be used.

A slug of a new tag to create.

Either this and name or id should be provided. If both are provided, the id will be used.

A name of a new tag to create.

Either this and slug or id should be provided. If both are provided, the id will be used.

Contains the flag indicating if the read time feature is enabled or not. User can enable or disable the read time feature from the publication settings. Shows read time on blogs if enabled.

Contains a publication and a cursor for pagination.

Input to reinvite a user to a publication.

Response to reinviting a user to a publication.

The input for removing a prompt from the AI search

Response to removing a prompt from the AI search

The input for removing a documentation project.

The input for the removal of a member from a documentation

The payload for removing a documentation project.

Input to remove a user from a publication.

Response to removing a user from a publication.

Contains basic information about the reply. A reply is a response to a comment.

Input to revoke a user invitation to join a documentation project.

Response to revoking an invitation to join a documentation project.

Input to revoke a user invitation to a publication.

Response to revoking a user invitation to a publication.

Contains the role based invite information.

Information to help in seo related meta tags.

Contains basic information about the scheduled post. A scheduled post is a post that is scheduled to be published in the future.

Enum of all the scopes that can be used with the @requireAuth directive.

import_subscribers_to_publication

acknowledge_email_import

recommend_publications

reject_draft_submission

write_ai_search_prompt

Connection for posts within a publication search. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Contains basic information about the series. A series is a collection of posts that are related to each other.

The number of posts to return.

The cursor after which the posts are to be returned.

Connection for Series. Contains a list of edges containing nodes. Each node is a Series. Page info contains information about pagination like hasNextPage and endCursor.

Contains a Series and a cursor for pagination.

Connection for posts within a series. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Available social media links.

SortOrder is a common enum for all types that can be sorted.

Contains basic information about the static page. Static pages are pages that are written in markdown and can be added to blog.

Connection to get list of static pages. Returns a list of edges which contains the static page and cursor to the last item of the previous page.

An edge that contains a node of type static page and cursor to the node.

The String scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.

Contains the publication's Stripe configuration.

The input for syncing API reference definitions

The response to syncing documentation project API Reference definition

The number of posts in particular tag to return per page.

The cursor after which the posts are to be returned.

The cursor before which the posts are to be returned.

Contains a tag and a cursor for pagination.

The field by which to sort the tag feed.

Contains the flag indicating if the text selection sharer feature is enabled or not. User can enable or disable the text selection sharer feature from the publication settings. Shows a widget if a text on a blog post is selected. Allows for easy sharing or copying of the selected text.

Narrow the time range to a specific period.

Can't be used with relative.

Narrow the time range to a specific period.

Can't be used with absolute.

A field whose value exists in the standard IANA Time Zone Database: https://www.iana.org/time-zones

Payload for the toggleFollowingUser mutation.

Response to toggling role based invite links.

Views implementation that will be returned if no grouping is applied.

Visitors implementation that will be returned if no grouping is applied.

Views implementation that will be returned if no grouping is applied.

Visitors implementation that will be returned if no grouping is applied.

The input for updating the AI search prompts

Response to updating the AI search prompts

Input to update a role based invite.

Response to updating a role based invite for a publication.

Basic information about a user on Hashnode.

The maximum number of publications to return in a batch.

The cursor to start the query from.

The sort direction for the publication.

Filter to apply to the publications.

The number of posts to return on a single page.

The page number that should be returned.

The sort direction for the posts based on the publish dates.

The filters to be applied to the post list.

The number of posts to return on a single page.

The page number that should be returned.

The number of posts to return on a single page.

The page number that should be returned.

The number of tags to return on a single page.

The page number that should be returned.

Connection for users to another user. Contains a list of nodes. Each node is a user. Page info contains information about pagination like hasNextPage and endCursor.

Drafts that belong to a user.

A generic type which holds a draft during pagination.

Contains a node of type user and cursor for pagination.

Connection for posts written by a single user. Contains a list of edges containing nodes. Each node is a post. Page info contains information about pagination like hasNextPage and endCursor.

Filter for the posts of a user.

Only include posts that reference the provided tag IDs.

Filtering by tags and tagSlugs will filter posts that match either of those two filters.

Only include posts that reference the provided tag slugs.

Filtering by tags and tagSlugs will filter posts that match either of those two filters.

Contains a post and the author status.

Filter for the posts of a user.

Sorting for the posts of a user.

The invited role of the user in the publication.

The role of the user in the publication.

Connection to get list of publications. Returns a list of edges which contains the publications and cursor to the last item of the previous page.

Filter to apply to the publications.

An edge that contains a node of type publication and cursor to the node.

Sorting for the publications of a user.

Role of the user within Hashnode

Contains the flag indicating if the Versioning feature is enabled or not.

Contains the flag indicating if the view count feature is enabled or not. User can enable or disable the view count feature from the publication settings. Shows total views on blogs if enabled.

GroupedByOperatingSystemViews

GroupedByDeviceTypeViews

GroupedByBrowserViews

GroupedByCountryViews

GroupedByReferrerHostViews

GroupedByTimeVisitors

GroupedByPostVisitors

GroupedByPageVisitors

GroupedByPathVisitors

GroupedByOperatingSystemVisitors

GroupedByDeviceTypeVisitors

GroupedByBrowserVisitors

GroupedByCountryVisitors

GroupedByReferrerHostVisitors

The number of items to be returned per page.

A cursor to the last item of the previous page.

STATIC_PAGE_PUBLISHED

**Examples:**

Example 1 (graphql):
```graphql
query Publication($first: Int!, $host: String) {
    publication(host: $host) {
        drafts(first: $first) {
            edges {
                node {
                    title
                }
            }
        }
    }
}
```

Example 2 (json):
```json
{
    "errors": [
        {
            "message": "You must be authenticated.",
            "locations": [
                {
                    "line": 2,
                    "column": 3
                }
            ],
            "path": ["me"],
            "extensions": {
                "code": "UNAUTHENTICATED"
            }
        }
    ],
    "data": null
}
```

Example 3 (graphql):
```graphql
query Publication {
    publication(host: "blog.developerdao.com") {
        isTeam
        title
        posts(
            first: 10
            after: "NjQxZTc4NGY0M2NiMzc2YjAyNzNkMzU4XzIwMjMtMDMtMjVUMDQ6Mjc6NTkuNjQxWg=="
        ) {
            edges {
                node {
                    title
                    brief
                    url
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
}
```

Example 4 (gql):
```gql
query Followers {
    user(username: "SandroVolpicella") {
        id
        followers(pageSize: 10, page: 1) {
            pageInfo {
                hasNextPage
                hasPreviousPage
                previousPage
                nextPage
            }
        }
    }
}
```

---
