def print_activity(msg):
    if "Assistant" in msg.__class__.__name__:
        print(
            f"🤖 {'Using: ' + msg.content[0].name + '()' if hasattr(msg.content[0], 'name') else 'Thinking...'}"
        )
    elif "User" in msg.__class__.__name__:
        print("✓ Tool completed")


def print_final_result(messages):
    """Print the final agent result and cost information"""
    # Get the resultado message (último message)
    result_msg = messages[-1]

    # encontrar the último assistant message com actual content
    for msg in reversed(messages):
        if msg.__class__.__name__ == "AssistantMessage" and msg.content:
            # verificar se it has texto content (não just tool use)
            for block in msg.content:
                if hasattr(block, "text"):
                    print(f"\n📝 Final Result:\n{block.text}")
                    break
            break

    # Print cost se available
    if hasattr(result_msg, "total_cost_usd"):
        print(f"\n📊 Cost: ${result_msg.total_cost_usd:.2f}")

    # Print duration se available
    if hasattr(result_msg, "duration_ms"):
        print(f"⏱️  Duration: {result_msg.duration_ms / 1000:.2f}s")


def visualize_conversation(messages):
    """Create a visual representation of the entire agent conversation"""
    print("\n" + "=" * 60)
    print("🤖 AGENT CONVERSATION TIMELINE")
    print("=" * 60 + "\n")

    for i, msg in enumerate(messages):
        msg_type = msg.__class__.__name__

        if msg_type == "SystemMessage":
            print("⚙️  System Initialized")
            if hasattr(msg, "data") and "session_id" in msg.data:
                print(f"   Session: {msg.data['session_id'][:8]}...")
            print()

        elif msg_type == "AssistantMessage":
            print("🤖 Assistant:")
            if msg.content:
                for block in msg.content:
                    if hasattr(block, "text"):
                        # texto resposta
                        text = block.text[:500] + "..." if len(block.text) > 500 else block.text
                        print(f"   💬 {text}")
                    elif hasattr(block, "name"):
                        # Tool use
                        tool_name = block.name
                        print(f"   🔧 Using tool: {tool_name}")

                        # Show key parâmetros for certain tools
                        if hasattr(block, "input") and block.input:
                            if tool_name == "WebSearch" and "query" in block.input:
                                print(f'      Query: "{block.input["query"]}"')
                            elif tool_name == "TodoWrite" and "todos" in block.input:
                                todos = block.input["todos"]
                                in_progress = [t for t in todos if t["status"] == "in_progress"]
                                completed = [t for t in todos if t["status"] == "completed"]
                                print(
                                    f"      📋 {len(completed)} completed, {len(in_progress)} in progress"
                                )
            print()

        elif msg_type == "UserMessage":
            if msg.content and isinstance(msg.content, list):
                for result in msg.content:
                    if isinstance(result, dict) and result.get("type") == "tool_result":
                        print("👤 Tool Result Received")
                        tool_id = result.get("tool_use_id", "unknown")[:8]
                        print(f"   ID: {tool_id}...")

                        # Show resultado summary
                        if "content" in result:
                            content = result["content"]
                            if isinstance(content, str):
                                # Show mais of the content
                                summary = content[:500] + "..." if len(content) > 500 else content
                                print(f"   📥 {summary}")
            print()

        elif msg_type == "ResultMessage":
            print("✅ Conversation Complete")
            if hasattr(msg, "num_turns"):
                print(f"   Turns: {msg.num_turns}")
            if hasattr(msg, "total_cost_usd"):
                print(f"   Cost: ${msg.total_cost_usd:.2f}")
            if hasattr(msg, "duration_ms"):
                print(f"   Duration: {msg.duration_ms / 1000:.2f}s")
            if hasattr(msg, "usage"):
                usage = msg.usage
                total_tokens = usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                print(f"   Tokens: {total_tokens:,}")
            print()

    print("=" * 60 + "\n")
