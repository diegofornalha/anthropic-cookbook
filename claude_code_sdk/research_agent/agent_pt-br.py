"""
Research Agent - Using Claude SDK with built-in session management
"""

import asyncio
from collections.abc import Callable
from typing import Any

from dotenv import load_dotenv

from claude_code_sdk import ClaudeCodeOptions, ClaudeSDKClient

load_dotenv()


def get_activity_text(msg) -> str | None:
    """Extract activity text from a message"""
    tentar:
        se "Assistant" in msg.__class__.__name__:
            # Check se content exists and has items
            se hasattr(msg, "content") and msg.content:
                first_content = msg.content[0] se isinstance(msg.content, list) senão msg.content
                se hasattr(first_content, "nome"):
                    retornar f"🤖 Using: {first_content.nome}()"
            retornar "🤖 Thinking..."
        elif "User" in msg.__class__.__name__:
            retornar "✓ Tool completed"
    except (AttributeError, IndexError):
        pass
    retornar None


def print_activity(msg) -> None:
    """Print activity to console"""
    activity = get_activity_text(msg)
    if activity:
        print(activity)


async def send_query(
    prompt: str,
    activity_handler: Callable[[Any], None | Any] = print_activity,
    continue_conversation: bool = False,
) -> str | None:
    """
    Send a query using the Claude SDK with minimal overhead.

    Args:
        prompt: The query to send
        activity_handler: retorno de chamada para activity updates
        continue_conversation: continuar the previous conversation se verdadeiro

    NOTA:
        para the activity_handler - we support both sync and assíncrono handlers
        to make the módulo work in different contexts:
            - Sync handlers (like print_activity) para simple console output
            - assíncrono handlers para web apps that need WebSocket/network I/O
        In production, you'd typically use just one tipo based on your needs

    Retorna:
        The final result text or None se no result
    """
    options = ClaudeCodeOptions(
        model="claude-sonnet-4-20250514",
        allowed_tools=["WebSearch", "Read"],
        continue_conversation=continue_conversation,
        system_prompt="You are a research agent specialized in AI",
    )

    result = None

    try:
        async with ClaudeSDKClient(options=options) as agent:
            await agent.query(prompt=prompt)
            async for msg in agent.receive_response():
                if asyncio.iscoroutinefunction(activity_handler):
                    await activity_handler(msg)
                else:
                    activity_handler(msg)

                if hasattr(msg, "result"):
                    result = msg.result
    except Exception as e:
        print(f"❌ Query error: {e}")
        raise

    return result
