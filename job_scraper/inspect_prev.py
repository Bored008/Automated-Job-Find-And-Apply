import json

with open(r'C:\Users\Bored\.gemini\antigravity\brain\dd4ccb0a-33c4-4540-bdfc-5369b109c2d6\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for idx, line in enumerate(f):
        d = json.loads(line)
        tools = [t.get('name') for t in d.get('tool_calls', [])]
        if 'invoke_subagent' in tools or 'run_command' in tools:
            for t in d.get('tool_calls', []):
                if t.get('name') == 'invoke_subagent':
                    print(f"Step {idx}: invoke_subagent -> Role: {t.get('args', {}).get('Role')}, TypeName: {t.get('args', {}).get('TypeName')}")
                elif t.get('name') == 'run_command' and ('unstop' in str(t.get('args')) or 'apply' in str(t.get('args'))):
                    print(f"Step {idx}: run_command -> {t.get('args', {}).get('CommandLine')[:120]}")
