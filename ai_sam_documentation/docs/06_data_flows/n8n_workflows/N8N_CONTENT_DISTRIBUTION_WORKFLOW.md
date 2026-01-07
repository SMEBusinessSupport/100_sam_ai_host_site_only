# N8N Content Distribution Automation Workflow
**Purpose:** Automate SAM campaign distribution across 8 channels
**Source:** Information Memorandum → Multi-Channel Posts
**Agent:** AI-powered content transformation and scheduling

---

## 🎯 Workflow Overview

```
[Information Memorandum]
    → [AI Content Processor]
    → [8 Parallel Distribution Paths]
    → [Platform-Specific APIs]
    → [Performance Tracking]
    → [Dashboard Reporting]
```

**What This Workflow Does:**
1. Monitors for new article memorandums
2. Extracts content per channel specifications
3. Transforms content to platform-specific formats
4. Schedules posts at optimal times
5. Tracks performance across all channels
6. Reports results in real-time

---

## 📋 N8N Workflow Structure

### **Main Workflow: SAM Campaign Distributor**

```yaml
workflow_name: "SAM_Campaign_Article_Distributor"
trigger: "File watcher"
nodes: 25
execution_mode: "Sequential with parallel branches"
```

---

## 🔄 Node-by-Node Breakdown

### **NODE 1: Trigger - File Watcher**
```yaml
node_type: "Webhook" or "Cron + File Check"
purpose: "Detect new article memorandum"

configuration:
  watch_folder: "C:\Working With AI\Odoo Projects\custom-modules-v18\ai_automator_docs\docs\articles\"
  file_pattern: "ARTICLE_*_MEMORANDUM.md"
  trigger_on: "file_created"

output:
  - file_path
  - file_name
  - created_timestamp
```

---

### **NODE 2: Read Article Memorandum**
```yaml
node_type: "Read File"
purpose: "Load full memorandum content"

configuration:
  file_path: "{{ $json.file_path }}"
  encoding: "utf8"

output:
  - full_content (markdown)
  - file_metadata
```

---

### **NODE 3: Parse YAML Metadata**
```yaml
node_type: "Code (Python/JavaScript)"
purpose: "Extract metadata and extraction points"

code: |
  import yaml
  import re

  content = input_data['full_content']

  # Extract YAML blocks
  metadata_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
  metadata = yaml.safe_load(metadata_match.group(1))

  # Extract extraction points
  extraction_match = re.search(r'## 🔍 EXTRACTION POINTS\n```yaml\n(.*?)\n```', content, re.DOTALL)
  extraction_points = yaml.safe_load(extraction_match.group(1))

  output = {
    'metadata': metadata,
    'extraction_points': extraction_points,
    'full_article': content
  }

output:
  - metadata (dict)
  - extraction_points (dict)
  - full_article (text)
```

---

### **NODE 4: AI Content Analyzer**
```yaml
node_type: "HTTP Request" (Claude API)
purpose: "Analyze content and prepare transformations"

configuration:
  method: "POST"
  url: "https://api.anthropic.com/v1/messages"
  headers:
    x-api-key: "{{ $env.CLAUDE_API_KEY }}"
    anthropic-version: "2023-06-01"

  body:
    model: "claude-3-5-sonnet-20241022"
    max_tokens: 4000
    messages:
      - role: "user"
        content: |
          You are a content transformation specialist for the SAM AI campaign.

          Article Content:
          {{ $json.full_article }}

          Extraction Points:
          {{ $json.extraction_points }}

          Task: Validate content quality and identify key transformation elements for 8 channels.

          Return JSON with:
          {
            "quality_score": 1-10,
            "primary_hooks": [],
            "key_data_points": [],
            "emotional_triggers": [],
            "shareability_score": 1-10,
            "recommendations": []
          }

output:
  - content_analysis (JSON)
```

---

### **NODE 5: Split into 8 Channels**
```yaml
node_type: "Split In Batches" or "Function"
purpose: "Create parallel processing paths"

configuration:
  channels:
    - linkedin
    - twitter
    - medium
    - devto
    - reddit
    - hackernews
    - instagram
    - email

output: [Triggers 8 parallel sub-workflows]
```

---

## 📱 CHANNEL-SPECIFIC SUB-WORKFLOWS

### **SUB-WORKFLOW 1: LinkedIn Distributor**

```yaml
nodes:
  - LinkedIn Content Transformer (AI)
  - Character Count Validator
  - Hashtag Generator
  - Image Attacher
  - LinkedIn API Post
  - Tracking Logger
```

**Node: LinkedIn Content Transformer**
```yaml
node_type: "HTTP Request" (Claude API)
purpose: "Transform to LinkedIn format"

prompt: |
  Transform this article for LinkedIn (professional network).

  Source Article:
  {{ $node["Parse YAML Metadata"].json.full_article }}

  Extraction Points:
  {{ $node["Parse YAML Metadata"].json.extraction_points }}

  Requirements:
  - Length: 150-200 words
  - Tone: Professional + authority
  - Structure: Hook → Value → Question/CTA
  - Include 1 data point
  - End with engagement question
  - Use 3-5 hashtags
  - Optimal for 8 AM posting

  Return only the LinkedIn post text, ready to publish.

output:
  - linkedin_post (text, 150-200 words)
  - hashtags (array)
```

**Node: LinkedIn API Post**
```yaml
node_type: "HTTP Request"
purpose: "Post to LinkedIn"

configuration:
  method: "POST"
  url: "https://api.linkedin.com/v2/ugcPosts"
  authentication: "OAuth2"
  headers:
    Authorization: "Bearer {{ $env.LINKEDIN_ACCESS_TOKEN }}"

  body:
    author: "urn:li:person:{{ $env.LINKEDIN_USER_ID }}"
    lifecycleState: "PUBLISHED"
    specificContent:
      com.linkedin.ugc.ShareContent:
        shareCommentary:
          text: "{{ $json.linkedin_post }}"
        shareMediaCategory: "NONE"
    visibility:
      com.linkedin.ugc.MemberNetworkVisibility: "PUBLIC"

output:
  - post_id
  - post_url
  - timestamp
```

---

### **SUB-WORKFLOW 2: Twitter Thread Distributor**

```yaml
nodes:
  - Thread Generator (AI)
  - Tweet Validator (280 chars each)
  - Thread Compiler
  - Twitter API - Tweet 1
  - Twitter API - Tweet 2-15 (loop)
  - Thread URL Capture
  - Tracking Logger
```

**Node: Thread Generator**
```yaml
node_type: "HTTP Request" (Claude API)

prompt: |
  Transform this article into a Twitter thread.

  Source: {{ $node["Parse YAML Metadata"].json.full_article }}

  Requirements:
  - 15 tweets total
  - Tweet 1: Maximum hook (controversial/surprising)
  - Tweets 2-13: One key point per tweet
  - Tweet 14: Summary
  - Tweet 15: CTA with link
  - Each tweet: Max 280 characters
  - Use (1/15), (2/15) format
  - Include 2-3 hashtags in tweet 1 and 15
  - Numbered thread structure

  Return JSON array of 15 tweets.

output:
  - thread_tweets (array of 15 strings)
```

**Node: Twitter API Loop**
```yaml
node_type: "Loop" with HTTP Request
purpose: "Post tweets sequentially with reply chain"

configuration:
  for_each: "{{ $json.thread_tweets }}"
  delay_between: "180000" # 3 minutes

  tweet_request:
    method: "POST"
    url: "https://api.twitter.com/2/tweets"
    headers:
      Authorization: "Bearer {{ $env.TWITTER_BEARER_TOKEN }}"

    body:
      text: "{{ $item }}"
      reply:
        in_reply_to_tweet_id: "{{ $previousTweetId }}" # Chain tweets

output:
  - thread_url (first tweet URL)
  - all_tweet_ids (array)
```

---

### **SUB-WORKFLOW 3: Medium Article Publisher**

```yaml
nodes:
  - Article Formatter (markdown to Medium)
  - Image Uploader (hero + embedded)
  - Pull Quote Extractor
  - Medium API Post
  - Canonical URL Setter
  - Tracking Logger
```

**Node: Medium API Post**
```yaml
node_type: "HTTP Request"

configuration:
  method: "POST"
  url: "https://api.medium.com/v1/users/{{ $env.MEDIUM_USER_ID }}/posts"
  headers:
    Authorization: "Bearer {{ $env.MEDIUM_ACCESS_TOKEN }}"

  body:
    title: "{{ $json.metadata.seo.seo_title }}"
    contentFormat: "markdown"
    content: "{{ $node['Article Formatter'].json.formatted_article }}"
    tags: ["AI", "Productivity", "Technology", "Innovation", "SAM"]
    publishStatus: "public"
    canonicalUrl: "{{ $json.canonical_url }}"

output:
  - post_url
  - post_id
```

---

### **SUB-WORKFLOW 4: Dev.to Publisher**

```yaml
nodes:
  - Technical Format Converter
  - Code Block Highlighter
  - Dev.to Frontmatter Generator
  - Dev.to API Post
  - Tag Validator
  - Tracking Logger
```

**Node: Dev.to API Post**
```yaml
node_type: "HTTP Request"

configuration:
  method: "POST"
  url: "https://dev.to/api/articles"
  headers:
    api-key: "{{ $env.DEVTO_API_KEY }}"

  body:
    article:
      title: "{{ $json.metadata.seo.seo_title }}"
      published: true
      body_markdown: "{{ $node['Technical Format Converter'].json.devto_markdown }}"
      tags: ["ai", "productivity", "javascript", "python"]
      series: "SAM AI Campaign"
      canonical_url: "{{ $json.canonical_url }}"

output:
  - article_url
  - article_id
```

---

### **SUB-WORKFLOW 5: Reddit Multi-Subreddit Poster**

```yaml
nodes:
  - Reddit Format Converter
  - Subreddit Selector (3 variants)
  - Title Optimizer
  - Reddit API - r/programming
  - Reddit API - r/AI
  - Reddit API - r/SaaS
  - Comment Responder (monitors)
  - Tracking Logger
```

**Node: Reddit API Post**
```yaml
node_type: "HTTP Request" (execute 3 times for 3 subreddits)

configuration:
  method: "POST"
  url: "https://oauth.reddit.com/api/submit"
  headers:
    Authorization: "Bearer {{ $env.REDDIT_ACCESS_TOKEN }}"

  body:
    sr: "{{ $json.subreddit }}" # programming, AI, or SaaS
    kind: "self"
    title: "{{ $json.reddit_title }}"
    text: "{{ $json.reddit_body }}"
    sendreplies: true

output:
  - post_url
  - post_id
  - subreddit
```

---

### **SUB-WORKFLOW 6: Hacker News Poster**

```yaml
nodes:
  - HN Title Optimizer (factual, 80 chars)
  - HN First Comment Generator
  - HN API Submit
  - Comment Poster
  - Engagement Monitor
  - Tracking Logger
```

**Node: HN API Submit**
```yaml
node_type: "HTTP Request"

configuration:
  method: "POST"
  url: "https://news.ycombinator.com/submit"

  form_data:
    title: "{{ $json.hn_title }}"
    url: "{{ $json.article_url }}"
    # Or for text posts:
    text: "{{ $json.hn_text }}"

  # Note: HN doesn't have official API, may need Algolia HN API

output:
  - hn_post_url
  - hn_post_id
```

---

### **SUB-WORKFLOW 7: Instagram Carousel Publisher**

```yaml
nodes:
  - Carousel Slide Generator (AI)
  - Image Designer (Canva API or Bannerbear)
  - Instagram Graph API Auth
  - Container Creator
  - Media Publisher
  - Tracking Logger
```

**Node: Carousel Creator**
```yaml
node_type: "HTTP Request" (Instagram Graph API)

configuration:
  # Step 1: Create container for each slide
  method: "POST"
  url: "https://graph.facebook.com/v18.0/{{ $env.INSTAGRAM_BUSINESS_ID }}/media"

  body:
    image_url: "{{ $json.slide_images[0] }}"
    is_carousel_item: true

  # Step 2: Create carousel container
  method: "POST"
  url: "https://graph.facebook.com/v18.0/{{ $env.INSTAGRAM_BUSINESS_ID }}/media"

  body:
    media_type: "CAROUSEL"
    children: "{{ $json.carousel_item_ids }}"
    caption: "{{ $json.instagram_caption }}"

  # Step 3: Publish
  method: "POST"
  url: "https://graph.facebook.com/v18.0/{{ $env.INSTAGRAM_BUSINESS_ID }}/media_publish"

  body:
    creation_id: "{{ $json.carousel_container_id }}"

output:
  - instagram_post_url
  - instagram_post_id
```

---

### **SUB-WORKFLOW 8: Email Newsletter Sender**

```yaml
nodes:
  - Email Formatter
  - Subject Line Optimizer
  - Subscriber List Fetcher
  - Mailchimp/SendGrid API
  - Delivery Tracker
  - Open Rate Monitor
  - Click Tracker
```

**Node: SendGrid Email Campaign**
```yaml
node_type: "HTTP Request"

configuration:
  method: "POST"
  url: "https://api.sendgrid.com/v3/mail/send"
  headers:
    Authorization: "Bearer {{ $env.SENDGRID_API_KEY }}"

  body:
    personalizations:
      - to:
          - email: "{{ $json.subscriber_email }}"
        dynamic_template_data:
          first_name: "{{ $json.subscriber_name }}"
          article_content: "{{ $json.email_body }}"
          cta_link: "{{ $json.cta_url }}"

    from:
      email: "hello@samai.com"
      name: "SAM AI"

    template_id: "{{ $env.EMAIL_TEMPLATE_ID }}"

    tracking_settings:
      click_tracking:
        enable: true
      open_tracking:
        enable: true

output:
  - message_id
  - recipients_count
  - send_timestamp
```

---

## 📊 AGGREGATION & TRACKING

### **NODE: Performance Aggregator**
```yaml
node_type: "Function"
purpose: "Collect all channel results"

inputs:
  - linkedin_result
  - twitter_result
  - medium_result
  - devto_result
  - reddit_results (array)
  - hn_result
  - instagram_result
  - email_result

code: |
  const results = {
    article_id: input_data.metadata.article_number,
    publish_timestamp: new Date().toISOString(),
    channels: {
      linkedin: {
        post_url: linkedin_result.post_url,
        status: 'published'
      },
      twitter: {
        thread_url: twitter_result.thread_url,
        tweet_count: 15,
        status: 'published'
      },
      // ... all channels
    },
    total_posts: 8,
    estimated_reach: 10000
  }

  return results

output:
  - distribution_summary (JSON)
```

---

### **NODE: Google Analytics Event**
```yaml
node_type: "HTTP Request"
purpose: "Log distribution event"

configuration:
  method: "POST"
  url: "https://www.google-analytics.com/mp/collect"

  body:
    client_id: "{{ $env.GA_CLIENT_ID }}"
    events:
      - name: "article_distributed"
        params:
          article_number: "{{ $json.metadata.article_number }}"
          channels_count: 8
          timestamp: "{{ $json.publish_timestamp }}"

output:
  - tracking_confirmed
```

---

### **NODE: Airtable Logger**
```yaml
node_type: "HTTP Request"
purpose: "Log to campaign tracking database"

configuration:
  method: "POST"
  url: "https://api.airtable.com/v0/{{ $env.AIRTABLE_BASE_ID }}/Campaign%20Tracking"
  headers:
    Authorization: "Bearer {{ $env.AIRTABLE_API_KEY }}"

  body:
    records:
      - fields:
          Article: "{{ $json.metadata.social.headline }}"
          Article_Number: "{{ $json.metadata.article_number }}"
          Publish_Date: "{{ $json.publish_timestamp }}"
          LinkedIn_URL: "{{ $json.channels.linkedin.post_url }}"
          Twitter_URL: "{{ $json.channels.twitter.thread_url }}"
          Medium_URL: "{{ $json.channels.medium.post_url }}"
          DevTo_URL: "{{ $json.channels.devto.article_url }}"
          Reddit_URLs: "{{ $json.channels.reddit.post_urls.join(', ') }}"
          HN_URL: "{{ $json.channels.hn.post_url }}"
          Instagram_URL: "{{ $json.channels.instagram.post_url }}"
          Email_Sent: "{{ $json.channels.email.recipients_count }}"
          Status: "Published"
          Estimated_Reach: 10000

output:
  - airtable_record_id
```

---

## 📈 PERFORMANCE MONITORING SUB-WORKFLOW

### **Continuous Monitoring (Runs every hour)**

```yaml
workflow_name: "SAM_Campaign_Performance_Monitor"
trigger: "Cron (every hour)"

nodes:
  - Fetch All Published Posts
  - LinkedIn Insights API
  - Twitter Analytics API
  - Medium Stats API
  - Dev.to Analytics
  - Reddit Scores
  - Instagram Insights
  - Email Open/Click Stats
  - Aggregate Metrics
  - Update Dashboard
  - Alert on Milestones
```

**Node: LinkedIn Insights**
```yaml
node_type: "HTTP Request"

configuration:
  method: "GET"
  url: "https://api.linkedin.com/v2/organizationalEntityShareStatistics"
  params:
    q: "organizationalEntity"
    organizationalEntity: "{{ $env.LINKEDIN_PAGE_ID }}"
    shares: "{{ $json.linkedin_post_id }}"

output:
  - impressions
  - clicks
  - likes
  - comments
  - shares
```

**Node: Alert on Milestones**
```yaml
node_type: "IF" + "Slack/Email Notification"

conditions:
  - IF total_views > 1000: Alert "Viral threshold!"
  - IF conversions > 10: Alert "Conversion spike!"
  - IF engagement_rate > 10%: Alert "High engagement!"

slack_notification:
  webhook_url: "{{ $env.SLACK_WEBHOOK }}"
  message: |
    🚀 SAM Campaign Alert!

    Article: {{ $json.article_title }}
    Milestone: {{ $json.milestone_type }}

    📊 Stats:
    • Views: {{ $json.total_views }}
    • Engagement: {{ $json.engagement_rate }}%
    • Conversions: {{ $json.conversions }}

    🔗 Details: {{ $json.dashboard_url }}
```

---

## 🎛️ DASHBOARD INTEGRATION

### **Node: Update Real-Time Dashboard**
```yaml
node_type: "HTTP Request" (to dashboard API)

configuration:
  method: "POST"
  url: "{{ $env.DASHBOARD_API_URL }}/update"

  body:
    article_id: "{{ $json.article_number }}"
    metrics:
      total_views: "{{ $json.aggregated.total_views }}"
      total_engagement: "{{ $json.aggregated.total_engagement }}"
      total_clicks: "{{ $json.aggregated.total_clicks }}"
      conversions: "{{ $json.aggregated.conversions }}"

      by_channel:
        linkedin:
          views: "{{ $json.linkedin.impressions }}"
          engagement: "{{ $json.linkedin.engagement }}"
        twitter:
          views: "{{ $json.twitter.impressions }}"
          engagement: "{{ $json.twitter.engagement }}"
        # ... all channels

output:
  - dashboard_updated: true
```

---

## 🔧 ERROR HANDLING & RECOVERY

### **Global Error Handler Node**
```yaml
node_type: "Error Trigger"
purpose: "Catch and handle all workflow errors"

configuration:
  on_error:
    - Log error to Airtable
    - Send alert to Slack
    - Retry failed operation (3 attempts)
    - Fallback to manual notification

  error_logging:
    table: "Error_Log"
    fields:
      - timestamp
      - workflow_name
      - failed_node
      - error_message
      - article_id
      - channel_affected
      - retry_count

  slack_alert:
    message: |
      ⚠️ SAM Campaign Error

      Article: {{ $json.article_id }}
      Failed: {{ $json.failed_node }}
      Channel: {{ $json.channel }}

      Error: {{ $json.error_message }}

      Retry: {{ $json.retry_count }}/3

  retry_logic:
    max_attempts: 3
    delay_between: 300000  # 5 minutes
    exponential_backoff: true
```

---

## 📅 SCHEDULING WORKFLOW

### **Master Schedule Controller**
```yaml
workflow_name: "SAM_Campaign_Schedule_Master"
purpose: "Orchestrate timing across all articles"

configuration:
  articles_schedule:
    article_01:
      launch_day: "Monday Week 1"
      linkedin: "08:00"
      twitter: "09:00"
      medium: "10:00"
      devto: "11:00"
      reddit: "12:00"
      hn: "14:00"
      instagram: "18:00"
      email: "06:00"

    article_02:
      launch_day: "Tuesday Week 1"
      # ... timing

  execution:
    - FOR each article in schedule:
        - Check if launch_day matches today
        - FOR each channel:
            - Wait until scheduled time
            - Trigger channel-specific workflow
            - Log execution
```

---

## 🚀 COMPLETE WORKFLOW EXECUTION FLOW

```
1. FILE WATCHER detects new memorandum
     ↓
2. READ & PARSE memorandum content
     ↓
3. AI ANALYZES and validates content
     ↓
4. SPLIT into 8 parallel paths:

   Path A: LinkedIn
     → Transform content
     → Post to LinkedIn
     → Log tracking

   Path B: Twitter
     → Generate thread
     → Post sequentially
     → Log tracking

   Path C: Medium
     → Format article
     → Upload images
     → Publish

   Path D: Dev.to
     → Convert to technical format
     → Add code blocks
     → Publish

   Path E: Reddit
     → Create 3 subreddit posts
     → Monitor comments
     → Log tracking

   Path F: Hacker News
     → Optimize title
     → Post article
     → Add first comment

   Path G: Instagram
     → Generate carousel
     → Design slides
     → Publish

   Path H: Email
     → Format newsletter
     → Send to list
     → Track opens/clicks

5. AGGREGATE all results
     ↓
6. LOG to tracking systems (Airtable, GA)
     ↓
7. UPDATE real-time dashboard
     ↓
8. MONITOR performance (hourly)
     ↓
9. ALERT on milestones
     ↓
10. REPORT to Slack/Email
```

---

## 📊 EXPECTED AUTOMATION RESULTS

### **Time Savings:**
- Manual distribution time: 8 channels × 30 min = 4 hours
- Automated distribution time: 5 minutes (setup) + 0 minutes (execution)
- **Savings: 3 hours 55 minutes per article**
- **Campaign total: 10 articles × 4 hours = 40 hours saved**

### **Consistency:**
- 100% adherence to platform best practices
- 0% human error in formatting
- Perfect timing across all channels
- Consistent brand voice maintained

### **Scale:**
- 10 articles × 8 channels = 80 posts
- Executed in 10 days
- All tracking automated
- Real-time performance monitoring

---

## ✅ WORKFLOW SETUP CHECKLIST

**API Keys Required:**
- [ ] Claude API (Anthropic)
- [ ] LinkedIn API (OAuth2)
- [ ] Twitter API (Bearer token)
- [ ] Medium API
- [ ] Dev.to API
- [ ] Reddit API (OAuth2)
- [ ] Instagram Graph API
- [ ] SendGrid/Mailchimp API
- [ ] Google Analytics API
- [ ] Airtable API
- [ ] Slack Webhook

**Configuration Needed:**
- [ ] N8N instance running
- [ ] All API credentials stored in environment variables
- [ ] File watcher path configured
- [ ] Dashboard API endpoint set
- [ ] Error logging table created
- [ ] Performance tracking tables ready
- [ ] Slack/Email alerts configured

**Testing Required:**
- [ ] Test article memorandum created
- [ ] Each channel workflow tested individually
- [ ] Full end-to-end test completed
- [ ] Error handling tested
- [ ] Performance monitoring validated
- [ ] Dashboard updates confirmed

---

## 🎯 SUCCESS METRICS

**Workflow Performance:**
- Execution time: <5 minutes per article
- Success rate: >95% across all channels
- Error recovery: <30 minutes
- Tracking accuracy: 100%

**Campaign Performance:**
- Total posts: 80 (10 articles × 8 channels)
- Total reach: 100,000-150,000
- Total engagement: 5,000-10,000
- Total conversions: 50-100

---

**This N8N workflow transforms one information memorandum into 8 optimized, platform-specific posts automatically, saving 40 hours across the campaign while maintaining perfect consistency and tracking.**

**Status:** 🟢 Ready for Implementation

---

**Next Steps:**
1. Set up N8N instance
2. Configure all API credentials
3. Import workflow JSON
4. Test with Article 01
5. Launch campaign automation
