"""
Lekhak — Marathi Proofreader Frontend
Gradio UI connecting to FastAPI backend.
"""

import gradio as gr
import requests

API_URL = "http://localhost:8000"


def check_text(text: str):
    if not text.strip():
        return "कृपया मजकूर टाका.", "", ""

    try:
        response = requests.post(
            f"{API_URL}/check",
            json={"text": text},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        spelling = data.get("spelling", {})
        grammar = data.get("grammar", {})

        spell_errors = spelling.get("errors", [])
        grammar_errors = grammar.get("errors", [])
        total = data.get("total_issues", 0)

        # Summary
        if total == 0:
            summary = "✅ कोणत्याही चुका नाहीत."
        else:
            summary = f"⚠️ एकूण {total} चुका सापडल्या."

        # Spelling output
        if not spell_errors:
            spell_out = "✅ स्पेलिंग ठीक आहे."
        else:
            lines = []
            for e in spell_errors:
                word = e.get("word", "")
                suggestions = e.get("suggestions", [])
                if suggestions:
                    lines.append(f"❌ '{word}' → सुचवणे: {', '.join(suggestions)}")
                else:
                    lines.append(f"❌ '{word}' → कोणतेही सुचवणे नाही")
            spell_out = "\n".join(lines)

        # Grammar output
        if not grammar_errors:
            grammar_out = "✅ व्याकरण ठीक आहे."
        else:
            lines = []
            for e in grammar_errors:
                lines.append(f"⚠️ {e.get('message', 'व्याकरण चूक')}")
            grammar_out = "\n".join(lines)

        return summary, spell_out, grammar_out

    except requests.exceptions.ConnectionError:
        return "❌ API चालू नाही. FastAPI सुरू करा.", "", ""
    except Exception as e:
        return f"❌ त्रुटी: {str(e)}", "", ""


def suggest_word(word: str):
    if not word.strip():
        return "शब्द टाका."

    try:
        response = requests.post(
            f"{API_URL}/suggest",
            json={"word": word},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        suggestions = data.get("suggestions", [])
        if not suggestions:
            return "कोणतेही सुचवणे सापडले नाही."

        lines = [f"{i+1}. {s['word']} (अंतर: {s['distance']})"
                 for i, s in enumerate(suggestions)]
        return "\n".join(lines)

    except requests.exceptions.ConnectionError:
        return "❌ API चालू नाही."
    except Exception as e:
        return f"❌ त्रुटी: {str(e)}"


# ── UI ────────────────────────────────────────────────────────────────────────

with gr.Blocks(title="Lekhak — मराठी प्रूफरीडर", theme=gr.themes.Soft()) as demo:

    gr.Markdown("# ✍️ Lekhak — मराठी प्रूफरीडर")

    # Tab 1 — Full text check
    with gr.Tab("मजकूर तपासा"):
        gr.Markdown("मराठी मजकूर लिहा आणि तपासा.")

        text_input = gr.Textbox(
            label="मराठी मजकूर",
            placeholder="इथे मराठी लिहा...",
            lines=5
        )
        check_btn = gr.Button("तपासा 🔍", variant="primary")

        summary_out  = gr.Textbox(label="सारांश", interactive=False)
        spell_out    = gr.Textbox(label="स्पेलिंग", lines=4, interactive=False)
        grammar_out  = gr.Textbox(label="व्याकरण", lines=4, interactive=False)

        check_btn.click(
            fn=check_text,
            inputs=[text_input],
            outputs=[summary_out, spell_out, grammar_out]
        )

        gr.Examples(
            examples=[
                ["मी शाळेत जातो."],
                ["तो घरि गेला होता."],
                ["माझे नाव रमेश आहे."],
            ],
            inputs=text_input
        )

    # Tab 2 — Single word suggest
    with gr.Tab("शब्द सुचवणे"):
        gr.Markdown("एक शब्द टाका — जवळचे शब्द दाखवतो.")

        word_input  = gr.Textbox(label="शब्द", placeholder="उदा. घरि")
        suggest_btn = gr.Button("सुचवा 💡", variant="primary")
        suggest_out = gr.Textbox(label="सुचवणे", lines=5, interactive=False)

        suggest_btn.click(
            fn=suggest_word,
            inputs=[word_input],
            outputs=[suggest_out]
        )

        gr.Examples(
            examples=[["घरि"], ["शाळा"], ["पुस्तक"]],
            inputs=word_input
        )


if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)