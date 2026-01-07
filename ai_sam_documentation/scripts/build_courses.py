# -*- coding: utf-8 -*-
"""
Build eLearning courses from docs/ folder structure.

Folder structure:
  docs/
    00_sam_skills/        -> slide.channel (Course)
      cto/                -> slide.slide (is_category=True, Section)
        capabilities.md   -> slide.slide (article content)

Runs on module install/upgrade via post_init_hook.
"""

import json
import logging
import re
from pathlib import Path

_logger = logging.getLogger(__name__)

# Optional markdown - fallback to basic if not available
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False
    _logger.warning("markdown library not installed. Using basic conversion.")


def get_module_path():
    """Get the ai_sam_documentation module path."""
    from odoo.modules.module import get_module_path as odoo_get_module_path
    return Path(odoo_get_module_path('ai_sam_documentation'))


def load_json_config(filename):
    """Load a JSON config file from docs/."""
    config_path = get_module_path() / 'docs' / filename
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def slugify(text):
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text


def convert_md_to_html(content):
    """Convert markdown content to HTML."""
    if MARKDOWN_AVAILABLE:
        return markdown.markdown(
            content,
            extensions=['tables', 'fenced_code', 'toc', 'nl2br']
        )
    else:
        # Basic conversion
        html = content
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        html = html.replace('\n\n', '</p><p>')
        return f'<div class="markdown-content"><p>{html}</p></div>'


def extract_title_from_md(content, filename):
    """Extract title from markdown content or filename."""
    # Try to find # Title at start
    match = re.match(r'^#\s+(.+)$', content.strip(), re.MULTILINE)
    if match:
        return match.group(1).strip()
    # Fall back to filename
    return filename.replace('.md', '').replace('_', ' ').replace('-', ' ').title()


def get_or_create_channel(env, folder_name, config):
    """Get or create a slide.channel for the given folder."""
    Channel = env['slide.channel']
    Tag = env['slide.channel.tag']

    # Get config for this course
    course_config = config.get('courses', {}).get(folder_name, {})
    defaults = config.get('defaults', {})

    # Generate display name from config or folder name
    display_name = course_config.get('name', folder_name.replace('_', ' ').title())

    # Check if channel exists
    existing = Channel.search([
        ('name', '=', display_name),
    ], limit=1)

    if existing:
        _logger.info(f"Found existing channel: {existing.name}")
        # Ensure Internal tag is applied
        _apply_internal_tag(env, existing)
        return existing

    # Create new channel
    vals = {
        'name': display_name,
        'description': course_config.get('description', ''),
        'channel_type': course_config.get('channel_type', defaults.get('channel_type', 'training')),
        'visibility': course_config.get('visibility', defaults.get('visibility', 'members')),
        'enroll': course_config.get('enroll', defaults.get('enroll', 'invite')),
        'allow_comment': course_config.get('allow_comment', defaults.get('allow_comment', False)),
        'sequence': course_config.get('sequence', 50),
        'is_published': True,  # Auto-publish on creation
    }

    channel = Channel.create(vals)
    _logger.info(f"Created channel: {channel.name}")

    # Apply Internal tag to new channel
    _apply_internal_tag(env, channel)

    return channel


def _apply_internal_tag(env, channel):
    """Apply the 'Internal' tag to a channel if it exists."""
    Tag = env['slide.channel.tag']
    internal_tag = Tag.search([('name', '=', 'Internal')], limit=1)
    if internal_tag and internal_tag not in channel.tag_ids:
        channel.write({'tag_ids': [(4, internal_tag.id)]})
        _logger.info(f"Applied 'Internal' tag to channel: {channel.name}")


def get_or_create_section(env, channel, section_name, sequence):
    """Get or create a section (slide with is_category=True)."""
    Slide = env['slide.slide']

    display_name = section_name.replace('_', ' ').replace('-', ' ').title()

    existing = Slide.search([
        ('channel_id', '=', channel.id),
        ('is_category', '=', True),
        ('name', '=', display_name)
    ], limit=1)

    if existing:
        # Update sequence to ensure correct ordering
        existing.write({'sequence': sequence})
        return existing

    section = Slide.create({
        'name': display_name,
        'channel_id': channel.id,
        'is_category': True,
        'is_published': True,  # Auto-publish sections
        'sequence': sequence,
    })
    _logger.info(f"Created section: {section.name} in {channel.name}")
    return section


def get_or_create_slide(env, channel, section, md_file, sequence):
    """Get or create a slide from markdown file."""
    Slide = env['slide.slide']

    # Read markdown content
    content_md = md_file.read_text(encoding='utf-8')
    title = extract_title_from_md(content_md, md_file.name)
    content_html = convert_md_to_html(content_md)

    # Check if slide exists
    existing = Slide.search([
        ('channel_id', '=', channel.id),
        ('name', '=', title)
    ], limit=1)

    if existing:
        # Update content AND sequence (category_id is auto-computed from sequence)
        update_vals = {
            'html_content': content_html,
            'sequence': sequence,  # Sequence determines which section slide belongs to
        }
        existing.write(update_vals)
        _logger.info(f"Updated slide: {existing.name} (seq={sequence})")
        return existing

    # Build slide values
    # NOTE: category_id is COMPUTED based on sequence - slides after a section
    # are automatically assigned to that section. We don't set category_id directly.
    vals = {
        'name': title,
        'channel_id': channel.id,
        'slide_category': 'article',  # Use article type for .md content
        'html_content': content_html,
        'is_published': True,  # Auto-publish lessons
        'is_preview': False,
        'sequence': sequence,  # This determines which section the slide belongs to
    }

    # Create new slide
    slide = Slide.create(vals)
    _logger.info(f"Created slide: {slide.name} in {channel.name}")
    return slide


def build_courses(env):
    """Main entry point - build all courses from docs/ folder."""
    _logger.info("=" * 60)
    _logger.info("Building SAM AI Courses from docs/ folder...")
    _logger.info("=" * 60)

    module_path = get_module_path()
    docs_path = module_path / 'docs'

    if not docs_path.exists():
        _logger.warning(f"docs/ folder not found at {docs_path}")
        return

    # Load configuration
    course_config = load_json_config('_course_config.json')

    # Track statistics
    stats = {
        'channels': 0,
        'sections': 0,
        'slides': 0,
    }

    # Process each numbered folder (00_*, 01_*, etc.)
    course_folders = sorted([
        f for f in docs_path.iterdir()
        if f.is_dir() and not f.name.startswith('_') and re.match(r'^\d{2}_', f.name)
    ])

    for course_folder in course_folders:
        _logger.info(f"\nProcessing course folder: {course_folder.name}")

        # Create/get channel
        channel = get_or_create_channel(env, course_folder.name, course_config)
        stats['channels'] += 1

        # IMPORTANT: Use a single global sequence counter for the entire channel
        # Odoo computes category_id based on sequence order:
        # - Section at seq 100
        # - Slides at seq 101, 102, 103... belong to that section
        # - Next section at seq 200
        # - Slides at seq 201, 202, 203... belong to that section
        global_sequence = 0

        # Process subfolders as sections
        for section_folder in sorted(course_folder.iterdir()):
            if not section_folder.is_dir():
                continue
            if section_folder.name.startswith('_'):
                continue

            # Section gets a sequence that's a multiple of 100
            global_sequence = ((global_sequence // 100) + 1) * 100
            section = get_or_create_section(env, channel, section_folder.name, global_sequence)
            stats['sections'] += 1
            _logger.info(f"  Section: {section_folder.name} (seq={global_sequence})")

            # Process .md files in section - they get sequences right after the section
            for md_file in sorted(section_folder.glob('*.md')):
                global_sequence += 1
                get_or_create_slide(env, channel, section, md_file, global_sequence)
                stats['slides'] += 1
                _logger.info(f"    Slide: {md_file.name} (seq={global_sequence})")

        # Also process .md files directly in course folder (no section)
        # These go at the very end with high sequence numbers
        global_sequence = 10000
        for md_file in sorted(course_folder.glob('*.md')):
            global_sequence += 1
            get_or_create_slide(env, channel, None, md_file, global_sequence)
            stats['slides'] += 1

    _logger.info("=" * 60)
    _logger.info(f"Build complete!")
    _logger.info(f"  Channels: {stats['channels']}")
    _logger.info(f"  Sections: {stats['sections']}")
    _logger.info(f"  Slides:   {stats['slides']}")
    _logger.info("=" * 60)

    # NOTE: Do NOT call env.cr.commit() here!
    # Odoo manages transactions automatically in post_init_hook.
    # Manual commits can cause stuck transactions and data integrity issues.
