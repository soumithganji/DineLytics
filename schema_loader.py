import yaml
import json


def _load_schema_config():

    with open('schemas/schema.yaml', 'r') as f:
        schema_config = yaml.safe_load(f)

    return schema_config


def _compact_fields(fields, prefix=""):
    """Recursively render fields as compact one-liners: name: type — desc"""
    lines = []
    for name, info in fields.items():
        if not isinstance(info, dict):
            continue
        types = ",".join(info.get("type", ["?"]))
        desc = info.get("description", "")
        if isinstance(desc, list):
            desc = desc[0]
        full = f"{prefix}{name}" if not prefix else f"{prefix}.{name}"
        lines.append(f"  {full}: {types} — {desc}")
        if "items" in info and isinstance(info["items"], dict):
            # Check if items has 'type' directly (simple array) or nested fields
            if "type" in info["items"] and not any(isinstance(v, dict) for v in info["items"].values()):
                continue  # simple typed array, already described
            lines.extend(_compact_fields(info["items"], f"{full}[]"))
    return lines


def load_all_schemas_string():
    """Pre-load ALL database schemas as an ultra-compact one-liner-per-field string.
    Reduces token count by ~70% vs indented JSON."""
    schema_cfg = _load_schema_config()
    parts = []
    for collection_name, path in schema_cfg.get('schema_paths', {}).items():
        try:
            with open(path) as f:
                schema = json.load(f)
            lines = [f"## {collection_name}"]
            lines.extend(_compact_fields(schema.get("fields", {})))
            parts.append("\n".join(lines))
        except Exception as e:
            parts.append(f"## {collection_name}\nError: {e}")
    return "\n".join(parts)


all_schemas_string = load_all_schemas_string()