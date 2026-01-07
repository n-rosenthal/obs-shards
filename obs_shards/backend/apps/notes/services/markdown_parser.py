"""
    `backend/apps/notes/services/markdown_parser.py`
    
    A simple Markdown parser for Obsidian notes.
"""

import hashlib
import yaml

FRONTMATTER_DELIMITER = "---"

class MarkdownParseResult:
    def __init__(self, metadata: dict, content: str, content_hash: str) -> None:
        """
        Initializes a MarkdownParseResult object.

        :param metadata: dict of frontmatter from the markdown file
        :param content: str of the markdown content
        :param content_hash: str of the SHA-256 hash of the content
        """
        self.metadata = metadata
        self.content = content
        self.content_hash = content_hash


class MarkdownParser:
    """
    Parser for Markdown files
    """
    @staticmethod
    def parse(text: str) -> MarkdownParseResult:
        """
        Parse a markdown string into a MarkdownParseResult object.

        The markdown string is parsed into its frontmatter and content parts.
        If the markdown string starts with the FRONTMATTER_DELIMITER string,
        the frontmatter is parsed into a dictionary using the yaml module.
        The content is the remaining string after the frontmatter delimiter.
        The content hash is computed using the SHA-256 algorithm.

        :param text: markdown string to be parsed
        :return: a MarkdownParseResult object containing the parsed metadata, content, and content hash
        :rtype: MarkdownParseResult
        """
        metadata = {}
        content = text

        if text.startswith(FRONTMATTER_DELIMITER):
            parts = text.split(FRONTMATTER_DELIMITER, 2)
            metadata = yaml.safe_load(parts[1]) or {}
            content = parts[2].strip()

        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

        return MarkdownParseResult(
            metadata=metadata,
            content=content,
            content_hash=content_hash
        )
