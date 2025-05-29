# json_tree_viewer.py
import streamlit as st
import json
from streamlit_ace import st_ace

st.title("🌳 JSON Viewer & Path Picker")

json_input = st.text_area("📥 Dán JSON vào đây", height=300)

if json_input:
    try:
        data = json.loads(json_input)
        st.subheader("🧭 Xem JSON")
        content = json.dumps(data, indent=2, ensure_ascii=False)
        selected = st_ace(
            value=content,
            language="json",
            theme="monokai",
            height=400,
            readonly=True
        )

        st.markdown("🔍 Muốn tìm path cho key cụ thể?")
        keyname = st.text_input("Tên key (ví dụ: `videoId`)")

        def find_key_paths(obj, target_key, current_path=None, results=None):
            if current_path is None:
                current_path = []
            if results is None:
                results = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_path = current_path + [f"['{k}']"]
                    if k == target_key:
                        results.append({"path": "".join(new_path), "value": v})
                    find_key_paths(v, target_key, new_path, results)
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    new_path = current_path + [f"[{i}]"]
                    find_key_paths(v, target_key, new_path, results)
            return results

        if keyname:
            results = find_key_paths(data, keyname)
            for r in results:
                st.code(r["path"])
                st.json(r["value"])

    except Exception as e:
        st.error(f"Lỗi: {e}")
