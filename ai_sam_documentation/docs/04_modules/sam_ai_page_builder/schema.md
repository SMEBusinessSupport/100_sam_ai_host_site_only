# sam_ai_page_builder - Database Schema

Auto-generated model documentation.

## Models (4 total)

### `page.builder.tool.executor`

_Page Builder Tool Executor_

### `sam.ai.page`

_SAM AI Page_

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `page_html` (Text)
- `page_css` (Text)
- `page_js` (Text)
- `ai_prompt_history` (Text)
- `state` (Selection)
- `active` (Boolean)
- `create_uid` (Many2one)
- `create_date` (Date)

### `name`

**Key Fields**:
- `name` (Char)
- `description` (Text)
- `page_html` (Text)
- `page_css` (Text)
- `page_js` (Text)
- `ai_prompt_history` (Text)
- `state` (Selection)
- `active` (Boolean)
- `create_uid` (Many2one)
- `create_date` (Date)

### `sam.page.publisher`

_SAM AI Page Publisher_

**Key Fields**:
- `name` (Char)
